from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QTableWidget, QHeaderView


class RegisterTable(QTableWidget):
    def __init__(self):
        super().__init__(0, 5)
        self.setHorizontalHeaderLabels(["Name", "Type", "Address", "Value", "Alarm"])
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        table_height = int(screen_geometry.height() * 0.7)
        self.setGeometry(0, 0, screen_geometry.width(), table_height)
        for col in range(self.columnCount()):
            self.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)
