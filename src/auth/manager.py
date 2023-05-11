from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin

from src.auth.models import User
from src.auth.utils import get_user_db

from src.config import SECRET

READY_SECRET = SECRET


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = READY_SECRET
    verification_token_secret = READY_SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        # here I can send message to email
        print(f"User {user.id} has registered.")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
