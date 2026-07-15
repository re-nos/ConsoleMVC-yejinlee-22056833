from console_mvc.models.order import Order
from console_mvc.models.production import ProductionJob
from console_mvc.models.sample import Sample


def prompt_str(message: str) -> str:
    return input(message).strip()


def prompt_int(message: str) -> int:
    return int(input(message).strip())


def prompt_float(message: str) -> float:
    return float(input(message).strip())


def print_info(message: str) -> None:
    print(message)


def print_error(message: str) -> None:
    print(f"[오류] {message}")


def print_samples(samples: list[Sample]) -> None:
    if not samples:
        print_info("등록된 시료가 없습니다.")
        return

    print(f"{'ID':<8}{'이름':<16}{'평균생산시간':<12}{'수율':<8}{'재고':<8}")
    for s in samples:
        print(f"{s.id:<8}{s.name:<16}{s.avg_production_time:<12}{s.yield_rate:<8}{s.stock:<8}")


def print_orders(orders: list[Order]) -> None:
    if not orders:
        print_info("해당하는 주문이 없습니다.")
        return

    print(f"{'ID':<6}{'시료ID':<8}{'고객명':<16}{'수량':<8}{'상태':<12}")
    for o in orders:
        print(f"{o.id:<6}{o.sample_id:<8}{o.customer:<16}{o.quantity:<8}{o.status.value:<12}")


def print_counts(counts: dict[str, int]) -> None:
    print("[주문 상태별 건수]")
    for status, count in counts.items():
        print(f"  {status:<12}: {count}건")


def print_stock_statuses(statuses) -> None:
    if not statuses:
        print_info("등록된 시료가 없습니다.")
        return

    print(f"{'시료ID':<8}{'이름':<16}{'재고':<8}{'대기수요':<10}{'상태':<8}{'잔여율':<10}")
    for st in statuses:
        print(
            f"{st.sample_id:<8}{st.name:<16}{st.stock:<8}{st.pending_demand:<10}"
            f"{st.status:<8}{st.remaining_ratio:>6.1f}%"
        )


def print_job(job: ProductionJob | None) -> None:
    if job is None:
        print_info("현재 생산 중인 작업이 없습니다.")
        return

    print(
        f"[생산 중] 주문ID={job.order_id} 시료ID={job.sample_id} "
        f"생산수량={job.quantity_to_produce} 남은시간={job.remaining_time}"
    )


def print_waiting_jobs(jobs: list[ProductionJob]) -> None:
    if not jobs:
        print_info("대기 중인 생산 작업이 없습니다.")
        return

    print("[생산 대기열]")
    for job in jobs:
        print(
            f"  주문ID={job.order_id} 시료ID={job.sample_id} "
            f"생산수량={job.quantity_to_produce} 총생산시간={job.total_time}"
        )
