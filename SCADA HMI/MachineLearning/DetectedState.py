from abc import ABC, abstractmethod


class DetectedState(ABC):
    def __init__(self):
        return

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def update(self, label):
        pass