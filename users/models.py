from users.repositories import RedisRepository


class User:
    """Model User"""
    __slots__ = ["user_id", "username", "email", "password"]

    def __init__(self, username, email, password):
        self.user_id = RedisRepository.generate_user_id()
        self.username = username
        self.email = email
        self.password = password

    def user_mapping(self):
        """Return Mapping"""
        response = {
            "username": self.username,
            "email": self.email,
            "password": self.password
        }
        return response

    def create_user(self):
        """Create user"""
        RedisRepository.add_user(self)

    @staticmethod
    def delete_user(user_id):
        """Delete user"""
        RedisRepository.delete_user(user_id)
