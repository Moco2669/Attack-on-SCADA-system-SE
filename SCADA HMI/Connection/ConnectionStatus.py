from abc import ABC, abstractmethod
from GUI.ConnectionLabel import ConnectionLabel


class ConnectionStatus(ABC):
    def __init__(self):
        return

    @abstractmethod
    def __bool__(self):
        pass

    @staticmethod
    @abstractmethod
    def update_label(label: ConnectionLabel) -> None:
        pass

    @staticmethod
    @abstractmethod
    def as_event() -> str:
        pass