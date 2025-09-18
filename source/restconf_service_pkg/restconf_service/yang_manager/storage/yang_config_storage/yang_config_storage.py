from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Iterator


class YangConfigStorage(ABC):
    @abstractmethod
    def get_config(self) -> dict:
        ...

    @abstractmethod
    def update_config(self, new_config: dict) -> None:
        ...

    @abstractmethod
    @contextmanager
    def lock_config(self) -> Iterator[None]:
        ...
