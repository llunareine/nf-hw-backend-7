from attrs import define
from pydantic import BaseModel, Field, EmailStr
from fastapi.exceptions import HTTPException


@define
class User:
    email: EmailStr
    full_name: str
    password: str
    photo: str
    id: int = 0



class UsersRepository:
    users: list[User]

    def __init__(self):
        self.users = []
    def get_attr(self, user:User):
        return {
            'ID': user.id,
            "email": user.email,
            "full_name": user.full_name,
            "photo": user.photo
        }
    def get_by_email(self, email: str) -> User:
        for user in self.users:
            if user.email == email:
                return user
        return None

    def get_by_id(self, id: int) -> User:
        for user in self.users:
            if user.id == id:
                return user
        return None

    def save(self, user: User):
        user.id = len(self.users) + 1
        self.users.append(user)
        return user


    def get_next_id(self):
        return len(self.users) + 1