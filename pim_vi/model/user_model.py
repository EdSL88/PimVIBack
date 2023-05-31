from datetime import datetime, timedelta
from typing import Optional, Union, Any

from jose import jwt
from prisma import Prisma
from pim_vi.model import User
from prisma.models import User as PrismaUser
from passlib.context import CryptContext


class UserModel:
    def __init__(self):
        self.db = Prisma()

    async def __aenter__(self):
        await self.db.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.db.disconnect()

    async def create_user(self, user: User) -> Optional[PrismaUser]:
        try:
            return await self.db.user.create({
                "name": user.name,
                "email": user.email,
                "password": user.password,
                "rg": user.rg,
                "cpf": user.cpf,
            })
        except Exception as e:
            print(e)
            return None

    async def login(self, user: User) -> PrismaUser:
        user_db = await self.db.user.find_first(where={"email": user.email})
        return user_db

    async def get_user_by_email(self, user: User) -> Optional[PrismaUser]:
        try:
            return await self.db.user.find_unique(where={"email": user.email})
        except Exception as e:
            print(e)
            return None

    async def get_user_by_id(self, user_id: str) -> Optional[PrismaUser]:
        try:
            return await self.db.user.find_unique(where={"id": user_id})
        except Exception as e:
            print(e)
            return None

    async def update_user(self, id: str, user: PrismaUser) -> Optional[PrismaUser]:
        try:
            return await self.db.user.update(where={"id": id}, data={
                "name": user.name,
                "email": user.email,
                "password": user.password,
                "rg": user.rg,
                "cpf": user.cpf
            })
        except Exception as e:
            print(e)
            return None

    async def delete_user(self, user_id: str):
        try:
            return await self.db.user.delete(where={"id": user_id})
        except Exception as e:
            print(e)
            return None
