import json
from json import JSONDecodeError
from typing import Any

from fastapi import Header, Depends
from restconf_service.api.constants import RestconfHeader, RestconfErrorType, RestconfErrorTag
from restconf_service.api.exceptions.exceptions import RestconfHTTPException
from starlette.requests import Request
from starlette.responses import Response


def get_accept_header(
    accept: str = Header(default=RestconfHeader.YANG_DATA_JSON.value),
) -> RestconfHeader | Response:
    try:
        return RestconfHeader(accept)
    except ValueError:
        raise RestconfHTTPException(
            status_code=406,
            error_type=RestconfErrorType.PROTOCOL,
            error_tag=RestconfErrorTag.INVALID_VALUE,
            error_message='Not supported Accept',
            media_type=RestconfHeader.YANG_DATA_JSON,
        )


def get_content_type_header(
    accept: RestconfHeader = Depends(get_accept_header),
    content_type: str = Header(default=RestconfHeader.YANG_DATA_JSON.value),
) -> RestconfHeader | Response:
    try:
        return RestconfHeader(content_type)
    except ValueError:
        raise RestconfHTTPException(
            status_code=406,
            error_type=RestconfErrorType.PROTOCOL,
            error_tag=RestconfErrorTag.INVALID_VALUE,
            error_message='Not supported Content-Type',
            media_type=accept,
        )


async def get_body_by_content_type(
    request: Request,
    accept: RestconfHeader = Depends(get_accept_header),
    content_type: RestconfHeader = Depends(get_content_type_header),
) -> Any:
    body = await request.body()
    if not body:
        raise RestconfHTTPException(
            status_code=400,
            error_type=RestconfErrorType.PROTOCOL,
            error_tag=RestconfErrorTag.INVALID_VALUE,
            error_message='Empty body',
            media_type=accept,
        )

    if content_type == RestconfHeader.YANG_DATA_JSON:
        try:
            return json.loads(body)
        except (TypeError, JSONDecodeError):
            raise RestconfHTTPException(
                status_code=400,
                error_type=RestconfErrorType.PROTOCOL,
                error_tag=RestconfErrorTag.MALFORMED_MESSAGE,
                error_message='Malformed JSON body',
                media_type=accept,
            )
