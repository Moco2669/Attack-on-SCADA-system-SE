import sys
from turtledemo.clock import setup

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout, QWidget,QDesktopWidget
import Connection
from DataBase import *
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel, QWidget, QHBoxLayout
from PyQt5.QtGui import QGuiApplication, QFont
from PyQt5.QtCore import Qt, QTimer, QDateTime, QTimeZone,pyqtSignal,QObject
from Connection import *
import socket
from Acquisition import *
import threading
import Connection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tableWidget = None
        self.initUI()

    def setUpWindow(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('SCADA-HMI')

    def centralWidgetWith(self, layout):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_widget.setLayout(layout)
        return central_widget

    def makeTable(self):
        table = QTableWidget(0, 5)
        table.setHorizontalHeaderLabels(["Name", "Type", "Address", "Value", "Alarm"])
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        table_height = int(screen_geometry.height() * 0.7)
        table.setGeometry(0, 0, screen_geometry.width(), table_height)
        for col in range(table.columnCount()):
            table.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)
        return table

    def layoutWith(self, table):
        layout = QVBoxLayout()
        layout.addWidget(table)
        return layout

    def initUI(self):
        self.setUpWindow()
        self.tableWidget = self.makeTable()
        layout = self.layoutWith(self.tableWidget)
        central_widget = self.centralWidgetWith(layout)



        # Create a QHBoxLayout to place the "CONNECTED" connectionStatusLabel and the time connectionStatusLabel side by side
        hbox = QHBoxLayout()

        # Create the "CONNECTED" connectionStatusLabel
        self.connectionStatusLabel = QLabel("CONNECTED")
        self.attackDetectionLabel = QLabel(f"STATE OF SYSTEM:{StateHolder.state}")
        self.attackDetectionLabel.setFont(QFont("Helvetica", 10, QFont.Bold))
        self.connectionStatusLabel.setFont(QFont("Helvetica", 10, QFont.Bold))
        self.connectionStatusLabel.setAlignment(Qt.AlignCenter)
        self.attackDetectionLabel.setAlignment(Qt.AlignCenter)
        # Set a fixed height for the connectionStatusLabel
        self.connectionStatusLabel.setFixedHeight(30)
        hbox.addWidget(self.connectionStatusLabel)
        hbox.addWidget(self.attackDetectionLabel)

        layout.addLayout(hbox)

        # okida na svake 0.5 sek update tabele
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTable)
        self.timer.start(500)

        self.show()

    def updateTable(self):
        #print(StateHolder.state)
        if Connection.ConnectionHandler.isConnected:
            self.connectionStatusLabel.setStyleSheet("background-color: green;")
        else:
            self.connectionStatusLabel.setStyleSheet("background-color: red")

        if StateHolder.state in ("COMMAND INJECTION", "REPLAY ATTACK"):
            self.attackDetectionLabel.setStyleSheet("background-color: red")
            self.attackDetectionLabel.setText(f"STATE OF SYSTEM: {StateHolder.state}")
        else:
            self.attackDetectionLabel.setStyleSheet("background-color: green;")
            self.attackDetectionLabel.setText(f"STATE OF SYSTEM: {StateHolder.state}")

        tuples = makeTuplesForPrint(signal_info)  # fresh info
        data = list()
        data.extend(tuples)
        self.tableWidget.setRowCount(0)  # brise poslednje podatke
        for row, item in enumerate(data):  # update
            self.tableWidget.insertRow(row)
            for col, text in enumerate(item):
                # self.tableWidget.setItem(row, col, QTableWidgetItem(text))
                item_widget = QTableWidgetItem(text)
                if text == "HIGH ALARM":
                    # Set the text color to red
                    item_widget.setForeground(QColor(255, 0, 0))  # Red color

                    # Set the font to bold
                    font = QFont()
                    font.setBold(True)
                    item_widget.setFont(font)
                    self.tableWidget.setItem(row, col, item_widget)
                elif text == "LOW ALARM":
                    item_widget.setForeground(QColor(255, 0, 0))  # Red color

                    # Set the font to bold
                    font = QFont()
                    font.setBold(True)
                    item_widget.setFont(font)
                    self.tableWidget.setItem(row, col, item_widget)
                else:
                    item_widget.setForeground(QColor(0, 0, 0))
                    font = QFont()
                    font.setBold(False)
                    item_widget.setFont(font)
                    self.tableWidget.setItem(row, col, item_widget)

    def closeEvent(self, event):
        Connection.ConnectionHandler.client.close()
        Connection.ConnectionHandler.isRunning = False


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

if __name__ == '__main__':
    main()