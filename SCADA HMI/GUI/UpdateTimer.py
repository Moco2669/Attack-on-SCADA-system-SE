from PyQt5.QtCore import QTimer


class UpdateTimer(QTimer):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.timeout.connect(main_window.update_gui)
