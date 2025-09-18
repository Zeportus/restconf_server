from dataclasses import dataclass
from typing import Callable, Any

from pydantic import BaseModel
from restconf_service.rpc_handlers import jukebox_rpc_handler_stub
from restconf_service.rpc_handlers.jukebox_rpc_handler_stub import PlayArgs


@dataclass
class RpcHandlerInfo:
    rpc_handler: Callable[..., dict | None]
    rpc_handler_args_model: type[BaseModel]


class RpcHandlerProvider:
    RPC_HANDLERS_MAP: dict[str, RpcHandlerInfo] = {
        'example-jukebox:play': RpcHandlerInfo(
            rpc_handler=jukebox_rpc_handler_stub.play,
            rpc_handler_args_model=PlayArgs
        ),
    }

    @classmethod
    def get_rpc_handler_info(cls, operation: str) -> RpcHandlerInfo | None:
        return cls.RPC_HANDLERS_MAP.get(operation)
