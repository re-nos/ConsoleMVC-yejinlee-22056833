from typing import Optional

from console_mvc.models.production import ProductionJob, ProductionLine


class ProductionController:
    """생산 라인의 현재 작업/대기열 조회 유스케이스를 담당 (조회 전용)."""

    def __init__(self, production_line: ProductionLine) -> None:
        self._production_line = production_line

    def current_job(self) -> Optional[ProductionJob]:
        return self._production_line.current_job()

    def waiting_jobs(self) -> list[ProductionJob]:
        return self._production_line.waiting_jobs()
