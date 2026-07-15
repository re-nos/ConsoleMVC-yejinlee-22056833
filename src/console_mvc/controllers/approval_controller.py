from console_mvc.errors import InvalidStateError
from console_mvc.models.order import Order, OrderStatus
from console_mvc.models.production import ProductionJob, ProductionLine
from console_mvc.models.repository import OrderRepository, SampleRepository


class ApprovalController:
    """RESERVED 주문의 승인/거절 및 생산 완료에 따른 주문 상태 전환을 담당."""

    def __init__(
        self,
        sample_repo: SampleRepository,
        order_repo: OrderRepository,
        production_line: ProductionLine,
    ) -> None:
        self._sample_repo = sample_repo
        self._order_repo = order_repo
        self._production_line = production_line

    def approve(self, order_id: int) -> Order:
        order = self._order_repo.get(order_id)
        if order.status != OrderStatus.RESERVED:
            raise InvalidStateError(f"RESERVED 상태의 주문만 승인할 수 있습니다: {order_id}")

        sample = self._sample_repo.get(order.sample_id)

        if sample.stock >= order.quantity:
            sample.stock -= order.quantity
            order.status = OrderStatus.CONFIRMED
        else:
            shortfall = order.quantity - sample.stock
            sample.stock = 0
            job = ProductionJob.create(
                order_id=order.id,
                sample_id=sample.id,
                shortfall=shortfall,
                yield_rate=sample.yield_rate,
                avg_production_time=sample.avg_production_time,
            )
            self._production_line.enqueue(job)
            order.status = OrderStatus.PRODUCING

        return order

    def reject(self, order_id: int) -> Order:
        order = self._order_repo.get(order_id)
        if order.status != OrderStatus.RESERVED:
            raise InvalidStateError(f"RESERVED 상태의 주문만 거절할 수 있습니다: {order_id}")

        order.status = OrderStatus.REJECTED
        return order

    def advance_production(self, minutes: float) -> list[Order]:
        """생산 라인 시간을 진행시키고, 완료된 작업에 대응하는 주문을 CONFIRMED로 전환."""
        completed_jobs = self._production_line.tick(minutes)
        completed_orders = []

        for job in completed_jobs:
            order = self._order_repo.get(job.order_id)
            order.status = OrderStatus.CONFIRMED
            completed_orders.append(order)

        return completed_orders
