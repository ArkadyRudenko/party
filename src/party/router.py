from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import fastapi_users
from src.auth.models import User
from src.database import get_async_session
from src.party.models import party, user_party
from src.party.schemas import PartyCreate

router = APIRouter(
    prefix='/party',
    tags=['Party']
)

current_user = fastapi_users.current_user()


@router.get('/all')
async def get_all(session: AsyncSession = Depends(get_async_session),
                  user: User = Depends(current_user)):
    print(user.id)
    query = select(user_party).where(user_party.c.user_id == user.id)
    result = await session.execute(query)
    party_result = []
    for item in result:
        query = select(party).where(party.c.id == item[1])
        party_res = await session.execute(query)
        party_result.append(party_res.first()._asdict())

    return party_result


@router.get('/{party_id}', dependencies=[Depends(current_user)])
async def get_party(party_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(party).where(party.c.id == party_id)
    result = await session.execute(query)
    return result.first()._asdict()


@router.post('/')
async def add_party(new_party: PartyCreate, session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_user)):
    stmt = insert(party).values(
        title=new_party.title,
        description=new_party.description,
        date=new_party.date,
        owner_id=user.id,
    ).returning(party.c.id)

    party_id = -1
    for result in await session.execute(stmt):
        party_id = result.id

    stmt = insert(user_party).values(
        user_id=user.id,
        party_id=party_id,
    )

    await session.execute(stmt)
    await session.commit()

    return {'status': 200}
