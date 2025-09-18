import json
from contextlib import contextmanager
from pathlib import Path
from threading import Lock
from typing import Iterator

from restconf_service.yang_manager.storage.yang_config_storage.yang_config_storage import YangConfigStorage


class YangConfigStorageFS(YangConfigStorage):
    def __init__(
        self,
        yang_config_path: Path,
    ):
        self._yang_config_path = yang_config_path
        self._config_lock = Lock()

    def get_config(self) -> dict:
        if not self._yang_config_path.exists():
            return {}

        return json.loads(self._yang_config_path.read_text())

    def update_config(self, new_config: dict) -> None:
        if not self._yang_config_path.exists():
            self._yang_config_path.touch()

        self._yang_config_path.write_text(json.dumps(new_config))

    @contextmanager
    def lock_config(self) -> Iterator[None]:
        with self._config_lock:
            yield
