import time
from os import getenv as env

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response

from service.log import access_logger, app_logger
from service.models import Error
from service.response import access_error, server_error

API_KEY = env("API_KEY", "default_api_key")


class AccessMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        started_at = time.perf_counter()
        response = await call_next(request)
        request_time = time.perf_counter() - started_at

        status_code = response.status_code

        access_logger.info(
            msg="",
            extra={
                "request_time": round(request_time, 4),
                "status_code": status_code,
                "requested_url": request.url,
                "method": request.method,
            },
        )
        return response


class AuthorizationMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        user_api_key = request.headers.get("api-key")

        if user_api_key != API_KEY or user_api_key is None:
            error = Error(error_key="server_error", error_message="Invalid Api-Key")
            return access_error([error])

        return await call_next(request)


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        try:
            return await call_next(request)
        except Exception as e:  # pylint: disable=W0703,W1203
            app_logger.exception(msg=f"Caught unhandled {e.__class__} exception: {e}")
            error = Error(error_key="server_error", error_message="Internal Server Error")
            return server_error([error])


def add_middlewares(app: FastAPI) -> None:
    app.add_middleware(AuthorizationMiddleware)
    app.add_middleware(ExceptionHandlerMiddleware)
    app.add_middleware(AccessMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
