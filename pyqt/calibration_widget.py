# !/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import time
from PySide6.QtCore import Qt, QTimer, QPoint, Signal, Slot
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QMessageBox
from PySide6.QtGui import QPainter, QPen, QBrush
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
    # custom signals
    calibration_finish = Signal(list,list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resolution = (1920, 1080)
        self.refresh_interval_ms = 40
        self.point_show_time_ms = 1000
        self.point_show_calibration_time_ms = 500
        self.point_show_interval_ms = 200
        self.refresh_num_each_point = int(self.point_show_time_ms/self.refresh_interval_ms) 
        self.refresh_num_each_calibration = int(self.point_show_calibration_time_ms/self.refresh_interval_ms) 
        
        self.init_ui()
        self.init_calibration_params()
        self.init_timer()
        
    
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
        self.calibration_point_number = global_config.get_value('eyetracker', 'calibration_point_number',9)
        calibration_point_dict = {
            5: [(0.1, 0.1), (0.9, 0.1), (0.5, 0.5), (0.1, 0.9), (0.9, 0.9)],
            9: [(0.1, 0.1), (0.5, 0.1), (0.9, 0.1),
                (0.1, 0.5), (0.5, 0.5), (0.9, 0.5),
                (0.1, 0.9), (0.5, 0.9), (0.9, 0.9)],
            13: [(0.1, 0.1), (0.5, 0.1), (0.9, 0.1),
                (0.3, 0.3), (0.7, 0.3),
                (0.1, 0.5), (0.5, 0.5), (0.9, 0.5),
                (0.3, 0.7), (0.7, 0.7),
                (0.1, 0.9), (0.5, 0.9), (0.9, 0.9)]
        }
        if self.calibration_point_number in calibration_point_dict.keys():
            self.calibration_point_list = calibration_point_dict[self.calibration_point_number]    
        else:
            QMessageBox.warning(self, '警告', '配置参数calibration_point_number错误！\n '
                                              '必须为5, 9, 13三个值之一\n'
                                              '此参数将被设置为默认值5')
            self.calibration_point_list = calibration_point_dict[5]

    def init_timer(self):
        self.timer = QTimer()
        self.timer.stop()
        self.timer.setInterval(self.refresh_interval_ms)
        self.timer.timeout.connect(self.do_timer_timeout)

    @Slot()
    def start_calibration(self):
        self.eyetracker_wrap = global_config.eyetracker_wrapper
        self.is_debug = global_config.get_value('mode', 'debug', False)
        self.current_point = 0
        self.current_refresh = 0
        if not self.eyetracker_wrap.eyetracker:
            if self.is_debug:
                QMessageBox.information(self,u'调试模式',u'未发现眼动仪，仅演示显示效果！')
            else:
                QMessageBox.information(self,u'矫正开启错误',u'未发现眼动仪，请检查连接')
        else:
            self.eyetracker_wrap.calibration_start()
        self.showFullScreen()
        self.timer.start()

    @Slot()
    def do_timer_timeout(self):
        if self.current_point < self.calibration_point_number:
            self.point_show.p_x = self.calibration_point_list[self.current_point][0]
            self.point_show.p_y = self.calibration_point_list[self.current_point][1]
            self.point_show.p_rad = 40.0 * (1-self.current_refresh/self.refresh_num_each_point)
            self.point_show.update()
            if self.current_refresh == self.refresh_num_each_point-self.refresh_num_each_calibration:
                time.sleep(0.5)
                if self.eyetracker_wrap.eyetracker:
                    self.eyetracker_wrap.calibration_collect((self.point_show.p_x, self.point_show.p_y)) 
            self.current_refresh = self.current_refresh + 1
            if self.current_refresh >= self.refresh_num_each_point:
                self.current_point = self.current_point + 1
                self.current_refresh = 0
        else:
            self.timer.stop()
            self.calibration_result = None
            if self.eyetracker_wrap.eyetracker:
                self.calibration_result = self.eyetracker_wrap.calibration_apply()
                self.eyetracker_wrap.calibration_end()
            self.close()
            self.process_calibration_result()

    def process_calibration_result(self):
        calibration_sample_list = ()
        if self.calibration_result:
            calibration_status = self.calibration_result.status
            if calibration_status != 'calibration_status_success':
                qresult = QMessageBox.question(self,'矫正失败','矫正状态：%s \n 是否重新矫正？'%calibration_status,
                                     QMessageBox.Yes|QMessageBox.No)
                if qresult == QMessageBox.Yes:
                    self.start_calibration()
                    return
            left_samples = []
            right_samples = []
            for calibration_point in self.calibration_result.calibration_points:
                for calibration_sample in calibration_point.calibration_samples:
                    left_sample = (calibration_sample.left_eye.position_on_display_area + 
                                (calibration_sample.left_eye.validity,) )
                    right_sample = (calibration_sample.right_eye.position_on_display_area + 
                                (calibration_sample.right_eye.validity,) )
                    left_samples.append(left_sample)
                    right_samples.append(right_sample)
            calibration_sample_list = [left_samples,right_samples]
        self.calibration_finish.emit(self.calibration_point_list, calibration_sample_list)    
                    
         
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Q:
            self.timer.stop()
            self.close()
            self.eyetracker_wrap.calibration_end()
            self.calibration_finish.emit(self.calibration_point_list,[[],[],'calibration_key_Q exit'])


if __name__ == "__main__":
    global_config.init()
    app = QApplication([])
    widget = CalibrationWidget()
    widget.start_calibration()
    sys.exit(app.exec_())
