# src/api/models.py
"""Model of users"""


class Users:
    """Class of user"""
    def __init__(self, id, balance) -> None:
        self.id = id
        self.balance = balance
