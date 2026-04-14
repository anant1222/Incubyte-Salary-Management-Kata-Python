from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

import app.models  # noqa: F401

from app.core.error_handlers import register_error_handlers
from app.db.database import Base, engine
from app.routes import employee_routes, health_routes


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(bind=engine)
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Salary Management API",
        version="0.1.0",
        lifespan=lifespan,
    )
    register_error_handlers(app)
    app.include_router(health_routes.router)
    app.include_router(employee_routes.router)
    return app


app = create_app()
