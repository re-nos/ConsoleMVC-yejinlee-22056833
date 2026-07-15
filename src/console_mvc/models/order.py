from dataclasses import dataclass
from enum import Enum


class OrderStatus(str, Enum):
    RESERVED = "RESERVED"
    REJECTED = "REJECTED"
    PRODUCING = "PRODUCING"
    CONFIRMED = "CONFIRMED"
    RELEASE = "RELEASE"


@dataclass
class Order:
    """고객 주문 한 건을 표현하는 모델."""

    id: int
    sample_id: str
    customer: str
    quantity: int
    status: OrderStatus = OrderStatus.RESERVED
