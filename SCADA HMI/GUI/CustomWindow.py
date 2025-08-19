from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from DataBase import DataBase
from Connection import ConnectionHandler
from GUI.ConnectionLabel import ConnectionLabel
from GUI.DetectionLabel import DetectionLabel
from GUI.RegisterTable import RegisterTable
from GUI.UpdateTimer import UpdateTimer


class MainWindow(QMainWindow):
    def __init__(self, database : DataBase, connection: ConnectionHandler):
        super().__init__()
        self.database = database
        self.connection = connection
        self.table = RegisterTable()
        self.connectionStatusLabel = ConnectionLabel()
        self.attackDetectionLabel = DetectionLabel()
        self.updateTimer = UpdateTimer(self)
        self.init_ui()

    def set_up_window(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('SCADA-HMI')

    def make_central_widget_with(self, layout):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_widget.setLayout(layout)
        return central_widget

    def make_status_bar(self):
        status_bar = QHBoxLayout()
        status_bar.addWidget(self.connectionStatusLabel)
        status_bar.addWidget(self.attackDetectionLabel)
        return status_bar

    def make_layout_with(self, status_bar):
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(status_bar)
        return layout

    def init_ui(self):
        self.set_up_window()
        layout = self.make_layout_with(self.make_status_bar())
        self.make_central_widget_with(layout)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.updateTimer.start(500)

        self.show()

    def update_gui(self):
        self.update_status_bar()
        self.update_table()

    def update_table(self):
        data = self.database.get_rows_for_print()
        self.table.set_data(data)

    def update_status_bar(self):
        if self.connection.isConnected:
            self.connectionStatusLabel.connected()
        else:
            self.connectionStatusLabel.disconnected()
        if self.database.system_state in ("COMMAND INJECTION", "REPLAY ATTACK"):
            self.attackDetectionLabel.abnormal_state(self.database.system_state)
        else:
            self.attackDetectionLabel.normal_state(self.database.system_state)

    def closeEvent(self, event):
        self.database.stop()
        self.updateTimer.timeout.disconnect(self.update_gui)
        self.updateTimer.stop()
        self.close()
        event.accept()
