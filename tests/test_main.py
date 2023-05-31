import pytest
from fastapi.testclient import TestClient

from faker import Faker
from pim_vi.model import User, Sale, Product
from pim_vi.model.user_model import UserModel


@pytest.mark.asyncio
@pytest.mark.first
async def test_set_user():
    faker = Faker(locale="pt_BR")
    faker.locale = "pt_BR"
    user = User(email=faker.email(), name=faker.name(), password=faker.password())
    user.name = faker.name()
    user.email = faker.email()
    user.password = faker.password()
    pytest.user = user


@pytest.mark.asyncio
async def test_read_main(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.asyncio
@pytest.mark.dependency()
async def test_create_user(client: TestClient):
    response = client.post("/user", json={"name": pytest.user.name, "email": pytest.user.email,
                                          "password": pytest.user.password})
    assert response.status_code == 200
    assert response.json()["id"] != None
    assert response.json()["name"] == pytest.user.name
    assert response.json()["email"] == pytest.user.email
    print(response.json)
    pytest.user_id = response.json()["id"]


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_create_user"])
async def test_read_db_user() -> None:
    async with UserModel() as um:
        user_db = await um.get_user_by_id(pytest.user_id)
        assert user_db is not None
        assert pytest.user.name == user_db.name
        assert pytest.user.email == user_db.email


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_create_user"])
async def test_login_user(client: TestClient):
    """Test"""
    response = client.post("/user/login", json={"email": pytest.user.email, "password": pytest.user.password})
    assert response.status_code == 200
    assert response.json()["access_token"] is not None
    pytest.token = response.json()["access_token"]


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_login_user"])
async def test_get_user(client: TestClient):
    response = client.get("/user", headers={"Authorization": f"Bearer {pytest.token}"})
    assert response.status_code == 200
    assert response.json()["id"] == pytest.user_id
    assert response.json()["name"] == pytest.user.name
    assert response.json()["email"] == pytest.user.email


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_login_user"])
async def test_update_user(client: TestClient):
    faker = Faker()
    faker.locale = "pt_BR"
    user = User(email=faker.email(), name=faker.name(), password=faker.password(), cpf=faker.phone_number(),
                rg=faker.phone_number())
    response = client.put("/user", json={"name": user.name, "email": user.email, "password": user.password},
                          headers={"Authorization": f"Bearer {pytest.token}"})
    assert response.status_code == 200
    assert response.json()["id"] == pytest.user_id
    assert response.json()["name"] == user.name
    assert response.json()["email"] == user.email
    pytest.user = user


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_update_user"])
async def test_get_user_updated(client: TestClient):
    async with UserModel() as um:
        user_db = await um.get_user_by_id(pytest.user_id)
        assert user_db is not None
        assert pytest.user.name == user_db.name
        assert pytest.user.email == user_db.email


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_update_user"])
async def test_create_product(client: TestClient):
    product = Product(name="Teste", price=10.0, image="teste.png", quantity=10)

    response = client.post("/product", json={"name": product.name, "price": product.price, "image": product.image,
                                             "quantity": product.quantity},
                           headers={"Authorization": f"Bearer {pytest.token}"})
    assert response.status_code == 200
    print(response.json())
    assert response.json()["id"] != None
    assert response.json()["name"] == product.name
    assert response.json()["price"] == product.price
    assert response.json()["image"] == product.image
    pytest.product_id = response.json()["id"]


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_create_product"])
async def test_get_product(client: TestClient):
    response = client.get(f"/product/{pytest.product_id}", headers={"Authorization": f"Bearer {pytest.token}"})
    assert response.status_code == 200
    assert response.json()["id"] == pytest.product_id
    assert response.json()["name"] == "Teste"
    assert response.json()["price"] == 10.0
    assert response.json()["image"] == "teste.png"


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_create_user"])
async def test_create_sales(client: TestClient):
    faker = Faker(locale="pt_BR")
    faker.locale = "pt_BR"
    sales = []
    pytest.sales_ids = []
    responses = []
    for i in range(0, 5):
        sale = Sale(payment_method="pix", total=faker.pyfloat(), product_id=pytest.product_id)
        sales.append(sale)
    for sale in sales:
        response = client.post("/sale", json={
            "payment_method": sale.payment_method,
            "total": sale.total,
            "product_id": sale.product_id
        },
                               headers={"Authorization": f"Bearer {pytest.token}"})
        responses.append(response)
    for response in responses:
        assert response.status_code == 200
        assert response.json()["id"] != None
        pytest.sales_ids.append(response.json()["id"])


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_create_sale"])
async def test_get_sales(client: TestClient):
    for sale_id in pytest.sales_ids:
        response = client.get(f"/sale/{sale_id}", headers={"Authorization": f"Bearer {pytest.token}"})
        assert response.status_code == 200
        assert response.json()["id"] == sale_id


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_create_sale"])
async def test_update_product(client: TestClient):
    response = client.put(f"/product/{pytest.product_id}",
                          json={"name": "Teste", "price": 10.0, "image": "teste.png", "quantity": 10},
                          headers={"Authorization": f"Bearer {pytest.token}"})
    print(response.json())
    assert response.status_code == 200
    assert response.json()["id"] == pytest.product_id
    assert response.json()["name"] == "Teste"
    assert response.json()["price"] == 10.0
    assert response.json()["image"] == "teste.png"


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_create_sale"])
async def test_delete_sales(client: TestClient):
    for sale_id in pytest.sales_ids:
        response = client.delete(f"/sale/{sale_id}", headers={"Authorization": f"Bearer {pytest.token}"})
        assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_delete_sales"])
async def test_delete_product(client: TestClient):
    response = client.delete(f"/product/{pytest.product_id}", headers={"Authorization": f"Bearer {pytest.token}"})
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.last
async def test_delete_user():
    async with UserModel() as um:
        await um.delete_user(pytest.user_id)
        user_db = await um.get_user_by_id(pytest.user_id)
        assert user_db is None
