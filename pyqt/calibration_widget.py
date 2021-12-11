import sys
import time
from PySide6.QtCore import Qt, QTimer, QPoint, Signal, Slot
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QMessageBox
from PySide6.QtGui import QPainter, QPen, QBrush

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
        self.eyetracker = None
        self.resolution = (1920, 1080)
        self.is_debug = global_config.get_value('mode', 'debug', False)
        self.refresh_interval_ms = 100
        self.point_show_time_refresh = 10
        self.point_show_calibration_time_refresh = 5
        self.point_show_interval_refresh = 2
        self.current_point = 0
        self.current_timer = 0
        self.init_ui()
        self.init_calibration_params()
        self.init_timer()

    # custom signals
    calibration_finish = Signal(list, list)

    # init methods
    def init_ui(self):
        self.setObjectName(u"calibration_widget")
        self.resize(self.resolution[0],self.resolution[1])
        self.move(0,0)
        self.main_layout = QGridLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setObjectName(u'main_layout')
        self.point_show = PointShow(self)
        self.setContentsMargins(0,0,0,0)
        self.point_show.setObjectName(u"point_show")
        self.point_show.setStyleSheet("background-color:#808080")
        self.main_layout.addWidget(self.point_show)

    def init_calibration_params(self):
        self.calibration_point_number = global_config.get_value('eyetracker', 'calibration_point_number',5)
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

    def init_timer(self):
        self.timer = QTimer()
        self.timer.stop()
        self.timer.setInterval(self.refresh_interval_ms)
        self.timer.timeout.connect(self.do_timer_timeout)

    @Slot()
    def start_calibration(self):
        self.timer.start()
        self.showFullScreen()
        if self.is_debug:
            QMessageBox.information(self,u'调试模式',u'未发现眼动仪，仅演示显示效果！')
        else:
            self.calibration = tr.ScreenBasedCalibration(self.eyetracker)
            self.calibration.enter_calibration_mode()

    @Slot()
    def do_timer_timeout(self):
        if self.current_point < self.calibration_point_number:
            self.point_show.p_x = self.calibration_point_list[self.current_point][0]
            self.point_show.p_y = self.calibration_point_list[self.current_point][1]
            self.point_show.p_rad = 40.0 - self.current_timer * 4.0
            self.point_show.update()
            if self.current_timer == self.point_show_time_refresh-self.point_show_calibration_time_refresh:
                if not self.is_debug:
                    self.calibration.collect_data(self.point_show.p_x, self.point_show.p_y)
                time.sleep(0.5)
            self.current_timer = self.current_timer + 1
            if self.current_timer == self.point_show_time_refresh:
                self.current_point = self.current_point + 1
                self.current_timer = 0
        else:
            self.timer.stop()
            if not self.is_debug:
                self.calibration_result = self.calibration.compute_and_apply()
                self.calibration.leave_calibration_mode()
            left_gaze_data = []
            right_gaze_data = []
            if not self.is_debug:
                for calibration_point in self.calibration_result.calibration_points:
                    for calibration_samples in calibration_point._CalibrationPoint__calibration_samples:
                        left_data = calibration_samples._CalibrationSample__left_eye._CalibrationEyeData__position_on_display_area
                        right_data = calibration_samples._CalibrationSample__right_eye._CalibrationEyeData__position_on_display_area
                        left_gaze_data.append(left_data)
                        right_gaze_data.append(right_data)
            self.calibration_finish.emit(left_gaze_data, right_gaze_data)
            self.close()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Q:
            self.close()


if __name__ == "__main__":
    global_config.init()
    app = QApplication([])
    widget = CalibrationWidget()
    widget.start_calibration()
    sys.exit(app.exec_())
