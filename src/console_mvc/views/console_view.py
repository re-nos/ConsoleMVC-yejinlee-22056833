from console_mvc.models.order import Order
from console_mvc.models.production import ProductionJob
from console_mvc.models.sample import Sample
from console_mvc.views import colors
from console_mvc.views.text_width import pad

_SEPARATOR = "-" * 71

# 컬럼별 표시 폭(전각 문자 기준). 한글 헤더/값이 잘리지 않도록 여유를 둔다.
_SAMPLE_COLS = {"id": 8, "name": 16, "avg_time": 14, "yield_rate": 8, "stock": 8}
_ORDER_COLS = {"id": 6, "sample_id": 8, "customer": 18, "quantity": 8, "status": 12}
_STOCK_COLS = {"sample_id": 8, "name": 16, "stock": 8, "demand": 10, "status": 8}


def prompt_str(message: str) -> str:
    return input(colors.colorize(message, colors.PROMPT)).strip()


def prompt_int(message: str) -> int:
    return int(input(colors.colorize(message, colors.PROMPT)).strip())


def prompt_float(message: str) -> float:
    return float(input(colors.colorize(message, colors.PROMPT)).strip())


def print_info(message: str) -> None:
    print(colors.colorize(message, colors.SUCCESS))


def print_error(message: str) -> None:
    print(colors.colorize(f"[오류] {message}", colors.ERROR))


def print_section_title(title: str) -> None:
    print(colors.colorize("=" * 48, colors.TITLE))
    print(colors.colorize(title, colors.TITLE))
    print(colors.colorize(_SEPARATOR, colors.SEPARATOR))


def print_samples(samples: list[Sample]) -> None:
    print(colors.colorize(f"등록 시료 목록 (총 {len(samples)}종)", colors.HEADER))

    if not samples:
        print_info("등록된 시료가 없습니다.")
        return

    header = (
        pad("ID", _SAMPLE_COLS["id"])
        + pad("이름", _SAMPLE_COLS["name"])
        + pad("평균생산시간", _SAMPLE_COLS["avg_time"])
        + pad("수율", _SAMPLE_COLS["yield_rate"])
        + pad("재고", _SAMPLE_COLS["stock"])
    )
    print(colors.colorize(header, colors.HEADER))
    print(colors.colorize(_SEPARATOR, colors.SEPARATOR))

    for s in samples:
        row = (
            pad(s.id, _SAMPLE_COLS["id"])
            + pad(s.name, _SAMPLE_COLS["name"])
            + pad(str(s.avg_production_time), _SAMPLE_COLS["avg_time"])
            + pad(str(s.yield_rate), _SAMPLE_COLS["yield_rate"])
            + pad(str(s.stock), _SAMPLE_COLS["stock"])
        )
        print(row)


def print_orders(orders: list[Order]) -> None:
    if not orders:
        print_info("해당하는 주문이 없습니다.")
        return

    header = (
        pad("ID", _ORDER_COLS["id"])
        + pad("시료ID", _ORDER_COLS["sample_id"])
        + pad("고객명", _ORDER_COLS["customer"])
        + pad("수량", _ORDER_COLS["quantity"])
        + pad("상태", _ORDER_COLS["status"])
    )
    print(colors.colorize(header, colors.HEADER))
    print(colors.colorize(_SEPARATOR, colors.SEPARATOR))

    for o in orders:
        status_cell = colors.colorize(
            pad(o.status.value, _ORDER_COLS["status"]), colors.order_status_color(o.status.value)
        )
        row = (
            pad(str(o.id), _ORDER_COLS["id"])
            + pad(o.sample_id, _ORDER_COLS["sample_id"])
            + pad(o.customer, _ORDER_COLS["customer"])
            + pad(str(o.quantity), _ORDER_COLS["quantity"])
            + status_cell
        )
        print(row)


def print_counts(counts: dict[str, int]) -> None:
    print(colors.colorize("[주문 상태별 건수]", colors.HEADER))
    for status, count in counts.items():
        status_cell = colors.colorize(pad(status, 12), colors.order_status_color(status))
        print(f"  {status_cell}: {count}건")


def print_stock_statuses(statuses) -> None:
    if not statuses:
        print_info("등록된 시료가 없습니다.")
        return

    header = (
        pad("시료ID", _STOCK_COLS["sample_id"])
        + pad("이름", _STOCK_COLS["name"])
        + pad("재고", _STOCK_COLS["stock"])
        + pad("대기수요", _STOCK_COLS["demand"])
        + pad("상태", _STOCK_COLS["status"])
        + pad("잔여율", 10)
    )
    print(colors.colorize(header, colors.HEADER))
    print(colors.colorize(_SEPARATOR, colors.SEPARATOR))

    for st in statuses:
        status_cell = colors.colorize(pad(st.status, _STOCK_COLS["status"]), colors.stock_status_color(st.status))
        row = (
            pad(st.sample_id, _STOCK_COLS["sample_id"])
            + pad(st.name, _STOCK_COLS["name"])
            + pad(str(st.stock), _STOCK_COLS["stock"])
            + pad(str(st.pending_demand), _STOCK_COLS["demand"])
            + status_cell
            + f"{st.remaining_ratio:>6.1f}%"
        )
        print(row)


def print_job(job: ProductionJob | None) -> None:
    if job is None:
        print_info("현재 생산 중인 작업이 없습니다.")
        return

    print(
        colors.colorize(
            f"[생산 중] 주문ID={job.order_id} 시료ID={job.sample_id} "
            f"생산수량={job.quantity_to_produce} 남은시간={job.remaining_time}",
            colors.WARNING,
        )
    )


def print_waiting_jobs(jobs: list[ProductionJob]) -> None:
    if not jobs:
        print_info("대기 중인 생산 작업이 없습니다.")
        return

    print(colors.colorize("[생산 대기열]", colors.HEADER))
    for job in jobs:
        print(
            f"  주문ID={job.order_id} 시료ID={job.sample_id} "
            f"생산수량={job.quantity_to_produce} 총생산시간={job.total_time}"
        )
