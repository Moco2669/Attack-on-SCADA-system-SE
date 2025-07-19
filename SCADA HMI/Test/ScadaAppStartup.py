import socket
import sys
import threading

import Connection
import CustomWindow

from PyQt5.QtWidgets import QApplication

from Acquisition import Acquisition
from DataBase import base_info, signal_info


class ScadaAppStartup:
    def __init__(self):
        self.app = QApplication([])
        self.main_window = None
        self.acquisition_thread = None
        self.connect_thr = None

    def run(self):
        if self.app is None:
            self.app = QApplication([]) or QApplication.instance()
        self.main_window = CustomWindow.TableExample()
        Connection.ConnectionHandler.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        Connection.ConnectionHandler.isRunning = True
        self.acquisition_thread = threading.Thread(target=Acquisition, args=(base_info, signal_info))
        self.acquisition_thread.daemon = True
        self.acquisition_thread.start()
        self.connect_thr = threading.Thread(target=Connection.connect_thread, args=(base_info, 1))
        self.connect_thr.daemon = True
        self.connect_thr.start()

    def stop(self):
        #self.app.quit()
        self.main_window.close()
        #self.app.exit()
        Connection.ConnectionHandler.isRunning = False
        Connection.ConnectionHandler.isConnected = False
        with Connection.ConnectionHandler.connection_lock:
            Connection.ConnectionHandler.lostConnection.notify_all()
            Connection.ConnectionHandler.connected.notify_all()
        self.acquisition_thread.join()
        self.connect_thr.join()
        try:
            Connection.ConnectionHandler.client.close()
        except Exception as e:
            pass