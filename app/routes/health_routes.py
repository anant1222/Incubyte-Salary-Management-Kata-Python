from typing import Any

from fastapi import APIRouter

from app.core.response import success_response
from app.services import health_service

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, Any]:
    data = health_service.get_health_payload()
    return success_response(
        message="Health check successful",
        status_code=200,
        data=data,
    )
