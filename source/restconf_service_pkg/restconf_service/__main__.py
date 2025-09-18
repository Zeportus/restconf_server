import argparse

import uvicorn
from restconf_service.api.app_factory import create_app
from restconf_service.rpc_handlers.rpc_handler_provider import RpcHandlerProvider
from restconf_service.yang_manager.storage.yang_config_storage.yang_config_storage_fs import YangConfigStorageFS
from restconf_service.yang_manager.storage.yang_library_storage.yang_library_storage_fs import YangLibraryStorageFS
from restconf_service.settings.server_settings import ServerSettings
from restconf_service.yang_manager.yang_manager import YangManager
from restconf_service.restconf_service import RestconfService


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--config-path', help='Path to server config')

    args = parser.parse_args()

    server_settings = ServerSettings(_env_file=args.config_path)

    library_storage = YangLibraryStorageFS(
        yang_library_path=server_settings.yang_library_path,
        yang_modules_dir_path=server_settings.yang_modules_dir_path,
    )
    config_storage = YangConfigStorageFS(
        yang_config_path=server_settings.yang_config_path,
    )
    yang_manager = YangManager(
        library_storage=library_storage,
        config_storage=config_storage,
    )

    yang_manager.validate_config()

    service = RestconfService(
        yang_manager=yang_manager,
        rpc_handler_provider=RpcHandlerProvider(),
    )

    app = create_app(service=service)

    uvicorn.run(
        app=app,
        host=server_settings.server_host,
        port=server_settings.server_port,
    )


main()
