from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class User(BaseModel):
    name: str | None = None
    rg: str | None = None
    cpf: str | None = None
    email: str
    password: str


class Sale(BaseModel):
    payment_method: str
    total: float
    product_id: str | None = None
    status: bool = False


class Product(BaseModel):
    name: str
    price: float
    description: str | None = None
    category: str | None = None
    manufacturer: str | None = None
    quantity: int
    image: str | None = None
