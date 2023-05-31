from typing import List

from fastapi.params import Header

from pim_vi.controller import Controller
from pim_vi.model import Sale, Product
from pim_vi.model.sale_model import SaleModel


class SalesController(Controller):
    def __init__(self, app):
        super().__init__()
        app.post("/sale")(self.create_sale)
        app.get("/sale")(self.get_sales)
        app.get("/sale/{sale_id}")(self.get_sale_by_id)
        app.delete("/sale/{sale_id}")(self.delete_sale)

    async def create_sale(self, products_ids: List[str], sale: Sale, authorization: str = Header(None)):
        try:
            user_id = super().get_id_from_token(authorization)
            async with SaleModel() as m:
                sale = await m.create_sale(user_id, sale, products_ids)
            if not sale:
                return {"message": "Sale not created"}
            return sale
        except Exception as e:
            print(e)
            return {"message": "Erro ao criar venda", "error": e}

    async def get_sales(self, authorization: str = Header(None)):
        try:
            user_id = super().get_id_from_token(authorization)
            async with SaleModel() as m:
                sales = await m.get_sales(user_id)
            if not sales:
                return {"message": "Sales not found"}
            return sales
        except Exception as e:
            print(e)
            return {"message": "Erro ao buscar vendas", "error": e}

    async def get_sale_by_id(self, sale_id: str):
        try:
            async with SaleModel() as m:
                sale = await m.get_sale_by_id(sale_id)
            if not sale:
                return {"message": "Sale not found"}
            return sale
        except Exception as e:
            print(e)
            return {"message": "Erro ao buscar venda", "error": e}

    async def delete_sale(self, sale_id: str):
        try:
            async with SaleModel() as m:
                sale = await m.delete_sale(sale_id)
            if not sale:
                return {"message": "Sale not found"}
            return sale
        except Exception as e:
            print(e)
            return {"message": "Erro ao buscar venda", "error": e}
