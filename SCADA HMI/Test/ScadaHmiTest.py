import socket
import threading
import time
import unittest
import sys
from typing import override

from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
import ModbusMockServer
import Connection
import Acquisition
from CustomWindow import TableExample
from DataBase import base_info, signal_info
from Test.ScadaAppStartup import ScadaAppStartup


class TestNormalTemperature(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temperature = '282'
        cls.control_rods = '0'
        cls.automation_request = b'\x00\x00'
        cls.temperature_alarm = "NO ALARM"
        cls.control_rods_alarm = "NO ALARM"
        cls.mock_server = ModbusMockServer.NormalTemperatureModbusMockServer()

    def setUp(self):
        self.app = ScadaAppStartup()
        self.app.run()
        self.mock_server.start()

    def tearDown(self):
        self.mock_server.stop()
        self.app.stop()

    def test_temperature_display(self):
        result = self.query_gui_for(self.temperature,
                                    self.control_rods,
                                    self.check_temperature,
                                    self.check_control_rods)
        self.assertTrue(result, f"Alarms are not {self.temperature} and {self.control_rods}")

    def test_app_runs_with_mock_server(self):
        QTest.qWait(4000)
        for _ in range(30):
            if Connection.ConnectionHandler.isConnected:
                break
            QTest.qWait(100)
        label_style = self.app.main_window.label.styleSheet()
        self.assertIn("background-color: green", label_style)
        self.assertTrue(True)

    def test_alarm(self):
        result = self.query_gui_for(self.temperature_alarm,
                                    self.control_rods_alarm,
                                    self.check_temperature_alarm,
                                    self.check_control_rods_alarm)
        self.assertTrue(result, f"Alarms are not {self.temperature_alarm} and {self.control_rods_alarm}")

    def query_gui_for(self, temperature, control_rods, check_temperature, check_control_rods):
        table = self.app.main_window.tableWidget
        for _ in range(30):
            table_data = self.get_table_data(table)
            if check_temperature(table_data, temperature) and check_control_rods(table_data, control_rods):
                return True
            QTest.qWait(100)
        return False

    @staticmethod
    def check_temperature_alarm(data, value):
        return data[1][4] == value

    @staticmethod
    def check_temperature(data, value):
        return data[1][3] == value

    @staticmethod
    def check_control_rods_alarm(data, value):
        return data[0][4] == value

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
        cls.automation_request = b'\xff\x00'
        cls.temperature_alarm = "HIGH ALARM"
        cls.control_rods_alarm = "NO ALARM"
        cls.mock_server = ModbusMockServer.HighTemperatureModbusMockServer()

    def test_automation_logic(self):
        with self.mock_server.write_requests_condition:
            while not self.mock_server.write_requests:
                self.mock_server.write_requests_condition.wait()
            request = self.mock_server.write_requests[-1]
        self.assertTrue((request[-2:] == self.automation_request), f"Automation is sending {request[-2:]} to the server, expected {self.automation_request}")

class TestLowTemperature(TestNormalTemperature):
    @classmethod
    def setUpClass(cls):
        cls.temperature = '45'
        cls.control_rods = '0'
        cls.automation_request = b'\x00\x00'
        cls.temperature_alarm = "LOW ALARM"
        cls.control_rods_alarm = "NO ALARM"
        cls.mock_server = ModbusMockServer.LowTemperatureModbusMockServer()

    def test_automation_logic(self):
        with self.mock_server.write_requests_condition:
            while not self.mock_server.write_requests:
                self.mock_server.write_requests_condition.wait()
            request = self.mock_server.write_requests[-1]
        self.assertTrue((request[-2:] == self.automation_request), f"Automation is sending {request[-2:]} to the server, expected {self.automation_request}")

if __name__ == '__main__':
    unittest.main()