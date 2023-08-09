from fastapi import Request, status
from datetime import timedelta, datetime
from jose import jwt, JWTError
from api.users.settings_for_token import access_token_expire, name_cookies, secret_key, algorithm
from api.users.repositories import RedisRepository

ACCESS_TOKEN_EXPIRE_DAY = access_token_expire
NAME_COOKIES = name_cookies


def create_access_token(data: dict):
    """Create token"""
    expire = datetime.now() + timedelta(days=int(ACCESS_TOKEN_EXPIRE_DAY))  # Срок действия токена
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
    user = RedisRepository.get_user(username)  # Получаем пользователя и базы данных
    if not user:
        return response_unauthorized
    current_user = {
        "username": user.get("username"),
        "email": user.get("email")
    }
    return current_user
