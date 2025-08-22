from Connection.ConnectionStatus import ConnectionStatus
from GUI.ConnectionLabel import ConnectionLabel


class Disconnected(ConnectionStatus):
    def __init__(self):
        super().__init__()

    def __bool__(self):
        return False

    @staticmethod
    def update_label(label: ConnectionLabel):
        label.disconnected()

    @staticmethod
    def as_event():
        return "scada_disconnected"