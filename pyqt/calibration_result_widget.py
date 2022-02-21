# !/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import math
from PySide6.QtCore import Qt,  QPoint,  Slot
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QFrame
from PySide6.QtGui import QPainter, QPen, QBrush

class EyeDataShow(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(2)
        self.setStyleSheet('background-color:white')
        self.calibration_point_rad = 10
        self.calibration_point_list = [(0.5, 0.5), (0.1, 0.1), (0.9, 0.1), (0.9, 0.9), (0.1, 0.9)]
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
        for point in self.calibration_point_list:
            painter.drawEllipse(QPoint(point[0] * self.width(), point[1] * self.height()), 
                                self.calibration_point_rad, self.calibration_point_rad)

        pen = QPen(Qt.green, 3, Qt.SolidLine)
        painter.setPen(pen)
        for eye_pos in self.eye_data:
            if eye_pos[2] == 'validity_valid_and_used':
                painter.drawPoint(QPoint(eye_pos[0] * self.width(), eye_pos[1] * self.height()))

class CalibrationResultWidget(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(u'眼动矫正结果')
        self.setObjectName('CalibrationResultWidget')
        self.resize(960,480)
        self.setStyleSheet('background-color:0x161616')
        #self.setContentsMargins(6,6,6,6)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setObjectName('main_layout')
        self.left_result = EyeDataShow(self)
        self.right_result = EyeDataShow(self)
        self.main_layout.addWidget(self.left_result)
        self.main_layout.addWidget(self.right_result)

    @Slot(list, list)
    def draw_calibration_samples(self,calibration_point_list, calibration_sample_list):
        if len(calibration_sample_list)>2 and ('exit' in calibration_sample_list):
            return
        else:
            self.left_result.calibration_point_list = calibration_point_list
            self.right_result.calibration_point_list = calibration_point_list
            self.left_result.eye_data = calibration_sample_list[0]
            self.right_result.eye_data = calibration_sample_list[1]
            self.left_result.update()
            self.right_result.update()
            self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = CalibrationResultWidget()
    w.show()
    sys.exit(app.exec_())
