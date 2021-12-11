import sys
from PySide6.QtCore import Qt,  QPoint,  Slot
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QFrame
from PySide6.QtGui import QPainter, QPen, QBrush

import math

class EyeDataShow(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(2)
        self.setStyleSheet('background-color:white')
        self.p_rad = 10
        self.list = [(0.5, 0.5), (0.1, 0.1), (0.9, 0.1), (0.9, 0.9), (0.1, 0.9)]
        self.eye_data = []

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter()
        painter.begin(self)
        self.draw_eye_data(painter)
        painter.end()

    def draw_eye_data(self,painter):
        pen = QPen(Qt.black, 1, Qt.SolidLine)
        painter.setPen(pen)
        brush = QBrush()
        brush.setColor(Qt.white)
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)
        # draw calibration points
        for point in self.list:
            painter.drawEllipse(QPoint(point[0] * self.width(), point[1] * self.height()), self.p_rad, self.p_rad)

        pen = QPen(Qt.green, 3, Qt.SolidLine)
        painter.setPen(pen)
        for eye_pos in self.eye_data:
            if math.isnan(eye_pos[0]) or math.isnan(eye_pos[1]):
                continue
            if eye_pos[0] < 0 or eye_pos[0] > 1 or eye_pos[1] < 0 or eye_pos[1] > 1:
                continue
            painter.drawPoint(QPoint(eye_pos[0] * self.width(), eye_pos[1] * self.height()))

class CalibrationResultWidget(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setObjectName('CalibrationResultWidget')
        self.resize(960,480)
        self.setStyleSheet('background-color:0x101010')
        #self.setContentsMargins(6,6,6,6)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setObjectName('main_layout')
        self.left_result = EyeDataShow(self)
        self.right_result = EyeDataShow(self)
        self.main_layout.addWidget(self.left_result)
        self.main_layout.addWidget(self.right_result)

    @Slot(list,list)
    def do_draw_eye_data(self,left_eye_data,right_eye_data):
        self.left_result.eye_data = left_eye_data
        self.left_result.update()
        self.right_result.eye_data = right_eye_data
        self.right_result.update()
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = CalibrationResultWidget()
    w.show()
    sys.exit(app.exec_())