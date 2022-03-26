# src/api/users.py
"""User DAO"""
from src.models import Users


class UsersDAO:
    """Class UsersDAO"""
    def __init__(self) -> None:
        self.users = []

    def create(self, id, balance):
        """Create new user"""
        new_user = Users(id, balance)
        for user in self.users:
            if user.id == new_user.id:
                api.abort(404, 0)
        self.users.append(new_user)
        return self.users[-1]

    def get(self, id):
        """Search for user return idx and object Users"""
        for idx, user in enumerate(self.users):
            if user.id == id:
                return idx, self.users[idx]
        return -1, None

    def update(self, id, balance):
        """Update balance value"""
        idx, user = self.get(id)
        if user in self.users:
            self.users[idx].balance = balance
        else:
            api.abort(404, 0)
        return self.users[idx]

    def delete(self, id):
        """Delete Users"""
        idx, user = self.get(id)
        self.users.remove(idx)
