from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem


class RegisterTable(QTableWidget):
    def __init__(self):
        super().__init__(0, 5)
        self.setHorizontalHeaderLabels(["Register Name", "Register Type", "Starting Address", " Signal Value", "Alarm"])
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        table_height = int(screen_geometry.height() * 0.7)
        self.setGeometry(0, 0, screen_geometry.width(), table_height)
        for col in range(self.columnCount()):
            self.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)

    def set_data(self, data):
        self.setRowCount(len(data))
        for row, (register_name, register_type, starting_address, signal_value, alarm) in enumerate(data):
            self.setItem(row, 0, QTableWidgetItem(register_name))
            self.setItem(row, 1, QTableWidgetItem(register_type))
            self.setItem(row, 2, QTableWidgetItem(starting_address))
            self.setItem(row, 3, QTableWidgetItem(signal_value))
            self.setItem(row, 4, QTableWidgetItem(alarm))
