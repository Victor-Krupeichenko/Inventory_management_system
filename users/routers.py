from fastapi import APIRouter, status, Response
from users.schemes import RegisterUserScheme, AuthUserScheme
from users.models import User
from users.settings_for_token import name_cookies
from users.token_and_current_user import create_access_token
from utils import error_checking

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post("/register_user")
async def register_user(user: RegisterUserScheme):
    """Register User"""
    data = dict(user)
    errors = await error_checking(data, "error")
    if errors:
        return errors
    try:
        new_user = User(username=data.get("username"), password=data.get("password1"), email=data.get("email"))
        new_user.create_user()
        response = {
            "status": status.HTTP_201_CREATED,
            "username": new_user.username,
        }
        return response
    except Exception as ex:
        return {"error": f"{ex}", "status": status.HTTP_400_BAD_REQUEST}


@user_router.post("/login_user")
async def login_user(response: Response, user: AuthUserScheme):
    """Authenticate user"""
    data = dict(user)
    errors = await error_checking(data, "error")
    if errors:
        return errors
    jwt_token = create_access_token(data={"username": user.username})
    response.set_cookie(key=name_cookies, value=f"Bearer {jwt_token}", httponly=True)
    return {
        "token": jwt_token,
        "username": user.username
    }
