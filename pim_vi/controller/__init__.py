import ast
from ctypes import Union
from datetime import datetime, timedelta
from typing import Any, Tuple, Dict, Optional

from jose import jwt
from passlib.context import CryptContext


class Controller:
    def __init__(self):
        self.SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_DAYS = 3650

    def get_password_hash(self, password: str) -> str:
        return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(plain_password, hashed_password)

    def create_access_token(self, subject: Any, expires_delta: int = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(days=self.ACCESS_TOKEN_EXPIRE_DAYS)

        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, self.ALGORITHM)
        return encoded_jwt

    def verify_acess_token(self, token: str) -> bool:
        try:
            token = token.split(" ")[1]
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return True
        except Exception as e:
            print(e)
            return False

    def decode_token(self, token: str) -> Optional[Dict]:
        try:
            token = token.split(" ")[1]
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except Exception as e:
            print(e)
            return None

    def get_id_from_token(self, token: Dict):
        try:
            token = self.decode_token(token).get("sub")
            ast_e = ast.literal_eval(token)
            id = ast_e.get("id")
            return id
        except Exception as e:
            print(e)
            return None
