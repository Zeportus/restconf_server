from typing import Any

from restconf_service.api.constants import RestconfErrorType, RestconfErrorTag, RestconfHeader
from starlette.responses import JSONResponse, Response


def create_response(
    status_code: int,
    media_type: RestconfHeader,
    content: Any,
) -> Response:
    if media_type == RestconfHeader.YANG_DATA_JSON:
        return JSONResponse(
            status_code=status_code,
            media_type=RestconfHeader.YANG_DATA_JSON.value,
            content=content,
        )


def create_error_response(
    status_code: int,
    media_type: RestconfHeader,
    error_type: RestconfErrorType,
    error_tag: RestconfErrorTag,
    error_path: str,
    error_message: str,
) -> Response:
    error = {
        'error-type': error_type.value,
        'error-tag': error_tag.value,
        'error-message': error_message,
    }
    if error_path:
        error['error-path'] = error_path

    content = {
        'ietf-restconf:errors': {
            'error': [error]
        }
    }

    return create_response(status_code, media_type, content)
