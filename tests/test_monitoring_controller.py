import pytest

from console_mvc.controllers.approval_controller import ApprovalController
from console_mvc.controllers.monitoring_controller import MonitoringController
from console_mvc.controllers.order_controller import OrderController
from console_mvc.controllers.sample_controller import SampleController


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
def controller(sample_repo, order_repo) -> MonitoringController:
    return MonitoringController(sample_repo, order_repo)


def test_count_by_status_excludes_rejected(
    sample_controller, order_controller, approval_controller, controller
):
    sample_controller.register_sample("S1", "SiC Wafer", 10.0, 0.5)
    order1 = order_controller.place_order("S1", "고려대학교", 5)
    order2 = order_controller.place_order("S1", "카이스트", 5)
    order_controller.place_order("S1", "포항공대", 5)  # 그대로 RESERVED 유지

    approval_controller.reject(order1.id)
    approval_controller.approve(order2.id)  # 재고 0 -> PRODUCING

    counts = controller.count_by_status()

    assert counts["RESERVED"] == 1
    assert counts["PRODUCING"] == 1
    assert counts["CONFIRMED"] == 0
    assert counts["RELEASE"] == 0
    assert "REJECTED" not in counts


def test_stock_status_depleted_when_zero_stock(sample_controller, controller):
    sample_controller.register_sample("S1", "SiC Wafer", 10.0, 0.5)

    [status] = controller.stock_status()

    assert status.status == "고갈"
    assert status.remaining_ratio == 0.0


def test_stock_status_sufficient_when_no_demand(sample_controller, controller, sample_repo):
    sample_controller.register_sample("S1", "SiC Wafer", 10.0, 0.5)
    sample_repo.get("S1").stock = 10

    [status] = controller.stock_status()

    assert status.status == "여유"
    assert status.remaining_ratio == 100.0


def test_stock_status_shortage_when_demand_exceeds_stock(
    sample_controller, order_controller, controller, sample_repo
):
    sample_controller.register_sample("S1", "SiC Wafer", 10.0, 0.5)
    sample_repo.get("S1").stock = 4
    order_controller.place_order("S1", "고려대학교", 10)

    [status] = controller.stock_status()

    assert status.status == "부족"
    assert status.remaining_ratio == 40.0


def test_stock_status_sufficient_when_stock_covers_demand(
    sample_controller, order_controller, controller, sample_repo
):
    sample_controller.register_sample("S1", "SiC Wafer", 10.0, 0.5)
    sample_repo.get("S1").stock = 20
    order_controller.place_order("S1", "고려대학교", 10)

    [status] = controller.stock_status()

    assert status.status == "여유"
    assert status.remaining_ratio == 100.0
