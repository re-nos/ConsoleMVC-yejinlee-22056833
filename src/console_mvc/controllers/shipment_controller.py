from console_mvc.errors import InvalidStateError
from console_mvc.models.order import Order, OrderStatus
from console_mvc.models.repository import OrderRepository


class ShipmentController:
    """CONFIRMED 상태 주문의 출고(RELEASE) 처리를 담당."""

    def __init__(self, order_repo: OrderRepository) -> None:
        self._order_repo = order_repo

    def release(self, order_id: int) -> Order:
        order = self._order_repo.get(order_id)
        if order.status != OrderStatus.CONFIRMED:
            raise InvalidStateError(f"CONFIRMED 상태의 주문만 출고할 수 있습니다: {order_id}")

        order.status = OrderStatus.RELEASE
        return order
