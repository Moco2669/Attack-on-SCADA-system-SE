from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from Connection.ConnectionStatus import ConnectionStatus
from DataBase import DataBase
from GUI.ConnectionLabel import ConnectionLabel
from GUI.DetectionLabel import DetectionLabel
from GUI.RegisterTable import RegisterTable
from GUI.UpdateTimer import UpdateTimer
from MachineLearning.DetectedState import DetectedState


class MainWindow(QMainWindow):
    def __init__(self, database : DataBase):
        super().__init__()
        self.database = database
        self.table = RegisterTable()
        self.connectionStatusLabel = ConnectionLabel()
        self.attackDetectionLabel = DetectionLabel()
        self.setup_handlers()
        self.init_ui()

    def setup_handlers(self):
        @self.database.event("connection_update")
        def handle_update_connection(new_status: ConnectionStatus):
            self.connectionStatusLabel.update_signal.emit(new_status)

        @self.database.event("system_state_update")
        def handle_update_system_state(new_state: DetectedState):
            self.attackDetectionLabel.update_signal.emit(new_state)

        @self.database.event("registers_update")
        def handle_update_registers(registers):
            rows = self.table.rows_from(registers)
            self.table.update_data_signal.emit(rows)

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

        self.show()

    def closeEvent(self, event):
        self.database.stop()
        event.accept()
