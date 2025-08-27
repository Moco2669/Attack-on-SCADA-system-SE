from collections import deque
from PyQt5.QtCore import QPointF, pyqtSignal, Qt
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
import time


class HistoryGraph(QWidget):
    update_signal = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self.series_dict = {}
        self.register_colors = {
            "WaterThermometer": QColor(255, 0, 0),
            "ControlRods": QColor(0, 0, 255)
        }
        self.max_points = 200
        self.min_value = 0
        self.max_value = 700
        self.chart = QChart()
        self.chart_view = QChartView(self.chart)
        self.current_time = time.time()
        self.last_update = self.current_time

        self.init_ui()
        self.update_signal.connect(self.update_graph)

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.chart.setTitle("Register History")
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(self.chart_view)
        axis_x = QValueAxis()
        axis_x.setTitleText("Time")
        axis_y = QValueAxis()
        axis_y.setTitleText("Value")
        axis_y.setRange(self.min_value, self.max_value)
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        self.chart.addAxis(axis_x, Qt.AlignBottom)

    def make_series_for_register(self, register_name):
        color = self.register_colors[register_name]
        pen = QPen(color)
        pen.setWidth(2)
        series = QLineSeries()
        series.setName(register_name)
        series.setPen(pen)

        self.series_dict[register_name] = series
        self.chart.addSeries(series)

    def update_axes(self):
        axis_x = self.chart.axisX()
        axis_y = self.chart.axisY()

        x_min = max(0, self.current_time - self.max_points)
        x_max = self.current_time

        axis_x.setRange(x_min, x_max)

        for series_data in self.series_dict.values():
            series_data.attachAxis(axis_x)
            series_data.attachAxis(axis_y)

    def update_graph(self, registers):
        self.current_time = time.time()
        if self.current_time - self.last_update < 1:
            return
        self.last_update = self.current_time
        for reg in registers.values():
            register_name = reg.name
            value = reg.current_value
            if reg.signal_type == "DO":
                value = value * self.max_value

            if register_name not in self.series_dict:
                self.make_series_for_register(register_name)

            series_data = self.series_dict[register_name]

            x_point = self.current_time
            y_point = value

            if series_data.count() >= self.max_points:
                series_data.remove(0)
            series_data.append(QPointF(x_point, y_point))

        self.update_axes()