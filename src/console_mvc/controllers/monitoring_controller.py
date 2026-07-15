from dataclasses import dataclass

from console_mvc.models.order import OrderStatus
from console_mvc.models.repository import OrderRepository, SampleRepository

_MONITORED_STATUSES = (
    OrderStatus.RESERVED,
    OrderStatus.PRODUCING,
    OrderStatus.CONFIRMED,
    OrderStatus.RELEASE,
)


@dataclass
class StockStatus:
    sample_id: str
    name: str
    stock: int
    pending_demand: int
    status: str  # "여유" | "부족" | "고갈"
    remaining_ratio: float  # 0~100


class MonitoringController:
    """주문 상태별 건수 및 시료별 재고 현황 조회를 담당."""

    def __init__(self, sample_repo: SampleRepository, order_repo: OrderRepository) -> None:
        self._sample_repo = sample_repo
        self._order_repo = order_repo

    def count_by_status(self) -> dict[str, int]:
        counts = {status.value: 0 for status in _MONITORED_STATUSES}
        for order in self._order_repo.list_all():
            if order.status in counts:
                counts[order.status.value] += 1
        return counts

    def stock_status(self) -> list[StockStatus]:
        orders = self._order_repo.list_all()
        result = []

        for sample in self._sample_repo.list_all():
            pending_demand = sum(
                o.quantity
                for o in orders
                if o.sample_id == sample.id and o.status == OrderStatus.RESERVED
            )
            result.append(self._build_stock_status(sample, pending_demand))

        return result

    @staticmethod
    def _build_stock_status(sample, pending_demand: int) -> StockStatus:
        if sample.stock <= 0:
            status, ratio = "고갈", 0.0
        elif pending_demand == 0:
            status, ratio = "여유", 100.0
        elif sample.stock >= pending_demand:
            status, ratio = "여유", min(100.0, sample.stock / pending_demand * 100)
        else:
            status, ratio = "부족", sample.stock / pending_demand * 100

        return StockStatus(
            sample_id=sample.id,
            name=sample.name,
            stock=sample.stock,
            pending_demand=pending_demand,
            status=status,
            remaining_ratio=ratio,
        )
