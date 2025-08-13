import socket
import sys
import threading
from PyQt5.QtWidgets import QApplication
import Connection
from Acquisition import Executor
from DataBase import DataBase
from GUI import CustomWindow


class Application:
    def __init__(self):
        self.q_app = None
        self.database = None
        self.executor = None
        self.main_window = None
        self.acquisition_thread = None
        self.connection_thread = None
        self.run()

    def run(self):
        self.database = DataBase()
        self.executor = Executor(self.database)
        self.q_app = QApplication.instance()
        if self.q_app is None:
            self.q_app = QApplication(sys.argv)
        self.main_window = CustomWindow.MainWindow(self.database)
        Connection.ConnectionHandler.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        Connection.ConnectionHandler.isRunning = True
        self.acquisition_thread = threading.Thread(target=self.executor.AcquisitionAndAutomation)
        self.acquisition_thread.start()
        self.connection_thread = threading.Thread(target=Connection.connect_thread, args=(self.database.base_info, 1))
        self.connection_thread.start()

    def stop(self):
        #self.q_app.quit()
        self.main_window.close()
        Connection.ConnectionHandler.isRunning = False
        Connection.ConnectionHandler.isConnected = False
        with Connection.ConnectionHandler.connection_lock:
            Connection.ConnectionHandler.lostConnection.notify_all()
            Connection.ConnectionHandler.connected.notify_all()
        self.acquisition_thread.join()
        self.connection_thread.join()
        try:
            Connection.ConnectionHandler.client.close()
        except Exception as e:
            pass

if __name__ == "__main__":
    app = Application()
    sys.exit(app.q_app.exec_())