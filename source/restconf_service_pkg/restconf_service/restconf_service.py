from typing import Any

from restconf_service.exceptions import create_restconf_exc, RPCInfo
from restconf_service.rpc_handlers.rpc_handler_provider import RpcHandlerProvider
from restconf_service.yang_manager.yang_manager import YangManager
from yangson.exceptions import YangsonException
from yangson.typealiases import RawValue


class RestconfService:
    def __init__(
        self,
        yang_manager: YangManager,
        rpc_handler_provider: RpcHandlerProvider,
    ):
        self._yang_manager = yang_manager
        self._rpc_handler_provider = rpc_handler_provider

    def get_resource(self, path: str) -> RawValue:
        try:
            return self._yang_manager.get_node_value(path)
        except YangsonException as err:
            raise create_restconf_exc(err)

    def update_resource(
        self,
        path: str,
        value: RawValue,
    ) -> None:
        try:
            self._yang_manager.update_node_value(path, value)
        except YangsonException as err:
            raise create_restconf_exc(err)

    def process_operation(
        self,
        operation: str,
        input_kwargs: dict[str, dict[str, Any]] | None = None,
    ) -> dict | None:
        self._validate_rpc_and_handle_error(
            operation=operation,
            kwargs=input_kwargs,
        )

        input_field_name = 'input'
        operation_kwargs = input_kwargs.get(input_field_name)
        if not operation_kwargs:
            module_name = operation.split(':')[0]
            input_field_name = f'{module_name}:{input_field_name}'
            operation_kwargs = input_kwargs[input_field_name]

        rpc_handler_info = self._rpc_handler_provider.get_rpc_handler_info(operation)
        rpc_handler_args = rpc_handler_info.rpc_handler_args_model.model_validate(operation_kwargs)
        rpc_output = rpc_handler_info.rpc_handler(rpc_handler_args)

        if not rpc_output is None:
            self._validate_rpc_and_handle_error(
                operation=operation,
                kwargs={'output': rpc_output}
            )

        return rpc_output

    def _validate_rpc_and_handle_error(
        self,
        operation: str,
        kwargs: dict[str, dict[str, Any]]
    ) -> None:
        rpc_info = RPCInfo(
            is_output='output' in kwargs,
        )

        try:
            self._yang_manager.validate_rpc(
                operation=operation,
                kwargs=kwargs,
            )
        except YangsonException as err:
            raise create_restconf_exc(err, rpc_info)