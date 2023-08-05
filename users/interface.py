from abc import ABC, abstractmethod


class IUserRepository(ABC):
    """Interface for user interaction"""

    @abstractmethod
    def add_user(self, user):
        """Add user"""
        pass

    @abstractmethod
    def delete_user(self, user_id):
        """Delete user"""
        pass
