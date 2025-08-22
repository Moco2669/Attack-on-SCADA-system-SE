from Connection.ConnectionStatus import ConnectionStatus
from GUI.ConnectionLabel import ConnectionLabel


class Connected(ConnectionStatus):
    def __init__(self):
        super().__init__()

    def __bool__(self):
        return True

    @staticmethod
    def update_label(label: ConnectionLabel):
        label.connected()

    @staticmethod
    def as_event():
        return "scada_connected"