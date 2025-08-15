import sys
import threading
from PyQt5.QtWidgets import QApplication
from Connection import ConnectionHandler
from Acquisition import Executor
from DataBase import DataBase
from GUI import CustomWindow
from mlModel import MachineLearningModel


class Application:
    def __init__(self):
        self.q_app = None
        self.database = None
        self.executor = None
        self.connection_handler = None
        self.security_model = None
        self.main_window = None
        self.connection_thread = None
        self.security_thread = None
        self.run()

    def run(self):
        self.database = DataBase()
        self.connection_handler = ConnectionHandler(self.database)
        self.executor = Executor(self.database, self.connection_handler)
        self.security_model = MachineLearningModel(self.database, self.connection_handler)
        self.q_app = QApplication.instance()
        if self.q_app is None:
            self.q_app = QApplication(sys.argv)
        self.main_window = CustomWindow.MainWindow(self.database, self.connection_handler)

    def stop(self):
        #self.q_app.quit()
        self.main_window.close()
        self.database.stop()
        self.connection_handler.stop()
        self.executor.stop()
        self.security_model.stop()


if __name__ == "__main__":
    app = Application()
    sys.exit(app.q_app.exec_())