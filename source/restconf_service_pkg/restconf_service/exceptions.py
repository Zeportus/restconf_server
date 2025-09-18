from dataclasses import dataclass

from yangson.exceptions import YangsonException, NonexistentSchemaNode, RawTypeError, ValidationError, NonDataNode, \
    NonexistentInstance, RawMemberError, UnexpectedInput


@dataclass
class RPCInfo:
    is_output: bool


class RestconfException(Exception):
    def __init__(self, *args, rpc_info: RPCInfo | None = None):
        super().__init__(*args)
        self.rpc_info = rpc_info


class InvalidValue(RestconfException):
    ...


class NotFound(RestconfException):
    ...


class UnknownElement(RestconfException):
    ...


class OperationNotSupported(RestconfException):
    ...


class BadElement(RestconfException):
    ...


@dataclass
class RestconfExceptionData:
    exc_type: type[RestconfException]
    message: str | None = None
    use_message: bool = False


RESTCONF_EXCEPTIONS_MAP: dict[type[YangsonException], RestconfExceptionData] = {
    NonexistentSchemaNode: RestconfExceptionData(
        exc_type=UnknownElement,
        message='A schema node doesn’t exist.',
    ),
    RawMemberError: RestconfExceptionData(
        exc_type=UnknownElement,
        message='Object member doesn’t exist in the schema'
    ),

    NonexistentInstance: RestconfExceptionData(
        exc_type=NotFound,
        message='Attempt to access an instance node that doesn’t exist'
    ),

    NonDataNode: RestconfExceptionData(
        exc_type=OperationNotSupported,
        message='Attempt to access an instance of non-data node (rpc/action/notification)'
    ),

    RawTypeError: RestconfExceptionData(
        exc_type=InvalidValue,
        use_message=True,
    ),
    ValidationError: RestconfExceptionData(
        exc_type=InvalidValue,
        use_message=True,
    ),

    UnexpectedInput: RestconfExceptionData(
        exc_type=BadElement,
    ),
}

def create_restconf_exc(exc: YangsonException, rpc_info: RPCInfo | None = None) -> RestconfException:
    for yangson_exc_type, restconf_exc_data in RESTCONF_EXCEPTIONS_MAP.items():
        if isinstance(exc, yangson_exc_type):
            if restconf_exc_data.message:
                return restconf_exc_data.exc_type(restconf_exc_data.message, rpc_info=rpc_info)
            if restconf_exc_data.use_message:
                return restconf_exc_data.exc_type(exc.message, rpc_info=rpc_info)
            return restconf_exc_data.exc_type(str(exc), rpc_info=rpc_info)

    raise RuntimeError(f'Unexpected yangson exception: {type(exc)}: {exc}')
