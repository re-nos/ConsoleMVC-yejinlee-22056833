import pytest

from console_mvc.controllers.approval_controller import ApprovalController
from console_mvc.controllers.order_controller import OrderController
from console_mvc.controllers.sample_controller import SampleController
from console_mvc.errors import InvalidStateError
from console_mvc.models.order import OrderStatus


@pytest.fixture
def sample_controller(sample_repo) -> SampleController:
    return SampleController(sample_repo)


@pytest.fixture
def order_controller(sample_repo, order_repo) -> OrderController:
    return OrderController(sample_repo, order_repo)


@pytest.fixture
def controller(sample_repo, order_repo, production_line) -> ApprovalController:
    return ApprovalController(sample_repo, order_repo, production_line)


def test_approve_with_sufficient_stock_confirms_immediately(
    sample_controller, order_controller, controller, sample_repo
):
    sample_controller.register_sample("S1", "SiC Wafer", 10.0, 0.5)
    sample_repo.get("S1").stock = 20
    order = order_controller.place_order("S1", "고려대학교", 5)

    approved = controller.approve(order.id)

    assert approved.status == OrderStatus.CONFIRMED
    assert sample_repo.get("S1").stock == 15


def test_approve_with_insufficient_stock_starts_production(
    sample_controller, order_controller, controller, sample_repo, production_line
):
    sample_controller.register_sample("S1", "SiC Wafer", 10.0, 0.5)
    sample_repo.get("S1").stock = 2
    order = order_controller.place_order("S1", "고려대학교", 10)

    approved = controller.approve(order.id)

    assert approved.status == OrderStatus.PRODUCING
    assert sample_repo.get("S1").stock == 0
    job = production_line.current_job()
    assert job is not None
    assert job.order_id == order.id
    assert job.quantity_to_produce == 16  # ceil((10-2) / 0.5)
    assert job.total_time == 160.0  # 10.0 * 16


def test_reject_sets_rejected_status(sample_controller, order_controller, controller):
    sample_controller.register_sample("S1", "SiC Wafer", 10.0, 0.5)
    order = order_controller.place_order("S1", "고려대학교", 5)

    rejected = controller.reject(order.id)

    assert rejected.status == OrderStatus.REJECTED


def test_approve_non_reserved_order_raises(sample_controller, order_controller, controller):
    sample_controller.register_sample("S1", "SiC Wafer", 10.0, 0.5)
    order = order_controller.place_order("S1", "고려대학교", 5)
    controller.reject(order.id)

    with pytest.raises(InvalidStateError):
        controller.approve(order.id)


def test_reject_non_reserved_order_raises(sample_controller, order_controller, controller, sample_repo):
    sample_controller.register_sample("S1", "SiC Wafer", 10.0, 0.5)
    sample_repo.get("S1").stock = 20
    order = order_controller.place_order("S1", "고려대학교", 5)
    controller.approve(order.id)

    with pytest.raises(InvalidStateError):
        controller.reject(order.id)


def test_advance_production_confirms_completed_order(
    sample_controller, order_controller, controller, sample_repo
):
    sample_controller.register_sample("S1", "SiC Wafer", 10.0, 0.5)
    order = order_controller.place_order("S1", "고려대학교", 10)  # shortfall=10, qty_to_produce=20, time=200

    controller.approve(order.id)
    still_producing = controller.advance_production(150)
    completed = controller.advance_production(50)

    assert still_producing == []
    assert len(completed) == 1
    assert completed[0].id == order.id
    assert completed[0].status == OrderStatus.CONFIRMED
