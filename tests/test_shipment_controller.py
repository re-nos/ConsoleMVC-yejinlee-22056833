import pytest

from console_mvc.controllers.approval_controller import ApprovalController
from console_mvc.controllers.order_controller import OrderController
from console_mvc.controllers.sample_controller import SampleController
from console_mvc.controllers.shipment_controller import ShipmentController
from console_mvc.errors import InvalidStateError
from console_mvc.models.order import OrderStatus


@pytest.fixture
def sample_controller(sample_repo) -> SampleController:
    return SampleController(sample_repo)


@pytest.fixture
def order_controller(sample_repo, order_repo) -> OrderController:
    return OrderController(sample_repo, order_repo)


@pytest.fixture
def approval_controller(sample_repo, order_repo, production_line) -> ApprovalController:
    return ApprovalController(sample_repo, order_repo, production_line)


@pytest.fixture
def controller(order_repo) -> ShipmentController:
    return ShipmentController(order_repo)


def test_release_confirmed_order(
    sample_controller, order_controller, approval_controller, controller, sample_repo
):
    sample_controller.register_sample("S1", "SiC Wafer", 10.0, 0.5)
    sample_repo.get("S1").stock = 10
    order = order_controller.place_order("S1", "고려대학교", 5)
    approval_controller.approve(order.id)

    released = controller.release(order.id)

    assert released.status == OrderStatus.RELEASE


def test_release_non_confirmed_order_raises(sample_controller, order_controller, controller):
    sample_controller.register_sample("S1", "SiC Wafer", 10.0, 0.5)
    order = order_controller.place_order("S1", "고려대학교", 5)  # 아직 RESERVED

    with pytest.raises(InvalidStateError):
        controller.release(order.id)


def test_release_producing_order_raises(
    sample_controller, order_controller, approval_controller, controller
):
    sample_controller.register_sample("S1", "SiC Wafer", 10.0, 0.5)
    order = order_controller.place_order("S1", "고려대학교", 5)  # 재고 0 -> PRODUCING
    approval_controller.approve(order.id)

    with pytest.raises(InvalidStateError):
        controller.release(order.id)


def test_release_twice_raises(
    sample_controller, order_controller, approval_controller, controller, sample_repo
):
    sample_controller.register_sample("S1", "SiC Wafer", 10.0, 0.5)
    sample_repo.get("S1").stock = 10
    order = order_controller.place_order("S1", "고려대학교", 5)
    approval_controller.approve(order.id)
    controller.release(order.id)

    with pytest.raises(InvalidStateError):
        controller.release(order.id)
