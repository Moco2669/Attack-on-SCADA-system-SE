from PyQt5.QtGui import QGuiApplication, QFont, QColor
from PyQt5.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem
from GUI.TableRow import TableRow


class RegisterTable(QTableWidget):
    def __init__(self):
        super().__init__(0, 5)
        self.setHorizontalHeaderLabels(["Register Name", "Register Type", "Starting Address", " Signal Value", "Alarm"])
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        for col in range(self.columnCount()):
            self.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)

    def set_data(self, rows : list[TableRow]):
        self.setRowCount(len(rows))
        for row in range(len(rows)):
            for column in range(rows[row].num_of_fields):
                self.setItem(row, column, rows[row].table_items[column])
