from MachineLearning.DetectedState import DetectedState


class FindingState(DetectedState):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "FINDING STATE"

    def update(self, label):
        label.normal_state(self.__str__())