from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel


class StatusBarLabel(QLabel):
    def __init__(self):
        super().__init__("")
        self.setFont(QFont("Helvetica", 10, QFont.Bold))
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(30)