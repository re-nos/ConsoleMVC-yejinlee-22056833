import pytest

from console_mvc.controllers.order_controller import OrderController
from console_mvc.controllers.sample_controller import SampleController
from console_mvc.errors import InvalidStateError, NotFoundError
from console_mvc.models.order import OrderStatus


@pytest.fixture
def sample_controller(sample_repo) -> SampleController:
    return SampleController(sample_repo)


@pytest.fixture
def controller(sample_repo, order_repo) -> OrderController:
    return OrderController(sample_repo, order_repo)


def test_place_order(sample_controller, controller):
    sample_controller.register_sample("S1", "SiC Wafer", 10.0, 0.9)

    order = controller.place_order("S1", "고려대학교", 5)

    assert order.id == 1
    assert order.sample_id == "S1"
    assert order.customer == "고려대학교"
    assert order.quantity == 5
    assert order.status == OrderStatus.RESERVED


def test_place_order_unknown_sample_raises(controller):
    with pytest.raises(NotFoundError):
        controller.place_order("UNKNOWN", "고려대학교", 5)


def test_place_order_non_positive_quantity_raises(sample_controller, controller):
    sample_controller.register_sample("S1", "SiC Wafer", 10.0, 0.9)

    with pytest.raises(InvalidStateError):
        controller.place_order("S1", "고려대학교", 0)


def test_place_order_increments_id(sample_controller, controller):
    sample_controller.register_sample("S1", "SiC Wafer", 10.0, 0.9)

    order1 = controller.place_order("S1", "고려대학교", 5)
    order2 = controller.place_order("S1", "카이스트", 3)

    assert order2.id == order1.id + 1
