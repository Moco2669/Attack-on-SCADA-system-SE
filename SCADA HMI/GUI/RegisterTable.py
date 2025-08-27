from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTableWidget, QHeaderView
from GUI.TableRow import TableRow


class RegisterTable(QTableWidget):
    update_data_signal = pyqtSignal(list)
    def __init__(self):
        super().__init__(0, 5)
        self.setHorizontalHeaderLabels(["Register Name", "Register Type", "Starting Address", " Signal Value", "Alarm"])
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        for col in range(self.columnCount()):
            self.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)
        self.update_data_signal.connect(self.set_data)

    def set_data(self, rows : list[TableRow]):
        self.clearContents()
        self.setRowCount(len(rows))
        for row in range(len(rows)):
            for column in range(rows[row].num_of_fields):
                self.setItem(row, column, rows[row].table_items[column])

    @staticmethod
    def rows_from(registers: dict) -> list[TableRow]:
        row_list = list()
        for key, signal in registers.items():
            row_list.append(TableRow(signal))
        return row_list