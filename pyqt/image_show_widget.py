import sys
import time
import random
import os
import datetime
from enum import Enum

from PySide6.QtCore import Qt, QTimer, QPoint, Signal, Slot
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QMessageBox,QLabel
from PySide6.QtGui import QPixmap,QPainter, QPen, QBrush, QImage

import tobii_research as tr

import global_config

global_gaze_data = []
global_error_count = 0
current_gaze_data = []
def gaze_data_callback(gaze_data):
     global global_gaze_data
     global current_gaze_data
     current_gaze_data = gaze_data
     global_gaze_data.append(gaze_data)

class ImageShowWidget(QWidget):
    class DisplayState(Enum):
        Image = 1
        GrayScreen = 2
        Pause = 3
        Start = 4
        Ready = 5
        Stop = 6
        Other = 7

    def __init__(self,parent=None):
        super().__init__(parent)
        self.init_ui()
        self.load_config()
        self.state = self.DisplayState.Start
        self.init_timer()
        self.init_connections()
        self.load_images()
        self.time = 0

    def init_ui(self):
        self.setObjectName('image_show_widget')
        self.resize(self.resolution[0],self.resolution[1])
        self.move(0,0)
        self.image_layout = QGridLayout(self)
        self.image_layout.setObjectName('image_layout')
        self.image_layout.setContentsMargins(0,0,0,0)
        self.image_layout.setSpacing(5)
        self.image_display = QLabel(self)
        self.image_display.setLineWidth(0)
        self.image_display.setAlignment(Qt.AlignCenter)
        self.image_display.setObjectName('image_display')
        self.image_layout.addWidget(self.image_display)

    def load_config(self):
        self.eyetracker_frequency = global_config.get_value('eyetracker','frequency',60)
        self.image_show_time = global_config.get_value('image_show','last_time',10)*1000
        self.image_show_interval = global_config.get_value('image_show','time_interval',3)*1000
        self.dir_imgdb = global_config.get_value('database','path')
        self.dir_eye_data = global_config.get_value('data','path')
        self.is_debug = global_config.get_value('mode','debug')
        self.detect_error_interval_ms = 400
        self.imgshow_timer_interval_ms = 1000
        self.image_suffix = ('.bmp','.png','.jpg','.jpeg')

    def init_timer(self):
        self.imgshow_timer = QTimer()
        self.imgshow_timer.stop()
        self.imgshow_timer.setInterval(self.imgshow_timer_interval_ms)
        self.detect_error_timer = QTimer()
        self.detect_error_timer.stop()
        self.detect_error_timer.setInterval(self.detect_error_interval_ms)

    def init_connections(self):
        self.imgshow_timer.timeout.connect(self.do_timer_timeout)
        self.other_error.connect(self.other_error_close)

    def load_images(self):
        self.image_num = 0
        self.image_list = []
        imgdb_exist = os.path.exists(self.dir_imgdb)
        if not imgdb_exist:
            self.other_error.emit('imgdb directory not exist')
            return
        ls_imgdb = os.listdir(self.dir_imgdb)
        for item in ls_imgdb:
            if item.endswith(self.image_suffix):
                self.image_list.append(item)
        self.image_num = len(self.image_list)
        random.shuffle(self.image_list)
        self.state = self.DisplayState.Ready


    # custom signals
    eye_detection_error = Signal()
    other_error = Signal(str)

    @Slot(str)
    def other_error_close(self,str=None):
        msg = 'fatal error：' + str
        QMessageBox.warning(self, u'fatal error', msg)
        self.close()

    @Slot(object)
    def begin_test(self,eyetracker = None):
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowFlag(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.eyetracker = eyetracker
        self.showFullScreen()

    @Slot()
    def continue_test(self):
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowFlag(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

    @Slot()
    def do_timer_timeout(self):
        global global_error_count
        global global_gaze_data
        self.time = self.time + self.imgshow_timer_interval_ms
        if self.state == self.DisplayState.Ready:
            self.image_display.setStyleSheet("background-color:#808080")
            self.cur_image_index = 0
            self.cur_image = QImage()
            self.cur_image.load(self.image_list[0])
            self.cur_pixmap = QPixmap.fromImage(self.cur_image)
            self.image_display.setPixmap(self.cur_pixmap)
            global_error_count = 0
            try:
                self.eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
            except:
                # print('ERROR!')
                self.eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
                global_gaze_data = []
                self.eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

        elif (self.state == self.DisplayState.Image) and (
            self.time>=self.image_show_time/self.imgshow_timer_interval_ms):
            self.eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)




    @Slot()
    def do_error_detection(self):
        global global_gaze_data
        global global_error_count
        global current_gaze_data
        if current_gaze_data == []:
            return
        if np.isnan(current_gaze_data['left_gaze_point_on_display_area'][0]) and np.isnan(
                current_gaze_data['right_gaze_point_on_display_area'][0]):
            global_error_count = global_error_count + 1
        else:
            global_error_count = 0
        if global_error_count == int(self.eyetracker_frequency * 0.75):
            self.error_detect_timer.stop()
            self.timer.stop()
            self.eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
            global_gaze_data = []
            del (self.EyeTrackTime[-1])
            global_error_count = 0
            dlgTitle = "信息框"
            strInfo = "眼动仪捕捉眼动信息失败，请调整坐姿"
            QMessageBox.information(self, dlgTitle, strInfo)
            self.close()
            self.ExpError.emit(True)

    def keyReleaseEvent(self, event):
        global global_gaze_data
        if event.key() == Qt.Key_P:
            self.pause()

        if event.key() == Qt.Key_Q:
            self.timer.stop()
            self.error_detect_timer.stop()
            self.eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
            global_gaze_data = []
            del (self.EyeTrackTime[-1])
            self.close()