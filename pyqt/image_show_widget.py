# !/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import time
import random
import os
import datetime
import numpy as np
import json
from PySide6.QtCore import Qt, QTimer, Signal, Slot
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QMessageBox, QLabel
from PySide6.QtGui import QPixmap, QImage

import global_config

class ImageShowWidget(QWidget):
    # custom signals
    eye_detection_error = Signal(str)
    experiment_error = Signal(str)
    experiment_finished = Signal()
    experiment_pause = Signal(str)

    class DisplayState:
        Start = 0       # image show widget start / in experiment
        Ready = 1       # image show ready / pause
        Image = 2       # image show image / grayscreen
        Error = 3       # reserved for indicate error
        Finish = 4

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resolution = (1920,1080)
        self.load_config()
        self.init_ui()
        self.state = (1<<self.DisplayState.Start)
        self.init_timer()
        self.init_connections()
        self.load_images()
        self.countdown = 0

    def load_config(self):
        self.eyetracker_frequency = global_config.get_value('eyetracker', 'frequency', 60)
        self.image_show_time = global_config.get_value('image_show', 'last_time', 10) * 1000
        self.image_show_interval = global_config.get_value('image_show', 'time_interval', 3) * 1000
        self.dir_imgdb = global_config.get_value('database', 'path')
        self.dir_out_data = global_config.get_value('data', 'path')
        self.is_debug = global_config.get_value('mode', 'debug')
        self.detect_error_interval_ms = 20
        self.imgshow_timer_interval_ms = 100
        self.image_suffix = ('.bmp', '.png', '.jpg', '.jpeg')
        self.eye_detect_error_count = 0

    def init_ui(self):
        self.setObjectName('image_show_widget')
        self.resize(self.resolution[0], self.resolution[1])
        self.move(0, 0)
        self.image_layout = QGridLayout(self)
        self.image_layout.setObjectName('image_layout')
        self.image_layout.setContentsMargins(0, 0, 0, 0)
        self.image_layout.setSpacing(5)
        self.image_display = QLabel(self)
        self.image_display.setLineWidth(0)
        self.image_display.setAlignment(Qt.AlignCenter)
        self.image_display.setObjectName('image_display')
        self.image_display.setStyleSheet("background-color:#808080")
        self.image_layout.addWidget(self.image_display)

    def init_timer(self):
        self.imgshow_timer = QTimer()
        self.imgshow_timer.stop()
        self.imgshow_timer.setInterval(self.imgshow_timer_interval_ms)
        self.detect_error_timer = QTimer()
        self.detect_error_timer.stop()
        self.detect_error_timer.setInterval(self.detect_error_interval_ms)

    def init_connections(self):
        self.imgshow_timer.timeout.connect(self.do_timer_timeout)
        if global_config.eyetracker_wrapper.eyetracker:
            self.detect_error_timer.timeout.connect(self.do_error_detection)
            self.eye_detection_error.connect(self.pause)
        self.experiment_error.connect(self.pause)
        self.experiment_pause.connect(self.pause)
        self.experiment_finished.connect(self.close)

    def load_images(self):
        self.image_num = 0
        self.image_list = []
        self.cur_image_index = 0
        self.cur_image = QImage()
        imgdb_exist = os.path.exists(self.dir_imgdb)
        if not imgdb_exist:
            self.experiment_error.emit('imgdb directory not exist')
            return
        ls_imgdb = os.listdir(self.dir_imgdb)
        for item in ls_imgdb:
            if item.endswith(self.image_suffix):
                self.image_list.append(item)
        self.image_num = len(self.image_list)
        random.shuffle(self.image_list)
        self.state = self.state | (1<<self.DisplayState.Ready)

    def subscribe_eye_data(self):
        self.eye_detect_error_count = 0
        if self.eyetracker_wrap.eyetracker:
            if self.is_subscribed:
                self.eyetracker_wrap.clear_gaze_data()
            else:
                self.eyetracker_wrap.subscribe_gaze_data()
                self.is_subscribed = True
        else:
            if self.is_debug:
                if self.cur_image_index <= 0:
                    QMessageBox.information(self, '调试模式！', '未发现眼动仪，仅演示效果！')
            else:
                QMessageBox.warning(self,'警告','未发现眼动仪')

    def save_eye_data(self, filetype=('txt','json')):
        if 'txt' in filetype:
            fid = open(self.current_eye_data_file + '.txt', mode='a+')
            for gaze_data_sample in self.eyetracker_wrap.get_gaze_data():
                for gaze_dataf in gaze_data_sample:
                    data = gaze_data_sample[gaze_dataf]
                    fid.write(str(data) + ' ')
                fid.write('\n')
            fid.close()
        if 'json' in filetype:
            fid = open(self.current_eye_data_file + '.json', mode='a+')
            json.dump(self.eyetracker_wrap.get_gaze_data(), fid, indent=4, ensure_ascii=False)
            fid.close()


    @Slot(str)
    def begin_test(self, participant_id='debug'):
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.participant_id = participant_id
        self.eyetracker_wrap = global_config.eyetracker_wrapper
        self.cur_image_index = -1
        self.state = self.state |(1<<self.DisplayState.Image)
        self.countdown = 0
        self.eye_detect_error_count = 0
        self.is_subscribed = False
        self.do_timer_timeout()
        self.showFullScreen()

    @Slot(str)
    def continue_test(self,participant_id):
        # self.setWindowState(Qt.WindowMaximized)
        # self.setWindowFlag(Qt.FramelessWindowHint)
        self.participant_id = participant_id
        self.state = self.state | (1<<self.DisplayState.Ready)      # Ready bit set to 1
        self.countdown = 0
        if self.state | (1<<self.DisplayState.Image):
            self.cur_image_index = self.cur_image_index - 1
            self.state = self.state &(~(1<<self.DisplayState.Image))
        else:
            self.state = self.state | (1<<self.DisplayState.Image)
        self.is_subscribed = False
        self.do_timer_timeout()
        self.eye_detect_error_count = 0
        self.showFullScreen()

    @Slot()
    def do_timer_timeout(self):
        self.countdown = self.countdown - self.imgshow_timer_interval_ms
        if self.countdown < self.imgshow_timer_interval_ms:
            self.countdown = 0
            self.imgshow_timer.stop()
            if (self.state & (1 << self.DisplayState.Ready)):
                if self.state & (1<<self.DisplayState.Image):
                    if (self.state | (1<<self.DisplayState.Start)):
                        self.state = self.state & (~(1<<self.DisplayState.Start))
                    else:
                        self.save_eye_data(('txt','json'))
                    self.detect_error_timer.stop()
                    self.state = self.state & (~(1<<self.DisplayState.Image))
                    self.countdown = self.image_show_interval
                    self.cur_pixmap = QPixmap()
                    self.image_display.setPixmap(self.cur_pixmap)
                    self.imgshow_timer.start()
                else:
                    if self.cur_image_index < self.image_num-1:
                        self.cur_image_index = self.cur_image_index + 1
                        self.cur_image_name = self.image_list[self.cur_image_index].split('.')[0]
                        self.cur_image_file = os.path.join(self.dir_imgdb,self.image_list[self.cur_image_index])
                        self.cur_image.load(self.cur_image_file)
                        self.cur_pixmap = QPixmap.fromImage(self.cur_image)
                        self.image_display.setPixmap(self.cur_pixmap)
                        self.current_eye_data_file = os.path.join(self.dir_out_data,self.participant_id,self.cur_image_name)
                        time_str = datetime.datetime.now().strftime('%H:%M:%S.%f')
                        self.state = self.state | (1<<self.DisplayState.Image)
                        self.countdown = self.image_show_time
                        self.subscribe_eye_data()
                        self.imgshow_timer.start()
                        if self.eyetracker_wrap.eyetracker:
                            self.detect_error_timer.start()
                    else:
                        self.experiment_finished.emit()
                        return
            else:
                logging.error('enter imgshow timeout solver error')

    @Slot()
    def do_error_detection(self):
        current_gaze_data = self.eyetracker_wrap.get_current_gaze_data()
        if (len(current_gaze_data) == 0 or 
            (current_gaze_data['left_gaze_point_validity'] == 0 and 
             current_gaze_data['left_gaze_point_validity'] == 0)):
            self.eye_detect_error_count = self.eye_detect_error_count + 1
        else:
            self.eye_detect_error_count = 0
        if self.eye_detect_error_count >= int((self.image_show_time/self.detect_error_interval_ms) * 0.75):
            self.detect_error_timer.stop()
            self.imgshow_timer.stop()
            if (self.eyetracker_wrap.eyetracker):
                self.eyetracker_wrap.unsubscribe_gaze_data()
            self.eyetracker_wrap.clear_gaze_data()
            self.eye_detect_error_count = 0
            dlgTitle = "信息框"
            strInfo = "眼动仪捕捉眼动信息失败，请调整坐姿!"
            QMessageBox.information(self, dlgTitle, strInfo)
            self.eye_detection_error.emit('捕捉眼睛失败')

    @Slot(str)
    def pause(self, str=None):
        self.imgshow_timer.stop()
        self.detect_error_timer.stop()
        if (self.eyetracker_wrap.eyetracker):
            self.eyetracker_wrap.unsubscribe_gaze_data()
        self.state = self.state & (~(1<<self.DisplayState.Ready))
        self.close()
        pause_msg = u'程序暂停：' + str
        QMessageBox.warning(self, u'pause', pause_msg)
        

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_P:
            self.experiment_pause.emit('key pause')

        if event.key() == Qt.Key_Q:
            self.experiment_pause.emit('key quit')


if __name__ == '__main__':
    global_config.init()
    app = QApplication(sys.argv)
    w = ImageShowWidget()
    w.begin_test()
    sys.exit(app.exec_())
