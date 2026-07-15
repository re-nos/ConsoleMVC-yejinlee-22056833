import pytest

from console_mvc.controllers.sample_controller import SampleController
from console_mvc.errors import DuplicateIdError


@pytest.fixture
def controller(sample_repo) -> SampleController:
    return SampleController(sample_repo)


def test_register_sample(controller):
    sample = controller.register_sample("S1", "SiC Wafer", 10.0, 0.9)

    assert sample.id == "S1"
    assert sample.name == "SiC Wafer"
    assert sample.stock == 0


def test_register_duplicate_id_raises(controller):
    controller.register_sample("S1", "SiC Wafer", 10.0, 0.9)

    with pytest.raises(DuplicateIdError):
        controller.register_sample("S1", "GaN Wafer", 5.0, 0.8)


def test_list_samples(controller):
    controller.register_sample("S1", "SiC Wafer", 10.0, 0.9)
    controller.register_sample("S2", "GaN Wafer", 5.0, 0.8)

    samples = controller.list_samples()

    assert {s.id for s in samples} == {"S1", "S2"}


def test_search_by_name(controller):
    controller.register_sample("S1", "SiC Wafer", 10.0, 0.9)
    controller.register_sample("S2", "GaN Wafer", 5.0, 0.8)

    result = controller.search_by_name("sic")

    assert len(result) == 1
    assert result[0].id == "S1"


def test_search_by_name_no_match(controller):
    controller.register_sample("S1", "SiC Wafer", 10.0, 0.9)

    assert controller.search_by_name("unknown") == []
