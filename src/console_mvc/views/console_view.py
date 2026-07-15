from console_mvc.models.order import Order
from console_mvc.models.production import ProductionJob
from console_mvc.models.sample import Sample
from console_mvc.views import colors

_SEPARATOR = "-" * 71


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

    print(colors.colorize(f"{'ID':<8}{'이름':<16}{'평균생산시간':<12}{'수율':<8}{'재고':<8}", colors.HEADER))
    print(colors.colorize(_SEPARATOR, colors.SEPARATOR))
    for s in samples:
        print(f"{s.id:<8}{s.name:<16}{s.avg_production_time:<12}{s.yield_rate:<8}{s.stock:<8}")


def print_orders(orders: list[Order]) -> None:
    if not orders:
        print_info("해당하는 주문이 없습니다.")
        return

    print(colors.colorize(f"{'ID':<6}{'시료ID':<8}{'고객명':<16}{'수량':<8}{'상태':<12}", colors.HEADER))
    print(colors.colorize(_SEPARATOR, colors.SEPARATOR))
    for o in orders:
        status_cell = colors.colorize(f"{o.status.value:<12}", colors.order_status_color(o.status.value))
        print(f"{o.id:<6}{o.sample_id:<8}{o.customer:<16}{o.quantity:<8}{status_cell}")


def print_counts(counts: dict[str, int]) -> None:
    print(colors.colorize("[주문 상태별 건수]", colors.HEADER))
    for status, count in counts.items():
        status_cell = colors.colorize(f"{status:<12}", colors.order_status_color(status))
        print(f"  {status_cell}: {count}건")


def print_stock_statuses(statuses) -> None:
    if not statuses:
        print_info("등록된 시료가 없습니다.")
        return

    print(
        colors.colorize(
            f"{'시료ID':<8}{'이름':<16}{'재고':<8}{'대기수요':<10}{'상태':<8}{'잔여율':<10}", colors.HEADER
        )
    )
    print(colors.colorize(_SEPARATOR, colors.SEPARATOR))
    for st in statuses:
        status_cell = colors.colorize(f"{st.status:<8}", colors.stock_status_color(st.status))
        print(
            f"{st.sample_id:<8}{st.name:<16}{st.stock:<8}{st.pending_demand:<10}"
            f"{status_cell}{st.remaining_ratio:>6.1f}%"
        )


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
