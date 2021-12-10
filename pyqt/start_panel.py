# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys, math

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel, QFileDialog, QWidget
from PySide6.QtCore import QFile, Slot, Signal, Qt, QTimer, QPoint, QRect
from PySide6.QtGui import QPainter, QPen, QPixmap, QBrush, QPalette

import tobii_research as tr

import global_config
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
        self.eye_show = EyePosShow(self.ui.widget_eyepos)
        self.eye_show.setObjectName("eye_show")
        self.timer = QTimer()
        # init some params
        self.__isCalibration = False
        self.eyetracker_frequency = global_config.get_value('eyetracker', 'frequency', 60)
        self.mode = global_config.config_params['mode']



    def init_connections(self):
        pass

    # custom signals
    begin_test = Signal(str, str)

    # custom slots
    @Slot
    def on_btn_start_eyetracker_clicked(self):
        self.eyetrackers = tr.find_all_eyetrackers()
        if not self.eyetrackers:
            self.ui.eyetracker_info.clear()
            self.ui.eyetracker_info.appendPlainText('there is no eyetracker detected, please check your connection and'
                                                    ' settings, then click the button again!')
        else:
            self.eyetracker = self.eyetrackers[0]
            self.eyetracker.set_gaze_output_frequency(self.eyetracker_frequency)
            self.ui.eyetracker_info.clear()
            self.ui.eyetracker_info.appendPlainText('Address:' + self.eyetracker.address)
            self.ui.eyetracker_info.appendPlainText("Model: " + self.eyetracker.model)
            self.ui.eyetracker_info.appendPlainText("Name (It's OK if this is empty): " + self.eyetracker.device_name)
            self.ui.eyetracker_info.appendPlainText("Serial number: " + self.eyetracker.serial_number)
            self.ui.eyetracker_info.appendPlainText(
                "Gaze output frequency: " + str(self.eyetracker.get_gaze_output_frequency()))
            self.eyetracker.subscribe_to(tr.EYETRACKER_USER_POSITION_GUIDE, user_position_guide_callback,
                                         as_dictionary=True)
            self.track_box = self.eyetracker.get_track_box()
            self.z5 = self.track_box.back_upper_right[2]
            self.z1 = self.track_box.front_upper_right[2]
            self.eye_show.IsPainter = True
            self.timer.stop()
            self.timer.setInterval(20)
            self.timer.timeout.connect(self.do_timer_timeout)
            self.timer.start()
            self.ui.btn_calibration.setEnabled(True)

            # other methods

    @Slot
    def on_btn_calibration_clicked(self):
        # query whether to enter calibration
        query_result = QMessageBox.question(self, '提示', '是否开始校准？',
                                            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)
        if (query_result == QMessageBox.Yes):
            if self.__isCalibration == False:
                self.__Calibration_panel = Qmycalibration_panel(self)
                self.__Calibration_panel.OneCalibrationFinish.connect(self.OneCalibrationFinish)
                self.__isCalibration = True
            self.__Calibration_panel.eyetracker = self.eyetracker
            # self.eyetracker.unsubscribe_from(tr.EYETRACKER_USER_POSITION_GUIDE, user_position_guide_callback)
            self.timer.stop()
            self.__Calibration_panel.currentpoint = 0
            self.__Calibration_panel.point_Show.current_point_x = 0.5
            self.__Calibration_panel.point_Show.current_point_y = 0.5
            self.__Calibration_panel.point_Show.current_rad = 0
            self.__Calibration_panel.timer.start()
            self.__Calibration_panel.showFullScreen()
            self.__Calibration_panel.calibration_step()

if __name__ == "__main__":
    app = QApplication([])
    widget = StartPanel()
    widget.show()
    sys.exit(app.exec_())
