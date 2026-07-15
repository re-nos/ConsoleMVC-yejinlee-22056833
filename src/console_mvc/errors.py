class DomainError(Exception):
    """도메인 규칙 위반 시 발생하는 공통 예외."""


class NotFoundError(DomainError):
    """조회 대상을 찾을 수 없을 때 발생."""


class DuplicateIdError(DomainError):
    """이미 존재하는 ID로 등록을 시도할 때 발생."""


class InvalidStateError(DomainError):
    """현재 상태에서 허용되지 않는 작업을 시도할 때 발생."""
