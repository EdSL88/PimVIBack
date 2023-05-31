import pytest
from fastapi.testclient import TestClient

from pim_vi import app
from prisma import Prisma


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
async def db():
    await  Prisma().connect()


