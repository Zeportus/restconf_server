from restconf_service.api.constants import RestconfHeader, RestconfErrorType, RestconfErrorTag


class RestconfHTTPException(Exception):
    def __init__(
        self,
        status_code: int,
        media_type: RestconfHeader,
        error_type: RestconfErrorType,
        error_tag: RestconfErrorTag,
        error_message: str,
    ):
        self.status_code = status_code
        self.media_type = media_type
        self.error_type = error_type
        self.error_tag = error_tag
        self.error_message = error_message
