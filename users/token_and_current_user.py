from fastapi import Request, status
from datetime import timedelta, datetime
from jose import jwt, JWTError
from settings_for_token import access_token_expire, name_cookies, secret_key, algorithm
from redis_connect import client

ACCESS_TOKEN_EXPIRE_DAY = access_token_expire
NAME_COOKIES = name_cookies


def get_user(username):
    """Getting a user from the database"""
    with client as client_redis:
        return client_redis.hgetall(name=username)


def create_access_token(data: dict):
    """Create token"""
    expire = datetime.now() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAY)  # Срок действия токена
    encoded_jwt = jwt.encode({**data, "exp": expire}, key=secret_key, algorithm=algorithm)  # Кодируем токен
    return encoded_jwt  # Возвращаем закодированный токен


async def get_current_user(request: Request):
    """Getting the current user"""
    response_unauthorized = dict(error=status.HTTP_401_UNAUTHORIZED)
    try:
        cookie = request.cookies.get(name_cookies)  # Из запроса получаем куки
        if cookie is None:
            return response_unauthorized
        token = cookie.split(" ")[1]  # Из кук забираем только токен
        pyload = jwt.decode(token=token, key=secret_key, algorithms=algorithm)  # Декодируем токен
        username = pyload.get("username")  # Получаем из токена имя пользователя
    except JWTError as ex:
        return {"JWT error": f"{ex}"}
    user = get_user(username)  # Получаем пользователя и базы данных
    if not user:
        return response_unauthorized
    current_user = {
        "username": user.get("username"),
        "email": user.get("email")
    }
    return current_user
