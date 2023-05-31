from typing import Optional, List

from prisma import Prisma
from prisma.types import ProductsOnSalesWhereUniqueInput

from pim_vi.model import Sale
from prisma.models import Sale as PrismaSale


class SaleModel:
    def __init__(self):
        self.db = Prisma()

    async def __aenter__(self):
        await self.db.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.db.disconnect()

    async def create_sale(self, user_id: str, sale: Sale, products_ids: List[str]) -> Optional[PrismaSale]:
        try:
            sale = await self.db.sale.create({
                "userId": user_id,
                "paymentMethod": sale.payment_method,
                "total": sale.total,
                "productId": products_ids,
            })
            return sale
        except Exception as e:
            print(e)
            return None

    async def get_sales(self, user_id: str) -> Optional[List[PrismaSale]]:
        try:
            return await self.db.sale.find_many(where={"userId": user_id})
        except Exception as e:
            print(e)
            return None

    async def get_sale_by_id(self, sale_id: str) -> Optional[PrismaSale]:
        try:
            return await self.db.sale.find_unique(where={"id": sale_id})
        except Exception as e:
            print(e)
            return None

    async def update_sale(self, id: str, sale: Sale) -> Optional[PrismaSale]:
        try:
            return await self.db.sale.update(where={"id": id}, data={
                "productId": sale.product_id,
                "paymentMethod": sale.payment_method,
                "total": sale.total,
            })
        except Exception as e:
            print(e)
            return None

    async def delete_sale(self, sale_id: str):
        try:
            await self.db.sale.delete(where={"id": sale_id})
        except Exception as e:
            print(e)
            return None
