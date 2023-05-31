from typing import Optional

from prisma import Prisma

from pim_vi.model import Product
from prisma.models import Product as PrismaProduct


class ProductModel:
    def __init__(self):
        self.db = Prisma()

    async def __aenter__(self):
        await self.db.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.db.disconnect()

    async def create_product(self, product: Product) -> Optional[PrismaProduct]:
        try:
            return await self.db.product.create({
                "name": product.name,
                "price": product.price,
                "image": product.image,
                "quantity": product.quantity,
                "description": product.description,
                "category": product.category,
                "manufacturer": product.manufacturer
            })
        except Exception as e:
            print(e)
            return None

    async def get_all_products(self) -> Optional[list[PrismaProduct]]:
        try:
            return await self.db.product.find_many()
        except Exception as e:
            print(e)
            return None

    async def get_product(self, product_id: str) -> Optional[PrismaProduct]:
        try:
            return await self.db.product.find_unique(where={
                "id": product_id
            })
        except Exception as e:
            print(e)
            return None

    async def delete_product(self, product_id: str) -> Optional[PrismaProduct]:
        try:
            return await self.db.product.delete(where={
                "id": product_id
            })
        except Exception as e:
            print(e)
            return None

    # name: str
    # price: float
    # description: str | None = None
    # category: str | None = None
    # manufacturer: str | None = None
    # quantity: int
    # image: str | None = None

    async def update_product_by_id(self, product_id: str, product: Product):
        try:
            return await self.db.product.update(where={
                "id": product_id
            },
                data={

                    "name": product.name,
                    "price": product.price,
                    "image": product.image,
                    "quantity": product.quantity,
                    "description": product.description,
                    "category": product.category,
                    "manufacturer": product.manufacturer,

                })
        except Exception as e:
            print(e)
            return None
