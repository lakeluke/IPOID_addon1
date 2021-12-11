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
from calibration_widget import CalibrationWidget
from calibration_result_widget import CalibrationResultWidget
from setting_dialog import SettingDialog

global_user_position_guide = []


def user_position_guide_callback(gaze_data):
    global global_user_position_guide
    global_user_position_guide = gaze_data


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
            rect1 = QRect(0, 0.9 * self.height(), self.width(), 0.1 * self.height())
            rect2 = QRect(0, 0, self.width(), 0.9 * self.height())
            painter.fillRect(rect2, Qt.black)
            eye_find = 0
            if math.isnan(self.p_x[0]) or math.isnan(self.p_x[1]):
                painter.fillRect(rect1, Qt.red)
            else:
                relative_x = 1 - self.p_x[0]
                relative_y = self.p_x[1]
                if relative_x <= 1 and relative_y <= 1:
                    painter.drawEllipse(QPoint(relative_x * self.W, relative_y * self.H), self.current_rad,
                                        self.current_rad)
                    eye_find = eye_find + 1
                else:
                    painter.fillRect(rect1, Qt.red)
            if math.isnan(self.p_y[0]) or math.isnan(self.p_y[1]):
                painter.fillRect(rect1, Qt.red)
            else:
                relative_x = 1 - self.p_y[0]
                relative_y = self.p_y[1]
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

        self.calibration_widget = CalibrationWidget(self)
        self.calibration_result = CalibrationResultWidget(self)
        self.setting_dialog = SettingDialog(self)
        self.image_show_widget = ImageShowWidget(self)
        # init some params
        self.isCalibrated = False
        self.eyetracker_frequency = global_config.get_value('eyetracker', 'frequency', 60)
        self.is_debug = global_config.get_value('mode', 'debug')

        self.dir_imgdb = ''
        self.experiment_started = False

    def init_connections(self):
        self.start_calibration.connect(self.calibration_widget.start_calibration)
        self.calibration_widget.calibration_finish.connect(self.calibration_result.do_draw_eye_data)
        self.setting_dialog.settings_changed.connect(self.do_setting_config)
        self.begin_test.connect(self.image_show_widget.begin_test)
        self.continue_test.connect(self.image_show_widget.continue_test)
        self.image_show_widget.eye_detection_error.connect(self.solve_eye_detection_error)


    # custom signals
    start_calibration = Signal()
    begin_test = Signal()
    continue_test = Signal()

    # custom slots
    # slots autoconnect by name
    @Slot()
    def on_action_setting_triggered(self):
        self.setting_dialog.show()

    @Slot()
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

    @Slot()
    def on_btn_calibration_clicked(self):
        # query whether to enter calibration
        query_result = QMessageBox.question(self, '提示', '是否开始校准？',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if (query_result == QMessageBox.Yes):
            self.calibration_widget.eyetracker = self.eyetracker
            # self.eyetracker.unsubscribe_from(tr.EYETRACKER_USER_POSITION_GUIDE, user_position_guide_callback)
            self.timer.stop()
            self.calibration_widget.current_point = 0
            self.calibration_widget.point_show.p_x = 0.5
            self.calibration_widget.point_show.p_y = 0.5
            self.calibration_widget.point_show.current_rad = 0
            self.calibration_widget.timer.start()
            self.calibration_widget.showFullScreen()
            self.calibration_widget.calibration_step()
            if self.isCalibrated == False:
                self.isCalibrated = True

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
        self.ui.btn_start.setEnabled(True)

    @Slot()
    def on_btn_start_clicked(self):
        if os.path.exists(self.dir_imgdb):
            msg = '数据库地址：%s 无效,请检查是否已应用' % (self.dir_imgdb)
            QMessageBox.warning(self, '警告', msg)
            return
        if self.eyetracker == None:
            if (self.is_debug):
                QMessageBox.warning(self, '调试模式', '未检测到眼动仪设备，下面将只显示页面，不记录信息')
            else:
                QMessageBox.warning(self, 'fatal error', '未检测到眼动仪设备，请检查连接')
                return
        if self.experiment_started == False:
            self.image_show_widget.eyetracker = self.eyetracker
            self.experiment_started = True
            self.timer.stop()
            self.begin_test.emit()
        else:
            self.image_show_widget.is_ready = True
            self.timer.stop()
            self.continue_test.emit()

    # slots connect manually
    @Slot(str)
    def begin_setting(self, dir_data):
        self.dir_save_data = dir_data
        self.show()

    @Slot()
    def do_timer_timeout(self):
        if global_user_position_guide:
            left_data = global_user_position_guide['left_user_position']
            right_data = global_user_position_guide['right_user_position']
            self.eye_show.p_x = left_data
            self.eye_show.p_y = right_data
            self.eye_show.update()
            left_z = 0
            right_z = 0
            if not math.isnan(left_data[2]):
                left_z = left_data[2] * (self.z5 - self.z1) + self.z1
            if not math.isnan(right_data[2]):
                right_z = right_data[2] * (self.z5 - self.z1) + self.z1
            distance = int(0.5 * (left_z + right_z) / 10)
            if distance < 45:
                self.ui.pgb_v.setValue(45)
                self.ui.distance.setText(str(45))
            elif distance > 75:
                self.ui.pgb_v.setValue(75)
                self.ui.distance.setText(str(75))
            else:
                self.ui.pgb_v.setValue(distance)
                self.ui.distance.setText(str(distance))

    @Slot(dict)
    def do_setting_config(self, settings):
        self.eyetracker_frequency = settings['eyetracker']['frequency']
        self.image_show_time = settings['image_show']['last_time']
        self.image_show_interval = settings['image_show']['time_interval']
        global_config.set_value('eyetracker', 'frequency', self.eyetracker_frequency)
        global_config.set_value('image_show', 'last_time', self.image_show_time)
        global_config.set_value('image_show', 'time_interval', self.image_show_interval)

    @Slot()
    def solve_eye_detection_error(self):
        self.timer.start()

    @Slot()
    def finish_experiment(self):
        self.close()

    # other methods


if __name__ == "__main__":
    global_config.init()
    app = QApplication([])
    widget = StartPanel()
    widget.begin_setting()
    sys.exit(app.exec_())
