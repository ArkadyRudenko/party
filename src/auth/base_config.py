from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from src.auth.manager import get_user_manager
from src.auth.models import User

from src.config import SECRET

cookie_transport = CookieTransport(cookie_name='party', cookie_max_age=3600)

READY_SECRET = SECRET


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=READY_SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
