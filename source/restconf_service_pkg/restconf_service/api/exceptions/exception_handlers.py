import logging

from restconf_service.api.constants import RestconfHeader, RestconfErrorType, RestconfErrorTag
from restconf_service.api.exceptions.exceptions import RestconfHTTPException
from restconf_service.api.request_helper import get_accept_header
from restconf_service.api.response_factory import create_error_response
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger()


def restconf_http_exception_handler(
    request: Request,
    exc: RestconfHTTPException
) -> Response:
    return create_error_response(
        status_code=exc.status_code,
        error_type=exc.error_type,
        error_tag=exc.error_tag,
        error_path=request.path_params.get('resource_path'),
        error_message=exc.error_message,
        media_type=exc.media_type,
    )


def http_exception_handler(
    request: Request,
    exc: HTTPException
) -> Response:
    accept_header = request.headers.get('accept')
    if not accept_header:
        accept = RestconfHeader.YANG_DATA_JSON
    else:
        try:
            accept = get_accept_header(accept_header)
        except RestconfHTTPException as err:
            return restconf_http_exception_handler(request, err)

    return create_error_response(
        status_code=exc.status_code,
        error_type=RestconfErrorType.PROTOCOL,
        error_tag=RestconfErrorTag.OPERATION_FAILED,
        error_path=request.path_params.get('resource_path'),
        error_message=exc.detail,
        media_type=accept,
    )


def all_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(exc)
    accept_header = request.headers.get('accept')
    if not accept_header:
        accept = RestconfHeader.YANG_DATA_JSON
    else:
        try:
            accept = get_accept_header(accept_header)
        except RestconfHTTPException as err:
            return restconf_http_exception_handler(request, err)

    return create_error_response(
        status_code=500,
        error_type=RestconfErrorType.APPLICATION,
        error_tag=RestconfErrorTag.OPERATION_FAILED,
        error_path=request.path_params.get('resource_path'),
        error_message='Internal Server Error',
        media_type=accept,
    )