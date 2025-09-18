from fastapi import FastAPI
from restconf_service.api.exceptions.exception_handlers import restconf_http_exception_handler, http_exception_handler, \
    all_exception_handler
from restconf_service.api.exceptions.exceptions import RestconfHTTPException
from restconf_service.api.routers.data import DataRouter
from restconf_service.api.routers.operations import OperationsRouter
from restconf_service.restconf_service import RestconfService
from starlette.requests import HTTPException


def create_app(
    service: RestconfService,
) -> FastAPI:
    app = FastAPI(root_path='/restconf')

    app.add_exception_handler(RestconfHTTPException, restconf_http_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, all_exception_handler)

    app.include_router(DataRouter(
        service=service,
    ))
    app.include_router(OperationsRouter(
        service=service,
    ))

    return app
