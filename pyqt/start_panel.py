# !/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import math

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QWidget
from PySide6.QtCore import Slot, Signal, Qt, QTimer, QPoint, QRect
from PySide6.QtGui import QPainter, QPen, QBrush

import global_config
from calibration_widget import CalibrationWidget
from calibration_result_widget import CalibrationResultWidget
from setting_dialog import SettingDialog
from image_show_widget import ImageShowWidget
from ui.ui_start_panel import Ui_start_panel


class EyePosShow(QWidget):
    def __init__(self, parent=None):
        super(EyePosShow, self).__init__(parent)
        self.p_x = [0.5, 0.5, 0.5]
        self.p_y = [0.5, 0.5, 0.5]
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
            rect1 = QRect(0, 0.9 * self.height(), self.width(),
                          0.1 * self.height())
            rect2 = QRect(0, 0, self.width(), 0.9 * self.height())
            painter.fillRect(rect2, Qt.black)
            eye_find = 0
            if math.isnan(self.p_x[0]) or math.isnan(self.p_x[1]):
                painter.fillRect(rect1, Qt.red)
            else:
                relative_x = 1 - self.p_x[0]
                relative_y = self.p_x[1]
                if relative_x <= 1 and relative_y <= 1:
                    painter.drawEllipse(
                        QPoint(relative_x * self.W, relative_y * self.H),
                        self.current_rad, self.current_rad)
                    eye_find = eye_find + 1
                else:
                    painter.fillRect(rect1, Qt.red)
            if math.isnan(self.p_y[0]) or math.isnan(self.p_y[1]):
                painter.fillRect(rect1, Qt.red)
            else:
                relative_x = 1 - self.p_y[0]
                relative_y = self.p_y[1]
                if relative_x <= 1 and relative_y <= 1:
                    painter.drawEllipse(
                        QPoint(relative_x * self.W, relative_y * self.H),
                        self.current_rad, self.current_rad)
                    eye_find = eye_find + 1
                else:
                    painter.fillRect(rect1, Qt.red)
            if eye_find == 2:
                painter.fillRect(rect1, Qt.green)
            painter.end()


class StartPanel(QMainWindow):
    # custom signals
    start_calibration = Signal()
    begin_test = Signal(str)
    continue_test = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_start_panel()
        self.ui.setupUi(self)
        self.setWindowTitle(u'实验主控制台')
        self.ui.btn_calibration.setEnabled(False)
        self.ui.btn_start.setEnabled(False)
        self.eye_show = EyePosShow(self.ui.widget_eyepos)
        self.eye_show.setObjectName("eye_show")
        self.ui.widget_eyepos_layout.addWidget(self.eye_show)

        # init some params
        self.is_calibrated = False
        self.eyetracker_frequency = global_config.get_value('eyetracker', 'frequency')
        self.is_debug = global_config.get_value('mode', 'debug')
        self.dir_imgdb = global_config.get_value('database','path')
        self.ui.lineEdit_imgdb_dir.setText(self.dir_imgdb)
        self.participant_id = 'debug'

        self.eyetracker_wrap = global_config.eyetracker_wrapper

        self.calibration_widget = CalibrationWidget()
        self.calibration_result = CalibrationResultWidget()
        self.setting_dialog = SettingDialog()
        self.image_show_widget = ImageShowWidget()

        self.timer = QTimer()
        self.timer.stop()
        self.timer.setInterval(40)
        self.timer.timeout.connect(self.do_timer_timeout)
        
        self.experiment_started = False
        self.eyetracker_subscribed = False
        self.init_connections()

    def init_connections(self):
        self.timer.timeout.connect(
            self.do_timer_timeout)
        self.start_calibration.connect(
            self.calibration_widget.start_calibration)
        self.calibration_widget.calibration_finish.connect(
            self.calibration_result.draw_calibration_samples)
        self.calibration_widget.calibration_finish.connect(
            self.solve_calibration_end)
        self.begin_test.connect(
            self.image_show_widget.begin_test)
        self.continue_test.connect(
            self.image_show_widget.continue_test)
        self.image_show_widget.eye_detection_error.connect(
            self.solve_eye_detection_error)
        self.image_show_widget.experiment_pause.connect(
            self.image_show_pause)
        self.image_show_widget.experiment_finished.connect(
            self.finish_experiment)

    # custom slots
    # slots autoconnect by name
    @Slot()
    def on_action_setting_triggered(self):
        self.eyetracker_wrap.unsubscribe_user_position()
        self.setting_dialog.show()

    @Slot()
    def on_btn_start_eyetracker_clicked(self):
        if not self.eyetracker_wrap.eyetracker:
            self.ui.eyetracker_info.clear()
            self.ui.eyetracker_info.appendPlainText(
                'there is no eyetracker detected, please check your connection and'
                ' settings, then click the button again!')
        else:
            self.eyetracker_wrap.set_frequency(global_config.config_params['eyetracker']['frequency'])
            self.ui.eyetracker_info.clear()
            self.ui.eyetracker_info.appendPlainText(
                'Address:' + self.eyetracker_wrap.address)
            self.ui.eyetracker_info.appendPlainText(
                "Model: " + self.eyetracker_wrap.model)
            self.ui.eyetracker_info.appendPlainText(
                "Name: " + self.eyetracker_wrap.device_name)
            self.ui.eyetracker_info.appendPlainText(
                "Serial number: " + self.eyetracker_wrap.serial_number)
            self.ui.eyetracker_info.appendPlainText(
                "Gaze output frequency: " + str(self.eyetracker_wrap.get_frequency()))
            if not self.eyetracker_subscribed:
                self.eyetracker_wrap.subscribe_user_position()
                self.eyetracker_subscribed = True
            else:
                QMessageBox.information(self,'提示','重新向眼动仪请求位置数据，请稍等1～2秒')
                self.eyetracker_wrap.unsubscribe_user_position()
                self.eyetracker_wrap.subscribe_user_position()
            self.eye_show.IsPainter = True
            self.timer.start()
            self.ui.btn_calibration.setEnabled(True)

    @Slot()
    def on_btn_calibration_clicked(self):
        # query whether to enter calibration
        query_result = QMessageBox.question(self, '提示', '是否开始校准？',
                                            QMessageBox.Yes | QMessageBox.No,
                                            QMessageBox.Yes)
        if (query_result == QMessageBox.Yes):
            self.timer.stop()
            self.start_calibration.emit()
            if self.is_calibrated == False:
                self.is_calibrated = True

    @Slot()
    def on_btn_getdir_clicked(self):
        str_dir = QFileDialog.getExistingDirectory()
        if str_dir == '':
            return
        self.ui.lineEdit_imgdb_dir.setText(str_dir)

    @Slot()
    def on_btn_imgdb_apply_clicked(self):
        self.dir_imgdb = self.ui.lineEdit_imgdb_dir.text()
        is_exist = os.path.exists(self.dir_imgdb)
        if not is_exist:
            QMessageBox.warning(self, u'错误警告', u'路径不存在！')
            return
        global_config.set_value('database', 'path', self.dir_imgdb)
        self.ui.btn_start.setEnabled(True)

    @Slot()
    def on_btn_start_clicked(self):
        if not os.path.exists(self.dir_imgdb):
            msg = '数据库地址：%s 无效,请检查是否已应用' % (self.dir_imgdb)
            QMessageBox.warning(self, '警告', msg)
            return
        if self.eyetracker_wrap.eyetracker == None:
            if (self.is_debug):
                QMessageBox.warning(self, '调试模式', '未检测到眼动仪设备，下面将只显示页面，不记录信息')
            else:
                QMessageBox.warning(self, 'fatal error', '未检测到眼动仪设备，请检查连接')
                return
        if self.experiment_started == False:
            self.experiment_started = True
            self.timer.stop()
            self.begin_test.emit(self.participant_id)
        else:
            self.image_show_widget.is_ready = True
            self.timer.stop()
            self.continue_test.emit(self.participant_id)

    # slots connect manually
    @Slot(str)
    def begin_setting(self, participant_id='debug'):
        self.participant_id = participant_id
        self.show()

    @Slot()
    def do_timer_timeout(self):
        user_position = self.eyetracker_wrap.user_position
        if len(user_position):
            left_data = user_position['left_user_position']
            right_data = user_position['right_user_position']
            self.eye_show.p_x = left_data
            self.eye_show.p_y = right_data
            self.eye_show.update()
            track_box = self.eyetracker_wrap.get_track_box()
            track_box_base = track_box.front_upper_right
            track_box_size = (
                track_box.back_lower_left[0] - track_box.front_upper_right[0],
                track_box.back_lower_left[1] - track_box.front_upper_right[1],
                track_box.back_lower_left[2] - track_box.front_upper_right[2],
            )
            left_z = 0
            right_z = 0
            left_d2c = 1
            right_d2c = 1
            if user_position['left_user_position_validity']:
                left_z = left_data[2] * track_box_size[2] + track_box_base[2]
                left_d2c = math.sqrt((left_data[0] - 0.5)**2 +
                                     (left_data[1] - 0.5)**2 +
                                     (left_data[2] - 0.5)**2)
            if user_position['right_user_position_validity']:
                right_z = right_data[2] * track_box_size[2] + track_box_base[2]
                right_d2c = math.sqrt((right_data[0] - 0.5)**2 +
                                      (right_data[1] - 0.5)**2 +
                                      (right_data[2] - 0.5)**2)
            distance = int(0.5 * (left_z + right_z) / 10)
            d2c = 100 - int(0.5 * (left_d2c + right_d2c) * 100)
            self.ui.pgb_h.setValue(d2c)
            if distance < 45:
                self.ui.pgb_v.setValue(45)
                self.ui.distance.setText(str(45))
            elif distance > 75:
                self.ui.pgb_v.setValue(75)
                self.ui.distance.setText(str(75))
            else:
                self.ui.pgb_v.setValue(distance)
                self.ui.distance.setText(str(distance))

    @Slot()
    def solve_calibration_end(self):
        self.timer.start()
    
    @Slot()
    def solve_eye_detection_error(self):
        self.timer.start()

    @Slot()
    def finish_experiment(self):
        self.eyetracker_wrap.unsubscribe_user_position()
        self.close()

    @Slot()
    def image_show_pause(self):
        self.timer.start()
        self.show()

    # other methods


if __name__ == "__main__":
    global_config.init()
    app = QApplication([])
    widget = StartPanel()
    widget.begin_setting()
    sys.exit(app.exec_())
