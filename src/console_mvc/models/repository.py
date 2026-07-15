from typing import Optional

from console_mvc.errors import DuplicateIdError, NotFoundError
from console_mvc.models.order import Order
from console_mvc.models.sample import Sample


class SampleRepository:
    """시료 데이터를 메모리 내 dict로 관리하는 저장소."""

    def __init__(self) -> None:
        self._samples: dict[str, Sample] = {}

    def add(self, sample: Sample) -> Sample:
        if sample.id in self._samples:
            raise DuplicateIdError(f"이미 존재하는 시료 ID입니다: {sample.id}")
        self._samples[sample.id] = sample
        return sample

    def get(self, sample_id: str) -> Sample:
        sample = self._samples.get(sample_id)
        if sample is None:
            raise NotFoundError(f"존재하지 않는 시료 ID입니다: {sample_id}")
        return sample

    def find(self, sample_id: str) -> Optional[Sample]:
        return self._samples.get(sample_id)

    def list_all(self) -> list[Sample]:
        return list(self._samples.values())

    def search_by_name(self, keyword: str) -> list[Sample]:
        keyword_lower = keyword.lower()
        return [s for s in self._samples.values() if keyword_lower in s.name.lower()]


class OrderRepository:
    """주문 데이터를 메모리 내 dict로 관리하는 저장소."""

    def __init__(self) -> None:
        self._orders: dict[int, Order] = {}
        self._next_id: int = 1

    def add(self, sample_id: str, customer: str, quantity: int) -> Order:
        order = Order(id=self._next_id, sample_id=sample_id, customer=customer, quantity=quantity)
        self._orders[order.id] = order
        self._next_id += 1
        return order

    def get(self, order_id: int) -> Order:
        order = self._orders.get(order_id)
        if order is None:
            raise NotFoundError(f"존재하지 않는 주문 ID입니다: {order_id}")
        return order

    def list_all(self) -> list[Order]:
        return list(self._orders.values())

    def list_by_status(self, status) -> list[Order]:
        return [o for o in self._orders.values() if o.status == status]
