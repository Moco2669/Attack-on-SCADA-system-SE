from GUI.StatusBarLabel import StatusBarLabel


class DetectionLabel(StatusBarLabel):
    def __init__(self):
        super().__init__()
        self.normal_state("FINDING STATE")

    def abnormal_state(self, state):
        self.setStyleSheet("background-color: red")
        self.setText(f"STATE OF SYSTEM: {state}")

    def normal_state(self, state):
        self.setStyleSheet("background-color: green")
        self.setText(f"STATE OF SYSTEM: {state}")