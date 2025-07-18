import socket
import threading
import time
import unittest
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
import ModbusMockServer
import Connection
import Acquisition
from CustomWindow import TableExample
from DataBase import base_info, signal_info

class TestNormalTemperature(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temperature = '282'
        cls.control_rods = '0'
        cls.mock_server = ModbusMockServer.NormalTemperatureModbusMockServer()

    def setUp(self):
        self.app = QApplication(sys.argv)
        Connection.ConnectionHandler.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.mock_server.start()


        self.main_window = TableExample()

        Connection.ConnectionHandler.isRunning = True

        self.acquisition_thread = threading.Thread(
            target=Acquisition.Acquisition, args=(base_info, signal_info))
        self.acquisition_thread.daemon = True
        self.acquisition_thread.start()

        self.connect_thread = threading.Thread(
            target=Connection.connect_thread, args=(base_info, 1))
        self.connect_thread.daemon = True
        self.connect_thread.start()

    def tearDown(self):
        self.app.quit()
        self.mock_server.stop()
        self.main_window.close()
        self.app.exit()
        Connection.ConnectionHandler.isRunning = False
        Connection.ConnectionHandler.isConnected = False
        with Connection.ConnectionHandler.connection_lock:
            Connection.ConnectionHandler.lostConnection.notify_all()
            Connection.ConnectionHandler.connected.notify_all()
        self.acquisition_thread.join()
        self.connect_thread.join()
        time.sleep(3)

    def test_temperature_display(self):
        table = self.main_window.tableWidget

        for _ in range(30):
            table_data = self.get_table_data(table)
            if self.check_temperature(table_data, self.temperature) and self.check_control_rods(table_data, self.control_rods):
                self.assertTrue(True, "Signals display fine")
                return
            QTest.qWait(100)
        self.assertTrue(False, "Signals never had the appropriate value")

    def test_app_runs_with_mock_server(self):
        QTest.qWait(4000)
        for _ in range(30):
            if Connection.ConnectionHandler.isConnected:
                break
            QTest.qWait(100)
        label_style = self.main_window.label.styleSheet()
        self.assertIn("background-color: green", label_style)
        self.assertTrue(True)

    @staticmethod
    def check_temperature(data, value):
        return data[1][3] == value

    @staticmethod
    def check_control_rods(data, value):
        return data[0][3] == value

    @staticmethod
    def get_table_data(a_table):
        data = []
        for row in range(a_table.rowCount()):
            row_data = []
            for col in range(a_table.columnCount()):
                item = a_table.item(row, col)
                row_data.append(item.text() if item else "None")
            data.append(row_data)
        return data

class TestHighTemperature(TestNormalTemperature):
    @classmethod
    def setUpClass(cls):
        cls.temperature = '365'
        cls.control_rods = '1'
        cls.mock_server = ModbusMockServer.HighTemperatureModbusMockServer()

class TestLowTemperature(TestNormalTemperature):
    @classmethod
    def setUpClass(cls):
        cls.temperature = '45'
        cls.control_rods = '0'
        cls.mock_server = ModbusMockServer.LowTemperatureModbusMockServer()

if __name__ == '__main__':
    unittest.main()