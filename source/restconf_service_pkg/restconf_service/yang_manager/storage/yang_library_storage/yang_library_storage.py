from abc import ABC, abstractmethod

from yangson import DataModel


class YangLibraryStorage(ABC):
    @abstractmethod
    def get_datamodel(self) -> DataModel:
        ...
