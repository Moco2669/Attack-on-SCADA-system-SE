import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from Acquisition import *
import threading
import Connection
from GUI.ConnectionLabel import ConnectionLabel
from GUI.DetectionLabel import DetectionLabel
from GUI.RegisterTable import RegisterTable
from GUI.UpdateTimer import UpdateTimer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
        data = get_rows_for_print(registers)
        self.table.set_data(data)

    def update_status_bar(self):
        if Connection.ConnectionHandler.isConnected:
            self.connectionStatusLabel.connected()
        else:
            self.connectionStatusLabel.disconnected()
        if StateHolder.state in ("COMMAND INJECTION", "REPLAY ATTACK"):
            self.attackDetectionLabel.abnormal_state(StateHolder.state)
        else:
            self.attackDetectionLabel.normal_state(StateHolder.state)

    def closeEvent(self, event):
        Connection.ConnectionHandler.client.close()
        Connection.ConnectionHandler.isRunning = False
        Connection.ConnectionHandler.isConnected = False
        with Connection.ConnectionHandler.connection_lock:
            Connection.ConnectionHandler.lostConnection.notify_all()
            Connection.ConnectionHandler.connected.notify_all()
        self.updateTimer.timeout.disconnect(self.update_gui)
        self.updateTimer.stop()
        self.close()
        event.accept()


def main():
    Connection.ConnectionHandler.isRunning = True
    app = QApplication(sys.argv)
    ex = MainWindow()
    acquisition_thread = threading.Thread(target=Acquisition, args=(base_info, registers))
    acquisition_thread.daemon = True  # koristi se za niti koje rade u pozadini
    acquisition_thread.start()
    connect_thr = threading.Thread(target=Connection.connect_thread, args=(base_info, 1))
    connect_thr.daemon = True
    connect_thr.start()
    # acquisition_thread.join()
    # connect_thr.join()
    sys.exit(app.exec_())

def main2():
    Connection.ConnectionHandler.isRunning = True
    acquisition_thread = threading.Thread(target=Acquisition, args=(base_info, registers))
    acquisition_thread.daemon = True
    acquisition_thread.start()
    connect_thr = threading.Thread(target=Connection.connect_thread, args=(base_info, 1))
    connect_thr.daemon = True
    connect_thr.start()
    input("Press Enter to exit...")
    Connection.ConnectionHandler.client.close()
    Connection.ConnectionHandler.isRunning = False
    acquisition_thread.join()
    connect_thr.join()