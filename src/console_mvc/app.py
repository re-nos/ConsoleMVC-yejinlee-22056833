import sys

import colorama

from console_mvc.controllers.approval_controller import ApprovalController
from console_mvc.controllers.monitoring_controller import MonitoringController
from console_mvc.controllers.order_controller import OrderController
from console_mvc.controllers.production_controller import ProductionController
from console_mvc.controllers.sample_controller import SampleController
from console_mvc.controllers.shipment_controller import ShipmentController
from console_mvc.models.production import ProductionLine
from console_mvc.models.repository import OrderRepository, SampleRepository
from console_mvc.views.menu_view import MenuView


def build_menu_view() -> MenuView:
    sample_repo = SampleRepository()
    order_repo = OrderRepository()
    production_line = ProductionLine()

    return MenuView(
        sample_controller=SampleController(sample_repo),
        order_controller=OrderController(sample_repo, order_repo),
        approval_controller=ApprovalController(sample_repo, order_repo, production_line),
        production_controller=ProductionController(production_line),
        monitoring_controller=MonitoringController(sample_repo, order_repo),
        shipment_controller=ShipmentController(order_repo),
    )


def main() -> None:
    # Windows 콘솔 기본 코드페이지(cp949)에서 한글이 깨지는 것을 방지
    sys.stdout.reconfigure(encoding="utf-8")
    # Windows 콘솔에서도 ANSI 컬러 코드가 정상 동작하도록 변환
    colorama.init(autoreset=True)
    build_menu_view().run()


if __name__ == "__main__":
    main()
