from PyQt5.QtCore import pyqtSignal
from GUI.StatusBarLabel import StatusBarLabel
from MachineLearning.DetectedState import DetectedState


class DetectionLabel(StatusBarLabel):
    update_signal = pyqtSignal(DetectedState)
    def __init__(self):
        super().__init__()
        self.normal_state("FINDING STATE")
        self.update_signal.connect(self.handle_update)

    def handle_update(self, state: DetectedState):
        state.update(self)

    def abnormal_state(self, state):
        self.setStyleSheet("background-color: red")
        self.setText(f"STATE OF SYSTEM: {state}")

    def normal_state(self, state):
        self.setStyleSheet("background-color: green")
        self.setText(f"STATE OF SYSTEM: {state}")