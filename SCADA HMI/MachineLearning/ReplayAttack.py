from GUI.DetectionLabel import DetectionLabel
from MachineLearning.DetectedState import DetectedState


class ReplayAttack(DetectedState):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "REPLAY ATTACK"

    def update(self, label: DetectionLabel):
        label.abnormal_state(self.__str__())