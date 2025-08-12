from GUI.StatusBarLabel import StatusBarLabel


class ConnectionLabel(StatusBarLabel):
    def __init__(self):
        super().__init__()

    def disconnected(self):
        self.setText("DISCONNECTED")
        self.setStyleSheet("background-color: red")

    def connected(self):
        self.setText("CONNECTED")
        self.setStyleSheet("background-color: green")