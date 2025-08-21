from GUI.DetectionLabel import DetectionLabel
from MachineLearning.DetectedState import DetectedState


class NormalState(DetectedState):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "NORMAL STATE"

    def update(self, label: DetectionLabel):
        label.normal_state(self.__str__())