from fastapi.params import Header

from pim_vi.controller import Controller
from pim_vi.model import Product
from pim_vi.model.product_model import ProductModel


class ProductController(Controller):
    def __init__(self, app):
        super().__init__()
        app.post("/product")(self.create_product)
        app.get("/product/{product_id}")(self.get_product)
        app.get("/product")(self.get_products)
        app.delete("/product/{product_id}")(self.delete_product)
        app.put("/product/{product_id}")(self.update_product)

    async def create_product(self, product: Product, authorization: str = Header(None)):
        try:
            user_id = super().get_id_from_token(authorization)
            async with ProductModel() as m:
                product = await m.create_product(product)
            if not product:
                return {"message": "Product not created"}
            return product
        except Exception as e:
            print(e)
            return {"message": "Erro ao criar produto", "error": e}

    async def get_products(self):
        try:
            async with ProductModel() as m:
                products = await m.get_all_products()
            if not products:
                return {"message": "Products not found"}
            return products
        except Exception as e:
            print(e)
            return {"message": "Erro ao buscar produtos", "error": e}

    async def get_product(self, product_id: str, authorization: str = Header(None)):
        try:
            user_id = super().get_id_from_token(authorization)
            async with ProductModel() as m:
                product = await m.get_product(product_id)
            if not product:
                return {"message": "Product not found"}
            return product
        except Exception as e:
            print(e)
            return {"message": "Erro ao buscar produto", "error": e}

    async def delete_product(self, product_id: str, authorization: str = Header(None)):
        try:
            user_id = super().get_id_from_token(authorization)
            async with ProductModel() as m:
                product = await m.delete_product(product_id)
            if not product:
                return {"message": "Product not found"}
            return product
        except Exception as e:
            print(e)
            return {"message": "Erro ao buscar produto", "error": e}

    async def update_product(self, product_id: str, product: Product, authorization: str = Header(None)):
        try:
            user_id = super().get_id_from_token(authorization)
            async with ProductModel() as m:
                product = await m.update_product_by_id(product_id, product)
            if not product:
                return {"message": "Product not found"}
            return product
        except Exception as e:
            print(e)
            return {"message": "Erro ao buscar produto", "error": e}
