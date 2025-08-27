from PyQt5.QtCore import QTimer


class UpdateTimer(QTimer):
    def __init__(self, main_window, callback):
        super().__init__(main_window)
        self.callback = callback
        self.timeout.connect(self.callback)

    def start(self, interval = 350):
        super().start(interval)

    def close(self):
        self.timeout.disconnect(self.callback)
        self.stop()
        self.deleteLater()