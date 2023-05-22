from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.party.router import current_user
from src.auth.models import User, user
from src.database import get_async_session

router = APIRouter(
    prefix='/account',
    tags=['Account']
)


@router.get('/all')
async def get_self(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    return {'your id': user.id}


@router.get('/all_users', dependencies=[Depends(current_user)])
async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(User))
    result = []
    for r in res:
        result.append(r._asdict())
    return {
        'status': 'success',
        'data': result
    }
