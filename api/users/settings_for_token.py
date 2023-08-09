import os
from dotenv import load_dotenv

load_dotenv()
secret_key = os.getenv("SECRET_KEY_TOKEN")
algorithm = os.getenv("ALGORITHM_TOKEN")
name_cookies = os.getenv("NAME_COOKIES")
access_token_expire = os.getenv("ACCESS_TOKEN_EXPIRE_DAYS")
