from api.users.repositories import RedisRepository
from passlib.hash import pbkdf2_sha256


class User:
    """Model User"""
    __slots__ = ["user_hash", "username", "email", "password"]

    def __init__(self, username, email, password):
        self.user_hash = username
        self.username = username
        self.email = email
        self.password = password

    def user_mapping(self):
        """Return Mapping"""
        hashed_password = pbkdf2_sha256.hash(self.password)
        response = {
            "username": self.username,
            "email": self.email,
            "password": hashed_password
        }
        return response

    def create_user(self):
        """Create user"""
        RedisRepository.add_user(self)

    @staticmethod
    def delete_user(user_hash):
        """Delete user"""
        RedisRepository.delete_user(user_hash)
