from dataclasses import dataclass


@dataclass
class Sample:
    """반도체 시료 정보와 현재 재고를 표현하는 모델."""

    id: str
    name: str
    avg_production_time: float
    yield_rate: float
    stock: int = 0
