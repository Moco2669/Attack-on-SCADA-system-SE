from PyQt5.QtCore import QTimer


class UpdateTimer(QTimer):
    def __init__(self, main_window, function):
        super().__init__(main_window)
        self.timeout.connect(function)
