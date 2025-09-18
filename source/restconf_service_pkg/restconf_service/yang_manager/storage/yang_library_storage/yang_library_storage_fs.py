from pathlib import Path

from restconf_service.yang_manager.storage.yang_library_storage.yang_library_storage import YangLibraryStorage
from yangson import DataModel


class YangLibraryStorageFS(YangLibraryStorage):
    def __init__(
        self,
        yang_library_path: Path,
        yang_modules_dir_path: Path,
    ):
        self._yang_library_path = yang_library_path
        self._yang_modules_dir_path = yang_modules_dir_path

    def get_datamodel(self) -> DataModel:
        return DataModel.from_file(
            name=str(self._yang_library_path),
            mod_path=(str(self._yang_modules_dir_path), ),
        )
