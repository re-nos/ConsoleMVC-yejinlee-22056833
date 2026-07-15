from console_mvc.models.repository import SampleRepository
from console_mvc.models.sample import Sample


class SampleController:
    """시료 등록, 목록 조회, 이름 검색 유스케이스를 담당."""

    def __init__(self, sample_repo: SampleRepository) -> None:
        self._sample_repo = sample_repo

    def register_sample(
        self, sample_id: str, name: str, avg_production_time: float, yield_rate: float
    ) -> Sample:
        sample = Sample(
            id=sample_id,
            name=name,
            avg_production_time=avg_production_time,
            yield_rate=yield_rate,
        )
        return self._sample_repo.add(sample)

    def list_samples(self) -> list[Sample]:
        return self._sample_repo.list_all()

    def search_by_name(self, keyword: str) -> list[Sample]:
        return self._sample_repo.search_by_name(keyword)
