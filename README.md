# ConsoleMVC PoC — S-Semi 반도체 시료 생산주문관리 시스템

`S_Semi_Project_PRD.md` 미션1-①(MVC 스켈레톤 코드)에 해당하는 PoC입니다.
Model / Controller / View 역할 분리를 검증하기 위한 콘솔 애플리케이션이며,
데이터는 메모리 내(In-memory)에서만 관리하고, 생산 라인 시간은 턴/틱 기반으로
결정적(deterministic)으로 진행됩니다.

## 요구 사항

- Python 3.14 (기존 `.venv` 사용)
- pytest (`requirements.txt`)

## 설치

```bash
.venv/Scripts/python.exe -m pip install -r requirements.txt
```

## 실행

```bash
PYTHONPATH=src .venv/Scripts/python.exe -m console_mvc.app
```

Windows 콘솔에서 한글이 깨지는 경우, 실행 전 `chcp 65001`로 코드페이지를
UTF-8로 변경하세요.

### 사용 흐름 예시

1. `1` 시료 관리 → `1` 등록으로 시료(ID, 이름, 평균생산시간, 수율) 등록
2. `2` 시료 주문으로 주문 접수 (초기 상태 `RESERVED`)
3. `3` 주문 승인/거절 → 승인 시 재고 충분하면 즉시 `CONFIRMED`,
   부족하면 생산 라인에 등록되어 `PRODUCING`
4. `5` 생산 라인에서 진행 시간(분)을 입력해 생산을 진행 → 완료되면 `CONFIRMED`
5. `4` 모니터링으로 상태별 건수 및 재고 현황 확인
6. `6` 출고 처리로 `CONFIRMED` 주문을 `RELEASE`로 전환

## 테스트

```bash
.venv/Scripts/python.exe -m pytest
```

## 구조

```
src/console_mvc/
  models/       # Sample, Order, ProductionJob/Line, 저장소(CRUD)
  controllers/  # 유스케이스별 컨트롤러 (시료/주문/승인/생산/모니터링/출고)
  views/        # 콘솔 입출력 및 메뉴 라우팅
  app.py        # 조립부(composition root)
tests/          # pytest 테스트
```

각 계층의 책임 분리 기준은 `CLAUDE.md`를 참고하세요.
