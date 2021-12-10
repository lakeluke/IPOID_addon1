import sys
import time
from PySide6.QtCore import Qt, QTimer, QPoint, Signal, Slot
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QMessageBox
from PySide6.QtGui import QPainter, QPen, QBrush, QPixmap

import tobii_research as tr

import global_config


def gaze_data_callback(gaze_data):
    global global_gaze_data
    global_gaze_data.append(gaze_data)


class PointShow(QWidget):
    def __init__(self, parent=None):
        super(PointShow, self).__init__(parent)
        self.p_x = 0.5
        self.p_y = 0.5
        self.p_rad = 0

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter()
        painter.begin(self)
        self.draw_circle(painter)
        painter.end()

    def draw_circle(self, painter):
        pen = QPen(Qt.red, 1, Qt.SolidLine)
        painter.setPen(pen)
        brush = QBrush()
        brush.setColor(Qt.red)
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)
        painter.drawEllipse(QPoint(self.p_x * self.width(), self.p_y * self.height()),
                            self.p_rad, self.p_rad)


class CalibrationWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.init_calibration_params()
        self.resolution = (1920, 1080)
        self.timer = QTimer()
        self.timer.stop()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.do_timer_timeout)
        self.timer.start()
        self.current_point = 0
        self.current_timer = 0
        self.eyetracker = None

    # custom signals
    OneCalibrationFinish = Signal(list, list)

    def init_ui(self):
        self.setObjectName(u"calibration_widget")
        self.resize(self.resolution)
        self.main_layout = QGridLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setObjectName(u'main_layout')
        self.point_show = PointShow(self)
        self.setContentsMargins(0,0,0,0)
        self.point_show.setObjectName("point_show")
        self.point_show.setStyleSheet("background-color:#808080")

    def init_calibration_params(self):
        self.calibration_point_number = global_config.get_value('eyetracker', 'calibration_point_number')
        if self.calibration_point_number == 5:
            self.calibration_point_list = [(0.1, 0.1), (0.9, 0.1), (0.5, 0.5), (0.1, 0.9), (0.9, 0.9)]
        elif self.calibration_point_number == 9:
            self.calibration_point_list = [(0.1, 0.1), (0.5, 0.1), (0.9, 0.1),
                                           (0.1, 0.5), (0.5, 0.5), (0.9, 0.5),
                                           (0.1, 0.9), (0.5, 0.9), (0.9, 0.9)]
        elif self.calibration_point_number == 13:
            self.calibration_point_list = [(0.1, 0.1), (0.5, 0.1), (0.9, 0.1),
                                           (0.3, 0.3), (0.7, 0.3),
                                           (0.1, 0.5), (0.5, 0.5), (0.9, 0.5),
                                           (0.3, 0.7), (0.7, 0.7),
                                           (0.1, 0.9), (0.5, 0.9), (0.9, 0.9)]
        else:
            QMessageBox.warning(self, '警告', '配置参数calibration_point_number错误！\n '
                                              '必须为5, 9, 13三个值之一\n'
                                              '此参数将被设置为默认值5')
            self.calibration_point_list = [(0.1, 0.1), (0.9, 0.1), (0.5, 0.5), (0.1, 0.9), (0.9, 0.9)]


    def calibration_step(self):
        self.calibration = tr.ScreenBasedCalibration(self.eyetracker)
        self.calibration.enter_calibration_mode()

    @Slot
    def do_timer_timeout(self):
        if self.current_point < 5:
            self.point_show.p_x = self.calibration_point_list[self.current_point][0]
            self.point_show.p_y = self.calibration_point_list[self.current_point][1]
            self.point_show.p_rad = 40.0 - self.current_timer * 4.0
            self.point_show.update()
            if self.current_timer == 5:
                self.calibration.collect_data(self.point_show.p_x, self.point_show.p_y)
                time.sleep(0.5)
            self.current_timer = self.current_timer + 1
            if self.current_timer == 10:
                self.current_point = self.current_point + 1
                self.current_timer = 0
        else:
            self.timer.stop()
            self.calibration_result = self.calibration.compute_and_apply()
            self.calibration.leave_calibration_mode()
            left_gaze_data = []
            right_gaze_data = []
            for calibration_point in self.calibration_result.calibration_points:
                for calibration_samples in calibration_point._CalibrationPoint__calibration_samples:
                    left_data = calibration_samples._CalibrationSample__left_eye._CalibrationEyeData__position_on_display_area
                    right_data = calibration_samples._CalibrationSample__right_eye._CalibrationEyeData__position_on_display_area
                    left_gaze_data.append(left_data)
                    right_gaze_data.append(right_data)
            self.OneCalibrationFinish.emit(left_gaze_data, right_gaze_data)
            self.close()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Q:
            self.close()


if __name__ == "__main__":
    app = QApplication([])
    widget = CalibrationWidget()
    widget.show()
    sys.exit(app.exec_())
