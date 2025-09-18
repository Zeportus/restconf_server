from dataclasses import dataclass

from restconf_service.api.constants import RestconfErrorType, RestconfErrorTag

from restconf_service.exceptions import RestconfException, NotFound, InvalidValue, UnknownElement, \
    OperationNotSupported, BadElement


@dataclass
class HttpErrorData:
    status_code: int
    error_type: RestconfErrorType
    error_tag: RestconfErrorTag


HTTP_ERROR_DATA_MAP: dict[type[RestconfException], HttpErrorData] = {
    NotFound: HttpErrorData(status_code=404,
                            error_type=RestconfErrorType.PROTOCOL,
                            error_tag=RestconfErrorTag.INVALID_VALUE),
    InvalidValue: HttpErrorData(status_code=400,
                                error_type=RestconfErrorType.PROTOCOL,
                                error_tag=RestconfErrorTag.INVALID_VALUE),
    UnknownElement: HttpErrorData(status_code=400,
                                  error_type=RestconfErrorType.PROTOCOL,
                                  error_tag=RestconfErrorTag.UNKNOWN_ELEMENT),
    OperationNotSupported: HttpErrorData(status_code=405,
                                         error_type=RestconfErrorType.PROTOCOL,
                                         error_tag=RestconfErrorTag.OPERATION_NOT_SUPPORTED),
    BadElement: HttpErrorData(status_code=400,
                              error_type=RestconfErrorType.PROTOCOL,
                              error_tag=RestconfErrorTag.BAD_ELEMENT),
}
