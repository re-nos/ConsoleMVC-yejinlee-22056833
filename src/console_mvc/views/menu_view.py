from console_mvc.controllers.approval_controller import ApprovalController
from console_mvc.controllers.monitoring_controller import MonitoringController
from console_mvc.controllers.order_controller import OrderController
from console_mvc.controllers.production_controller import ProductionController
from console_mvc.controllers.sample_controller import SampleController
from console_mvc.controllers.shipment_controller import ShipmentController
from console_mvc.errors import DomainError
from console_mvc.models.order import OrderStatus
from console_mvc.views import console_view as view

_MAIN_MENU = """
==================== S-Semi 생산주문관리 시스템 ====================
1. 시료 관리
2. 시료 주문
3. 주문 승인/거절
4. 모니터링
5. 생산 라인
6. 출고 처리
0. 종료
=====================================================================
"""


class MenuView:
    """콘솔 메인 메뉴 렌더링 및 사용자 입력을 각 Controller로 라우팅."""

    def __init__(
        self,
        sample_controller: SampleController,
        order_controller: OrderController,
        approval_controller: ApprovalController,
        production_controller: ProductionController,
        monitoring_controller: MonitoringController,
        shipment_controller: ShipmentController,
    ) -> None:
        self._sample_controller = sample_controller
        self._order_controller = order_controller
        self._approval_controller = approval_controller
        self._production_controller = production_controller
        self._monitoring_controller = monitoring_controller
        self._shipment_controller = shipment_controller

    def run(self) -> None:
        handlers = {
            "1": self._handle_sample_menu,
            "2": self._handle_order_menu,
            "3": self._handle_approval_menu,
            "4": self._handle_monitoring_menu,
            "5": self._handle_production_menu,
            "6": self._handle_shipment_menu,
        }

        while True:
            print(_MAIN_MENU)
            choice = view.prompt_str("메뉴 선택> ")

            if choice == "0":
                view.print_info("시스템을 종료합니다.")
                return

            handler = handlers.get(choice)
            if handler is None:
                view.print_error("올바른 메뉴 번호를 입력하세요.")
                continue

            try:
                handler()
            except DomainError as exc:
                view.print_error(str(exc))
            except ValueError:
                view.print_error("입력 형식이 올바르지 않습니다.")

    def _handle_sample_menu(self) -> None:
        print("\n[시료 관리] 1. 등록  2. 목록  3. 이름 검색")
        choice = view.prompt_str("선택> ")

        if choice == "1":
            sample_id = view.prompt_str("시료 ID: ")
            name = view.prompt_str("시료 이름: ")
            avg_time = view.prompt_float("평균 생산시간: ")
            yield_rate = view.prompt_float("수율(0~1): ")
            sample = self._sample_controller.register_sample(sample_id, name, avg_time, yield_rate)
            view.print_info(f"시료가 등록되었습니다: {sample.id}")
        elif choice == "2":
            view.print_samples(self._sample_controller.list_samples())
        elif choice == "3":
            keyword = view.prompt_str("검색어: ")
            view.print_samples(self._sample_controller.search_by_name(keyword))
        else:
            view.print_error("올바른 메뉴 번호를 입력하세요.")

    def _handle_order_menu(self) -> None:
        sample_id = view.prompt_str("시료 ID: ")
        customer = view.prompt_str("고객명: ")
        quantity = view.prompt_int("주문 수량: ")
        order = self._order_controller.place_order(sample_id, customer, quantity)
        view.print_info(f"주문이 접수되었습니다: 주문ID={order.id}, 상태={order.status.value}")

    def _handle_approval_menu(self) -> None:
        reserved_orders = self._order_controller.list_by_status(OrderStatus.RESERVED)
        view.print_orders(reserved_orders)

        if not reserved_orders:
            return

        order_id = view.prompt_int("승인/거절할 주문 ID: ")
        action = view.prompt_str("승인(a) / 거절(r): ").lower()

        if action == "a":
            order = self._approval_controller.approve(order_id)
        elif action == "r":
            order = self._approval_controller.reject(order_id)
        else:
            view.print_error("'a' 또는 'r'을 입력하세요.")
            return

        view.print_info(f"주문 {order.id} 상태가 {order.status.value}로 변경되었습니다.")

    def _handle_monitoring_menu(self) -> None:
        view.print_counts(self._monitoring_controller.count_by_status())
        view.print_stock_statuses(self._monitoring_controller.stock_status())

    def _handle_production_menu(self) -> None:
        view.print_job(self._production_controller.current_job())
        view.print_waiting_jobs(self._production_controller.waiting_jobs())

        minutes = view.prompt_float("생산 진행 시간(분, 0=진행 안 함): ")
        if minutes > 0:
            completed = self._approval_controller.advance_production(minutes)
            for order in completed:
                view.print_info(f"주문 {order.id}의 생산이 완료되어 CONFIRMED로 전환되었습니다.")

    def _handle_shipment_menu(self) -> None:
        confirmed_orders = self._order_controller.list_by_status(OrderStatus.CONFIRMED)
        view.print_orders(confirmed_orders)

        if not confirmed_orders:
            return

        order_id = view.prompt_int("출고할 주문 ID: ")
        order = self._shipment_controller.release(order_id)
        view.print_info(f"주문 {order.id}가 출고 처리되었습니다: {order.status.value}")
