from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import UserRead
from src.auth.base_config import fastapi_users
from src.auth.models import User, user
from src.database import get_async_session
from src.party.models import party, user_party, invitations
from src.party.schemas import PartyCreate, PartyRead

router = APIRouter(
    prefix='/party',
    tags=['Party']
)

current_user = fastapi_users.current_user()


@router.get('/get_invitations')
async def get_user_invitations(session: AsyncSession = Depends(get_async_session),
                               curr_user: User = Depends(current_user)):
    try:
        query = select(invitations).where(invitations.c.guest_id == curr_user.id)

        result = await session.execute(query)

        result_party = [item[0] for item in result.all()]

        return {
            'status': 'success',
            'data': result_party
        }

    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail={
            'status': 'SQLAlchemyError',
            'data': None,
        })


@router.get('/all')
async def get_all_user_party(session: AsyncSession = Depends(get_async_session),
                             curr_user: User = Depends(current_user)):
    print(curr_user.id)
    try:
        query = select(user_party).where(user_party.c.user_id == curr_user.id)
        result = await session.execute(query)
        party_result = []
        for item in result:
            query = select(party).where(party.c.id == item[1])
            party_res = await session.execute(query)
            party_result.append(party_res.first()._asdict())
        return {
            'status': 'success',
            'data': party_result,
        }
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail={
            'status': 'SQLAlchemyError',
            'data': None,
        })


@router.get('/{party_id}', dependencies=[Depends(current_user)])
@cache(expire=60)
async def get_party(party_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(party).where(party.c.id == party_id)
        party_result = await session.execute(query)

        party_result = PartyRead(**party_result.fetchone()._asdict())

        query = select(user_party).where(user_party.c.party_id == party_id)

        guests_result = await session.execute(query)

        guests = []
        for item in guests_result:
            query = select(user).where(user.c.id == item[0])
            user_res = await session.execute(query)
            party_data = user_res.fetchone()
            if party_data:
                guests.append(UserRead(**party_data._asdict()))

        return {
            'status': 'success',
            'data': {
                'party': party_result,
                'guests': guests,
            }
        }
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail={
            'status': 'SQLAlchemyError',
            'data': None,
        })


@router.post('/')
async def add_party(new_party: PartyCreate, session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_user)):
    try:
        stmt = insert(party).values(
            title=new_party.title,
            description=new_party.description,
            date=new_party.date,
            owner_id=user.id,
        ).returning(party.c.id)

        party_id = -1
        for result in await session.execute(stmt):
            party_id = result.id

        # add self as invited guest
        stmt = insert(user_party).values(
            user_id=user.id,
            party_id=party_id,
        )

        await session.execute(stmt)
        await session.commit()

        return {
            'status': 'success',
            'data': party_id,
        }

    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail={
            'status': 'SQLAlchemyError',
            'data': None,
        })


@router.post('/{party_id}/invite/{guest_id}', dependencies=[Depends(current_user)])
async def invite_user_to_party(party_id: int, guest_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(invitations).values(
            party_id=party_id,
            guest_id=guest_id,
        )

        await session.execute(stmt)
        await session.commit()

        return {
            'status': 'success',
            'data': None
        }

    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail={
            'status': 'SQLAlchemyError',
            'data': None,
        })


@router.post('/{party_id}/accept')
async def accept_invite(party_id: int, session: AsyncSession = Depends(get_async_session),
                        user: User = Depends(current_user)):
    try:
        stmt = insert(user_party).values(
            user_id=user.id,
            party_id=party_id,
        )

        await session.execute(stmt)

        stmt = delete(invitations).where(invitations.c.party_id == party_id
                                         and invitations.c.guest_id == user.id)

        await session.execute(stmt)

        # stmt = update(party).where(party.c.id == party_id).values(count_of_guests=2)
        result = await session.execute(
            update(party)
            .where(party.c.id == party_id)
            .values(count_of_guests=party.c.count_of_guests + 1)
            .returning(party.c.count_of_guests)
        )

        await session.commit()

        return {
            'status': 'success',
            'data': {'count_of_guests': result.scalar()}
        }

    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail={
            'status': 'SQLAlchemyError',
            'data': None,
        })
