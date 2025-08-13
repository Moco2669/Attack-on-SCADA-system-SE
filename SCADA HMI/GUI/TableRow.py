from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QTableWidgetItem
from Modbus.Signal import Signal


class TableRow:
    def __init__(self, signal : Signal):
        self._fields = [
            signal.name,
            signal.signal_type_string,
            signal.start_address,
            signal.current_value,
            signal.alarm
        ]
        self._table_items = []
        for field in self._fields:
            self._table_items.append(self.table_item(field))

    @property
    def table_items(self):
        return self._table_items

    @property
    def num_of_fields(self):
        return len(self._table_items)

    @staticmethod
    def table_item(element) -> QTableWidgetItem:
        font = QFont()
        item = QTableWidgetItem(str(element))
        if element == "HIGH ALARM" or element == "LOW ALARM":
            font.setBold(True)
            item.setForeground(QColor(255, 0, 0))
        else:
            font.setBold(False)
            item.setForeground(QColor(0, 0, 0))
        item.setFont(font)
        return item