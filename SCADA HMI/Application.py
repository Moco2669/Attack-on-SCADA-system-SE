import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication
from Connection import ConnectionHandler
from Acquisition import Executor
from DataBase import DataBase
from GUI import CustomWindow
from GUI.CustomWindow import MainWindow
from mlModel import MachineLearningModel


class Application:
    def __init__(self):
        self.q_app : QCoreApplication | None = QApplication.instance()
        if self.q_app is None:
            self.q_app = QApplication(sys.argv)
        self.database : DataBase = DataBase()
        self.connection_handler : ConnectionHandler = ConnectionHandler(self.database)
        self.executor : Executor = Executor(self.database, self.connection_handler)
        self.security_model : MachineLearningModel = MachineLearningModel(self.database, self.connection_handler)
        self.main_window : MainWindow = CustomWindow.MainWindow(self.database, self.connection_handler)

    def stop(self):
        self.main_window.close()


if __name__ == "__main__":
    app = Application()
    sys.exit(app.q_app.exec_())