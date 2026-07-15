import pytest

from console_mvc.models.production import ProductionLine
from console_mvc.models.repository import OrderRepository, SampleRepository


@pytest.fixture
def sample_repo() -> SampleRepository:
    return SampleRepository()


@pytest.fixture
def order_repo() -> OrderRepository:
    return OrderRepository()


@pytest.fixture
def production_line() -> ProductionLine:
    return ProductionLine()
