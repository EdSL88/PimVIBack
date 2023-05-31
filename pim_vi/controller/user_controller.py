import ast
from datetime import datetime, timedelta
from fastapi import FastAPI
from fastapi.params import Header

from pim_vi.controller import Controller
from pim_vi.model import User
from pim_vi.model.user_model import UserModel


class UserController(Controller):
    def __init__(self, app: FastAPI):
        super().__init__()
        app.post("/user")(self.create_user)
        app.post("/user/login")(self.login)
        app.get("/user")(self.get_me)
        app.put("/user")(self.update_user)

    async def create_user(self, user: User):
        user.password = super().get_password_hash(user.password)
        async with UserModel() as m:
            user = await m.create_user(user)
        if not user:
            return {"message": "User not created"}
        return user

    async def update_user(self, user: User, authorization: str = Header(None)):
        try:
            id = super().get_id_from_token(authorization)
            async with UserModel() as m:
                user_db = await m.get_user_by_id(id)
                if not user_db:
                    return {"message": "Usuário não encontrado"}
                if not user.password:
                    user_db = await m.update_user(id, user)
                else:
                    user.password = super().get_password_hash(user.password)
                    user_db = await m.update_user(id, user)
            return user_db
        except Exception as e:
            print(e)
            return {"message": "Erro ao atualizar usuário", "error": e}

    async def get_me(self, authorization: str = Header(None)):
        try:
            id = super().get_id_from_token(authorization)
            async with UserModel() as m:
                user = await m.get_user_by_id(id)
            if not user:
                return {"message": "Usuário não encontrado"}
            return user
        except Exception as e:
            print(e)
            return {"message": "Erro ao buscar usuário", "error": e}

    async def login(self, user: User):
        async with UserModel() as m:
            user_db = await m.login(user)
        if not user_db:
            return {"message": "Usuário não encontrado"}
        if not user or not super().verify_password(user.password, user_db.password):
            return {"message": "Credenciais inválidas"}
        access_token_expires = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_DAYS)
        access_token = super().create_access_token(subject={"id": user_db.id}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
