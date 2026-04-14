from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import AppException
from app.core.response import error_response

_SKIP_LOC = frozenset({"body", "query", "path", "header", "cookie"})


def _validation_error_message(errors: list[dict[str, Any]]) -> str:
    err = errors[0]
    loc = err.get("loc") or ()
    field: str | None = None
    for part in reversed(loc):
        if isinstance(part, str) and part not in _SKIP_LOC:
            field = part
            break

    if err.get("type") == "missing" and field is not None:
        return f"{field} is required"

    ctx = err.get("ctx") or {}
    inner = ctx.get("error")
    if isinstance(inner, Exception):
        return str(inner)

    msg = err.get("msg") or "Validation error"
    prefix = "Value error, "
    if msg.startswith(prefix):
        return msg[len(prefix) :]
    return msg


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(_request: Request, exc: AppException) -> JSONResponse:
        body = error_response(
            message=exc.message,
            status_code=exc.status_code,
            data=None,
        )
        return JSONResponse(status_code=exc.status_code, content=body)

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        _request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        detail = exc.detail
        if isinstance(detail, list):
            message = "Request could not be processed"
        else:
            message = str(detail)
        body = error_response(message=message, status_code=exc.status_code, data={})
        return JSONResponse(status_code=exc.status_code, content=body)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        body = error_response(
            message=_validation_error_message(exc.errors()),
            status_code=400,
            data={},
        )
        return JSONResponse(status_code=400, content=body)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_request: Request, _exc: Exception) -> JSONResponse:
        body = error_response(
            message="An unexpected error occurred",
            status_code=500,
            data=None,
        )
        return JSONResponse(status_code=500, content=body)
