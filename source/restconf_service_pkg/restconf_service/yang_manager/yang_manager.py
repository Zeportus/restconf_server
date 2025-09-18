from typing import Any

from restconf_service.yang_manager.storage.yang_config_storage.yang_config_storage import YangConfigStorage
from restconf_service.yang_manager.storage.yang_library_storage.yang_library_storage import YangLibraryStorage
from yangson.enumerations import ContentType
from yangson.instance import InstanceNode
from yangson.typealiases import RawValue


class YangManager:
    def __init__(
        self,
        library_storage: YangLibraryStorage,
        config_storage: YangConfigStorage,
    ):
        self._library_storage = library_storage
        self._config_storage = config_storage
        self._config_cache = None
        self._root_node = None

        self._datamodel = self._library_storage.get_datamodel()
        self._update_cache()

    def validate_config(self) -> None:
        if not self._config_cache:
            return

        self._root_node.validate(ctype=ContentType.all)

    def validate_rpc(self, operation: str, kwargs: dict[str, dict[str, Any]]) -> None:
        rpc_node = self._datamodel.from_raw(kwargs, subschema=operation)
        rpc_node.validate(ctype=ContentType.all)

    def get_node_value(self, resource_identifier: str) -> RawValue:
        return self._get_node(resource_identifier).raw_value()

    def update_node_value(self, resource_identifier: str, value: RawValue) -> None:
        with self._config_storage.lock_config():
            self._update_cache()

            node = self._get_node(resource_identifier)

            new_node = node.merge(value, raw=True)
            new_root_node = new_node.top()
            new_root_node.validate(ctype=ContentType.all)

            self._config_storage.update_config(new_root_node.raw_value())

            self._root_node = new_root_node

    def _update_cache(self) -> None:
        self._config_cache = self._config_storage.get_config()
        self._root_node = self._datamodel.from_raw(self._config_cache)

    def _get_node(self, resource_identifier: str) -> InstanceNode:
        instance_route = self._datamodel.parse_resource_id(resource_identifier)
        return self._root_node.goto(instance_route)
