from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import \
    QApplication, QMainWindow, QWidget, QGridLayout, QSlider, QLabel
from PyQt6.QtGui import QPainter, QVector2D
from math import sin, cos, pi
import sys
from time import time

WIDTH = 800
HEIGHT = 640

def rotateVec(v, angle):
    return QVector2D(
        cos(angle)*v.x() - sin(angle)*v.y(),
        sin(angle)*v.x() + cos(angle)*v.y()
    )

class KochSnowflake(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.__n = 1
        self.__drawTime = 0

    def drawSnowflakeLine(self, x1, y1, x2, y2, n):
        Vec = QVector2D
        begin, end = Vec(x1, y1), Vec(x2, y2)
        a = end - begin
        b = a/3
        rotatedB = rotateVec(b, -pi/3)
        if (n == 1):
            self.painter.drawLine(
                begin.x(), begin.y(),
                begin.x() + b.x(), begin.y() + b.y()
                )
            self.painter.drawLine(
                begin.x() + b.x(), begin.y() + b.y(),
                begin.x() + b.x() + rotatedB.x(), begin.y() + b.y() + rotatedB.y()
            )   
            self.painter.drawLine(
                begin.x() + b.x() + rotatedB.x(), begin.y() + b.y() + rotatedB.y(), 
                begin.x() + 2*b.x(), begin.y() + 2*b.y()
            )   
            self.painter.drawLine(
                begin.x() + 2*b.x(), begin.y() + 2*b.y(),
                end.x(), end.y()
            )
        else:
            self.drawSnowflakeLine(
                begin.x(), begin.y(),
                begin.x() + b.x(), begin.y() + b.y(),
                n-1
                )
            self.drawSnowflakeLine(
                begin.x() + b.x(), begin.y() + b.y(),
                begin.x() + b.x() + rotatedB.x(), begin.y() + b.y() + rotatedB.y(),
                n-1
            )   
            self.drawSnowflakeLine(
                begin.x() + b.x() + rotatedB.x(), begin.y() + b.y() + rotatedB.y(), 
                begin.x() + 2*b.x(), begin.y() + 2*b.y(),
                n-1
            )   
            self.drawSnowflakeLine(
                begin.x() + 2*b.x(), begin.y() + 2*b.y(),
                end.x(), end.y(),
                n-1
            )

    def setN(self, n):
        if n > 0:
            self.__n = n
    
    def getN(self):
        return self.__n

    def getDrawTime(self):
        return self.__drawTime

    def paintEvent(self, paintEvent):
        self.painter = QPainter(self)
        w, h = self.width(), self.height()
        t0 = time()
        self.drawSnowflakeLine(w/40, h/3*2, w*39/40, h/3*2, self.__n)
        self.__drawTime = time() - t0
        self.painter.end()

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Koch snowflake")
        self.setMinimumSize(WIDTH, HEIGHT)
        self.initWidgets()
    
    def onSliderValueChanged(self):
        self.snowflake.setN(self.slider.value())
        self.snowflake.update()
        self.label.setText(f"{self.snowflake.getN()} dimensions. Draw time is {int(self.snowflake.getDrawTime()*1000)} ms.")

    def initWidgets(self):
        self.cw = QWidget(self)
        self.setCentralWidget(self.cw)
        
        self.mainLayout = QGridLayout(self)
        self.cw.setLayout(self.mainLayout)

        self.snowflake = KochSnowflake(self)
        self.mainLayout.addWidget(self.snowflake, 0, 0, 4, 4)

        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.mainLayout.addWidget(self.slider, 4, 0, 1, 3)
        self.slider.setMinimum(1)
        self.slider.setMaximum(10)
        self.slider.valueChanged.connect(self.onSliderValueChanged)

        self.label = QLabel()
        self.mainLayout.addWidget(self.label, 4, 3)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()
    app.exec()