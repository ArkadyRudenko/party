from select import select

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import user
from src.database import get_async_session

router = APIRouter(
    prefix='/account',
    tags=['Account']
)


@router.get('/all')
async def get_all(session: AsyncSession = Depends(get_async_session)):
    query = select(user).where(len(user.c.username) > 1)
    result = await session.execute(query)
    return result.all()
