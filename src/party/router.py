from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.party.models import party
from src.party.schemas import PartyCreate

router = APIRouter(
    prefix='/party',
    tags=['Party']
)


@router.get('/{party_id}')
async def get_party(party_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(party).where(party.c.id == party_id)
    result = await session.execute(query)
    return result.all()


@router.post('/')
async def add_party(new_party: PartyCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(party).values(**new_party.dict())
    await session.execute(stmt)
    await session.commit()
    return {'status': 200}


