from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.party.router import current_user
from src.auth.models import User
from src.database import get_async_session

router = APIRouter(
    prefix='/account',
    tags=['Account']
)


@router.get('/all')
async def get_self(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    return 'account info'
