from abc import ABC, abstractmethod


class ConnectionStatus(ABC):
    def __init__(self):
        return

    @abstractmethod
    def __bool__(self):
        pass

    @staticmethod
    @abstractmethod
    def update_label(label) -> None:
        pass

    @staticmethod
    @abstractmethod
    def as_event() -> str:
        pass