from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from pim_vi.controller.product_controller import ProductController
from pim_vi.controller.sales_controller import SalesController
from pim_vi.model import User
from pim_vi.model.user_model import UserModel
from pim_vi.controller.user_controller import UserController
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


UserController(app)
SalesController(app)
ProductController(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = TestClient(app)
