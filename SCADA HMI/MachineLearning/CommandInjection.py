from MachineLearning.DetectedState import DetectedState


class CommandInjection(DetectedState):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "COMMAND INJECTION"

    def update(self, label):
        label.abnormal_state(self.__str__())