from PyQt5.QtCore import pyqtSignal
from Connection.ConnectionStatus import ConnectionStatus
from GUI.StatusBarLabel import StatusBarLabel


class ConnectionLabel(StatusBarLabel):
    update_signal = pyqtSignal(ConnectionStatus)
    def __init__(self):
        super().__init__()
        self.disconnected()
        self.update_signal.connect(self.handle_update)

    def handle_update(self, status: ConnectionStatus):
        status.update_label(self)

    def disconnected(self):
        self.setText("DISCONNECTED")
        self.setStyleSheet("background-color: red")

    def connected(self):
        self.setText("CONNECTED")
        self.setStyleSheet("background-color: green")