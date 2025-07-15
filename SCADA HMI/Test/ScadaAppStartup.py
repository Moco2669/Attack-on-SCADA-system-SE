import sys
import threading

import Connection
import CustomWindow

from PyQt5.QtWidgets import QApplication

from Acquisition import Acquisition
from DataBase import base_info, signal_info


class ScadaAppStartup:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = CustomWindow.TableExample()
        self.acquisition_thread = None
        self.connect_thr = None

    def run_app(self):
        self.acquisition_thread = threading.Thread(target=Acquisition, args=(base_info, signal_info))
        self.acquisition_thread.daemon = True
        self.acquisition_thread.start()
        self.connect_thr = threading.Thread(target=Connection.connect_thread, args=(base_info, 1))
        self.connect_thr.daemon = True
        self.connect_thr.start()
        sys.exit(self.app.exec_())