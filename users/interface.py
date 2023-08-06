from abc import ABC, abstractmethod


class IUserRepository(ABC):
    """Interface for user interaction"""

    @abstractmethod
    def add_user(self, user):
        """Add user"""
        pass

    @abstractmethod
    def delete_user(self, user_hash):
        """Delete user"""
        pass

    @abstractmethod
    def get_user(self, username):
        """Getting a user from the database"""
        pass


class IUserAuth(ABC):
    """Interface for user authentication and user credential validation"""

    @abstractmethod
    def exists_user(self, username, flag):
        """There is a user in the database"""
        pass

    @abstractmethod
    def get_password(self, values):
        """Getting a password"""
        pass
