# !/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from pathlib import Path
import sys
import json

from PySide6.QtWidgets import QApplication, QWidget, QMessageBox
from PySide6.QtCore import QFile, Slot, Signal
from PySide6.QtUiTools import QUiLoader

import global_config


class InfoDialog(QWidget):
    # custom signals
    signal_begin_test = Signal(str)

    def __init__(self):
        super(InfoDialog, self).__init__()
        self.ui_load = self.load_ui()
        self.ui_load.setWindowTitle('Information Fill')
        print(global_config.get_value('data', 'path', './outdata'))
        self.out_data_path = Path(global_config.get_value('data', 'path', './outdata')).absolute()
        self.info_path = './debug/'
        self.info_data = {}
        self.participant_info_file = './debug/participant_info.json'
        self.setup_connections()
        print(self.out_data_path)

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "ui" / "info_dialog.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        ui = loader.load(ui_file, self)
        ui_file.close()
        return ui

    def setup_connections(self):
        self.ui_load.btn_submit.clicked.connect(self.on_btn_submit_clicked)

    # custom slots
    @Slot(bool)
    def on_btn_submit_clicked(self):
        self.check_info()

    @Slot(bool)
    def slot_info_show(self):
        self.ui_load.show()

    # normal methods
    def check_info(self):
        flag_debug = global_config.get_value('mode', 'debug', False)
        if flag_debug:
            self.signal_begin_test.emit(self.info_path)
            self.terminate()
            return
        info_data = {}
        info_data['name'] = self.ui_load.tEdit_name.text()
        info_data['age'] = self.ui_load.tEdit_age.text()
        info_data['id'] = self.ui_load.tEdit_id.text()
        info_data['major'] = self.ui_load.tEdit_major.text()
        if self.ui_load.btn_man.isChecked():
            info_data['sex'] = '男'
        elif self.ui_load.btn_woman.isChecked():
            info_data['sex'] = '女'
        for field in ('name', 'age', 'id'):
            if info_data[field].strip() == '':
                msg_title = '信息填写错误'
                field_dict = {'name': '姓名', 'age': '年龄', 'id': '学号/编号'}
                msg_text = field_dict[field] + '未填写！'
                QMessageBox.warning(self.ui_load, msg_title, msg_text)
                return
        submit_choose = QMessageBox.question(self.ui_load, '信息提交确认','信息填写完成，是否确认提交？',
                                             QMessageBox.Yes | QMessageBox.Cancel,
                                             QMessageBox.Yes)
        if submit_choose == QMessageBox.Yes:
            self.info_data = info_data
            self.info_path = os.path.join(self.out_data_path, info_data['id'])
            if not os.path.exists(self.info_path):
                os.makedirs(self.info_path)
                self.terminate()
            else:
                cover = QMessageBox.question(self.ui_load, '提示', '该编号已存在，是否覆盖？\n 覆盖(Yes) 自动重编号(No) 修改编号(Cancel)',
                                             QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                             QMessageBox.No)
                if cover == QMessageBox.Yes:
                    self.terminate()
                elif cover == QMessageBox.No:
                    repeat_no = 1
                    repeat_str = '_rep' + str(repeat_no)
                    self.info_path = os.path.join(self.out_data_path, info_data['id'] + repeat_str)
                    while os.path.exists(self.info_path):
                        repeat_no = repeat_no + 1
                        repeat_str = '_rep' + str(repeat_no)
                        self.info_path = os.path.join(self.out_data_path, info_data['id'] + repeat_str)
                    os.makedirs(self.info_path)
                    self.terminate()
                else:
                    QMessageBox.information(self.ui_load, '取消覆盖', '你可以修改编号后再提交')
                    return
        else:
            QMessageBox.information(self.ui_load, '取消提交', '你可以继续填写信息')
            return

    def terminate(self):
        self.participant_info_file = os.path.join(self.info_path, 'participant_info.json')
        fid = open(self.participant_info_file, mode='w')
        json.dump(self.info_data, fid, ensure_ascii=False)
        fid.close()
        self.signal_begin_test.emit(self.info_path)
        self.ui_load.close()
        self.close()


if __name__ == "__main__":
    global_config.init()
    app = QApplication([])
    widget = InfoDialog()
    widget.ui_load.show()
    sys.exit(app.exec_())
