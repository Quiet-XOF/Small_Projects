import psutil
from PySide6 import QtCore, QtWidgets, QtGui
import pyqtgraph
import sys
import time


class Widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.setWindowTitle("CPU Monitor")

        self.text = QtWidgets.QLabel("Starting...", alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.text)

        self.plotWidget = pyqtgraph.PlotWidget()
        
        self.plotWidget.setYRange(0, 100)
        self.plotWidget.setTitle("System Monitor: CPU Usage")
        self.plotWidget.setLabel("left", "CPU Usage %")
        self.plotWidget.setLabel("bottom", "Time (seconds)")
        self.layout.addWidget(self.plotWidget)

        self.data = []
        self.max = 100

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.runCPU)
        self.timer.start(1000)

        self.plotWidget.setBackground((240, 240, 240))
    

    @QtCore.Slot()
    def runCPU(self):
        cpu_usage = psutil.cpu_percent(interval=None)

        self.data.append(cpu_usage)
        if len(self.data) > self.max:
            self.data.pop(0)
        
        if cpu_usage < 50:
            self.curve = self.plotWidget.plot(pen="g")
        elif cpu_usage < 80:
            self.curve = self.plotWidget.plot(pen="o")
        else:
            self.curve = self.plotWidget.plot(pen="r")

        self.curve.setData(self.data)
        self.text.setText(f"CPU usage: {cpu_usage}%")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Widget()
    widget.resize(600, 400)
    widget.show()

    sys.exit(app.exec())