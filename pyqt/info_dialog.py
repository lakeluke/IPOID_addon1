# !/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import json
from pathlib import Path
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox
from PySide6.QtCore import Slot, Signal
from shiboken6.Shiboken import invalidate

import global_config
from ui.ui_info_dialog import Ui_InfoDialog

class InfoDialog(QWidget):
    # custom signals
    begin_setting = Signal(str)     # call the start_panel 

    def __init__(self):
        super(InfoDialog, self).__init__()
        self.ui = Ui_InfoDialog()
        self.ui.setupUi(self)
        self.setWindowTitle('实验参与者信息填写')
        
        self.is_debug = global_config.get_value('mode', 'debug', False)
        self.out_data_path = Path(global_config.get_value('data', 'path', './outdata')).absolute()
        self.participant_id = 'debug'
        self.info_path = os.path.join(self.out_data_path,self.participant_id)
        self.participant_info_file = os.path.join(self.info_path,'participant_info.json')
        self.info_data = {}
        
        self.setup_connections()


    def setup_connections(self):
        pass

    def check_info(self):
        # get input information
        info_data = {}
        info_data['name'] = self.ui.tEdit_name.text()
        info_data['age'] = self.ui.tEdit_age.text()
        info_data['id'] = self.ui.tEdit_id.text()
        info_data['major'] = self.ui.tEdit_major.text()
        if self.ui.btn_man.isChecked():
            info_data['sex'] = '男'
        elif self.ui.btn_woman.isChecked():
            info_data['sex'] = '女'
            
        # check if information is null   
        invalid_fields = []
        for field in ('name', 'age', 'id'):
            if info_data[field].strip() == '':
                invalid_fields.append(field)
        return invalid_fields,info_data
    
            
    # custom slots
    @Slot(bool)
    def info_show(self):
        self.show()
 
    @Slot()
    def on_btn_submit_clicked(self):
        invalid_fields,info_data = self.check_info()
        if len(invalid_fields):
            if self.is_debug:
                msg_title = '[Debug Mode]'
                invalid_fields_str = ''
                for field in invalid_fields:
                    invalid_fields_str = invalid_fields_str + field + ','
                msg_text = invalid_fields_str + "is invalid! id is set to 'debug'"
                QMessageBox.warning(self, msg_title, msg_text)
                info_data['id'] = self.participant_id
            else:
                msg_title = '信息填写错误'
                field_dict = {'name': '姓名', 'age': '年龄', 'id': '学号/编号'}
                invalid_fields_str = ''
                for field in invalid_fields:
                    invalid_fields_str = invalid_fields_str + field_dict[field] + ' '
                msg_text = invalid_fields_str + '未填写！'
                QMessageBox.warning(self, msg_title, msg_text)
                return
        submit_choose = QMessageBox.question(self, '信息提交确认', '信息填写完成，是否确认提交？',
                                             QMessageBox.Yes | QMessageBox.Cancel,
                                             QMessageBox.Yes)
        if submit_choose == QMessageBox.Yes:
            self.info_data = info_data
            self.participant_id = info_data['id']
            self.info_path = os.path.join(self.out_data_path, self.participant_id)
            if not os.path.exists(self.info_path):
                os.makedirs(self.info_path)
                self.terminate()
            else:
                cover = QMessageBox.question(self, '提示', '该编号已存在，是否覆盖？\n 覆盖(Yes) 自动重编号(No) 修改编号(Cancel)',
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
                    QMessageBox.information(self, '取消覆盖', '你可以修改编号后再提交')
                    return
        else:
            QMessageBox.information(self, '取消提交', '你可以继续填写信息')
            return

    # normal methods
    def terminate(self):
        self.participant_info_file = os.path.join(self.info_path, 'participant_info.json')
        fid = open(self.participant_info_file, mode='w+')
        json.dump(self.info_data, fid, indent=4, ensure_ascii=False)
        fid.close()
        self.begin_setting.emit(self.participant_id)
        self.close()


if __name__ == "__main__":
    global_config.init()
    app = QApplication([])
    widget = InfoDialog()
    widget.show()
    sys.exit(app.exec_())
