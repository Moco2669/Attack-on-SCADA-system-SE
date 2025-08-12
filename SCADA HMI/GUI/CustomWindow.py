import sys
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QFont
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

    def update_table(self):
        if Connection.ConnectionHandler.isConnected:
            self.connectionStatusLabel.connected()
        else:
            self.connectionStatusLabel.disconnected()

        if StateHolder.state in ("COMMAND INJECTION", "REPLAY ATTACK"):
            self.attackDetectionLabel.abnormal_state(StateHolder.state)
        else:
            self.attackDetectionLabel.normal_state(StateHolder.state)

        data = makeTuplesForPrint(signal_info)
        self.table.setRowCount(0)  # brise poslednje podatke
        font = QFont()
        for row, item in enumerate(data):  # update
            self.table.insertRow(row)
            for col, text in enumerate(item):
                item_widget = QTableWidgetItem(text)
                if text == "HIGH ALARM":
                    item_widget.setForeground(QColor(255, 0, 0))  # Red color
                    font.setBold(True)
                    item_widget.setFont(font)
                elif text == "LOW ALARM":
                    item_widget.setForeground(QColor(255, 0, 0))  # Red color
                    font.setBold(True)
                    item_widget.setFont(font)
                else:
                    item_widget.setForeground(QColor(0, 0, 0))
                    font.setBold(False)
                    item_widget.setFont(font)
                self.table.setItem(row, col, item_widget)

    def closeEvent(self, event):
        Connection.ConnectionHandler.client.close()
        Connection.ConnectionHandler.isRunning = False
        self.updateTimer.timeout.disconnect(self.update_table)
        self.updateTimer.stop()
        self.close()
        event.accept()


def main():
    Connection.ConnectionHandler.isRunning = True
    app = QApplication(sys.argv)
    ex = MainWindow()
    acquisition_thread = threading.Thread(target=Acquisition, args=(base_info, signal_info))
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
    acquisition_thread = threading.Thread(target=Acquisition, args=(base_info, signal_info))
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