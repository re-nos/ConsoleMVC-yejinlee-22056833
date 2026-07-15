# CLAUDE.md

이 파일은 Claude Code가 이 저장소에서 작업할 때 참고하는 가이드입니다.

## 프로젝트 개요

콘솔 기반 MVC(Model-View-Controller) 애플리케이션입니다. Python 가상환경(`.venv`)을 사용합니다.
반도체 시료 생산주문관리 시스템 PoC이며 상세 요구사항은 `S_Semi_Project_PRD.md`를 참고합니다.

## 아키텍처: 계층별 책임 분리

- **Model** (`src/console_mvc/models/`): 데이터 구조(dataclass)와 저장소(CRUD)만 담당합니다.
  승인 로직, 생산량 계산 등 비즈니스 규칙은 포함하지 않습니다.
- **Controller** (`src/console_mvc/controllers/`): 유스케이스별로 파일을 분리(단일 책임)하고,
  Model 저장소를 조합해 기능 명세를 구현합니다. 콘솔 입출력에 의존하지 않아 pytest로
  독립적으로 테스트할 수 있어야 합니다.
- **View** (`src/console_mvc/views/`): 입력 수집/출력 포맷팅만 담당하며 비즈니스 로직을
  포함하지 않습니다. Controller가 반환한 순수 데이터를 표시합니다.
- **`app.py`**: 위 세 계층을 조립하는 조립부(composition root)이자 콘솔 메인 루프입니다.
- 데이터는 메모리 내(In-memory)에서만 관리합니다. 파일/DB 영속성은 별도의
  `DataPersistence` PoC 저장소의 몫이므로 이 저장소에 추가하지 않습니다.
- 생산 라인 시간은 실시간이 아닌 턴/틱 기반(`ProductionLine.tick(minutes)`)으로 진행되는
  결정적(deterministic) 방식을 사용합니다. 테스트 용이성을 위한 결정입니다.

## 커밋 컨벤션

[Conventional Commits](https://www.conventionalcommits.org/) 규칙을 따릅니다.

### 커밋 메시지 형식

```
<type>(<scope>): <subject>

<body>

<footer>
```

- **type**: 변경 종류 (필수)
- **scope**: 변경 범위, 예: `model`, `view`, `controller` (선택)
- **subject**: 변경 내용을 명령형, 현재형으로 간결하게 작성 (필수, 마침표 없이)
- **body**: 변경 이유와 내용을 상세히 설명 (선택)
- **footer**: 이슈 참조, Breaking Change 명시 등 (선택)

### type 종류

| type       | 설명                                      |
|------------|-------------------------------------------|
| `feat`     | 새로운 기능 추가                          |
| `fix`      | 버그 수정                                 |
| `refactor` | 기능 변경 없는 코드 구조 개선             |
| `test`     | 테스트 코드 추가/수정                     |
| `docs`     | 문서 수정 (README, CLAUDE.md 등)          |
| `style`    | 코드 포맷팅, 세미콜론 누락 등 (로직 무관) |
| `chore`    | 빌드 설정, 패키지 매니저 등 기타 변경     |
| `perf`     | 성능 개선                                 |

### 예시

```
feat(controller): 사용자 입력 검증 로직 추가

빈 문자열 입력 시 재입력을 요청하도록 컨트롤러에 검증 단계를 추가.

fix(model): 재고 수량 음수 저장 방지

refactor(view): 콘솔 출력 포맷팅 함수 분리

docs: README에 실행 방법 추가
```

### 기타 규칙

- 커밋은 하나의 논리적 변경 단위로 작게 유지합니다.
- subject는 50자 이내를 권장합니다.
- 커밋 메시지는 한글로 작성해도 무방하되, type/scope는 영문 소문자를 사용합니다.
