from collections import deque
from dataclasses import dataclass
from math import ceil
from typing import Optional


@dataclass
class ProductionJob:
    """생산 라인에 등록된 단일 생산 작업(하나의 주문에 대응)."""

    order_id: int
    sample_id: str
    quantity_to_produce: int
    total_time: float
    remaining_time: float

    @classmethod
    def create(
        cls, order_id: int, sample_id: str, shortfall: int, yield_rate: float, avg_production_time: float
    ) -> "ProductionJob":
        quantity_to_produce = ceil(shortfall / yield_rate)
        total_time = avg_production_time * quantity_to_produce
        return cls(
            order_id=order_id,
            sample_id=sample_id,
            quantity_to_produce=quantity_to_produce,
            total_time=total_time,
            remaining_time=total_time,
        )


class ProductionLine:
    """단일 생산 라인의 FIFO 큐와 틱(turn) 기반 시간 진행을 담당."""

    def __init__(self) -> None:
        self._queue: deque[ProductionJob] = deque()

    def enqueue(self, job: ProductionJob) -> ProductionJob:
        self._queue.append(job)
        return job

    def current_job(self) -> Optional[ProductionJob]:
        return self._queue[0] if self._queue else None

    def waiting_jobs(self) -> list[ProductionJob]:
        return list(self._queue)[1:]

    def tick(self, minutes: float) -> list[ProductionJob]:
        """minutes만큼 시간을 진행시키고, 그 사이 완료된 작업 목록을 FIFO 순서로 반환."""
        completed: list[ProductionJob] = []
        remaining_minutes = minutes

        while remaining_minutes > 0 and self._queue:
            job = self._queue[0]
            consumed = min(remaining_minutes, job.remaining_time)
            job.remaining_time -= consumed
            remaining_minutes -= consumed

            if job.remaining_time <= 0:
                job.remaining_time = 0
                completed.append(job)
                self._queue.popleft()
            else:
                break

        return completed
