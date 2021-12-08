# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys, math

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QFileDialog,QWidget
from PySide6.QtCore import QFile, Slot, Signal, Qt, QTimer, QPoint, QRect
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPainter, QPen, QPixmap, QBrush, QPalette

import tobii_research as tr
from ui.ui_start_panel import Ui_start_panel

global_user_position_guide = []


def user_position_guide_callback(gaze_data):
    global global_user_position_guide
    global_user_position_guide = gaze_data


class EyePosShow(QWidget):
    def __init__(self, parent=None):
        super(EyePosShow, self).__init__(parent)
        self.current_point_x = [0.5, 0.5, 0.5]
        self.current_point_y = [0.5, 0.5, 0.5]
        self.current_rad = 10
        self.IsPainter = False

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.IsPainter == True:
            self.W = self.width()
            self.H = self.height() * 0.8
            painter = QPainter()
            painter.begin(self)
            pen = QPen(Qt.white, 1, Qt.SolidLine)
            painter.setPen(pen)
            brush = QBrush()
            brush.setColor(Qt.white)
            brush.setStyle(Qt.SolidPattern)
            painter.setBrush(brush)
            rect1 = QRect(0, 0.9 * self.height(), self.width(), 0.1 * self.height())
            rect2 = QRect(0, 0, self.width(), 0.9 * self.height())
            painter.fillRect(rect2, Qt.black)
            eye_find = 0
            if math.isnan(self.current_point_x[0]) or math.isnan(self.current_point_x[1]):
                painter.fillRect(rect1, Qt.red)
            else:
                relative_x = 1 - self.current_point_x[0]
                relative_y = self.current_point_x[1]
                if relative_x <= 1 and relative_y <= 1:
                    painter.drawEllipse(QPoint(relative_x * self.W, relative_y * self.H), self.current_rad,
                                        self.current_rad)
                    eye_find = eye_find + 1
                else:
                    painter.fillRect(rect1, Qt.red)
            if math.isnan(self.current_point_y[0]) or math.isnan(self.current_point_y[1]):
                painter.fillRect(rect1, Qt.red)
            else:
                relative_x = 1 - self.current_point_y[0]
                relative_y = self.current_point_y[1]
                if relative_x <= 1 and relative_y <= 1:
                    painter.drawEllipse(QPoint(relative_x * self.W, relative_y * self.H), self.current_rad,
                                        self.current_rad)
                    eye_find = eye_find + 1
                else:
                    painter.fillRect(rect1, Qt.red)
            if eye_find == 2:
                painter.fillRect(rect1, Qt.green)
            painter.end()


class StartPanel(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_start_panel()
        self.ui.setupUi(self)
        self.eye_show = MyLabel(self.ui.widget_eyepos)


if __name__ == "__main__":
    app = QApplication([])
    widget = StartPanel()
    widget.show()
    sys.exit(app.exec_())
