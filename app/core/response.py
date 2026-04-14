from typing import Any

from pydantic import BaseModel


class UnifiedAPIResponse(BaseModel):
    """Standard envelope for all API JSON responses."""

    success: bool
    message: str
    statusCode: int
    data: dict[str, Any] | list[Any] | None = None

    def to_json_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


def success_response(
    *,
    message: str,
    status_code: int = 200,
    data: dict[str, Any] | list[Any] | None = None,
) -> dict[str, Any]:
    return UnifiedAPIResponse(
        success=True,
        message=message,
        statusCode=status_code,
        data=data,
    ).to_json_dict()


def error_response(
    *,
    message: str,
    status_code: int,
    data: dict[str, Any] | list[Any] | None = None,
) -> dict[str, Any]:
    return UnifiedAPIResponse(
        success=False,
        message=message,
        statusCode=status_code,
        data=data,
    ).to_json_dict()
