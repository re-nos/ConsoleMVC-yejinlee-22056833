from console_mvc.errors import InvalidStateError
from console_mvc.models.order import Order, OrderStatus
from console_mvc.models.repository import OrderRepository, SampleRepository


class OrderController:
    """고객 주문 접수(RESERVED) 및 주문 조회 유스케이스를 담당."""

    def __init__(self, sample_repo: SampleRepository, order_repo: OrderRepository) -> None:
        self._sample_repo = sample_repo
        self._order_repo = order_repo

    def place_order(self, sample_id: str, customer: str, quantity: int) -> Order:
        if quantity <= 0:
            raise InvalidStateError("주문 수량은 1 이상이어야 합니다.")

        self._sample_repo.get(sample_id)  # 존재하지 않으면 NotFoundError 발생
        return self._order_repo.add(sample_id=sample_id, customer=customer, quantity=quantity)

    def list_by_status(self, status: OrderStatus) -> list[Order]:
        return self._order_repo.list_by_status(status)
