# !/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import logging
from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QApplication, QDialog

import global_config
from ui.ui_setting_dialog import Ui_setting_dialog


class SettingDialog(QDialog):
    # custom signals
    settings_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_setting_dialog()
        self.ui.setupUi(self)
        self.setWindowTitle(u"设置")
        self.eyetracker_frequency_list = (
            global_config.eyetracker_wrapper.frequency_options()
        )
        self.default_eyetracker_frequency = global_config.get_value(
            "eyetracker", "frequency", 60
        )
        self.set_eyetracker_frequency_options()
        self.init_connections()

    # class init methods
    def init_connections(self):
        self.settings_changed.connect(self.apply_settings)

    def set_eyetracker_frequency_options(self):
        for i in range(0, len(self.eyetracker_frequency_list)):
            self.ui.frequency_combobox.insertItem(
                i, str(self.eyetracker_frequency_list[i]) + "Hz"
            )
        self.ui.frequency_combobox.setCurrentText(
            str(self.default_eyetracker_frequency) + "Hz"
        )

    # custom slots
    @Slot()
    def on_buttonBox_accepted(self):
        self.settings_changed.emit()

    @Slot()
    def apply_settings(self):
        eyetracker_frequency = round(
            float(self.ui.frequency_combobox.currentText()[0:-2])
        )
        imgshow_time = int(self.ui.imgshow_time_value.text())
        imgshow_interval = int(self.ui.imgshow_interval_value.text())
        global_config.set_value("image_show", "last_time", imgshow_time)
        global_config.set_value("image_show", "time_interval", imgshow_interval)
        if global_config.eyetracker_wrapper.eyetracker:
            global_config.eyetracker_wrapper.set_frequency(eyetracker_frequency)
            current_frequency = global_config.eyetracker_wrapper.get_frequency()
            global_config.set_value("eyetracker", "frequency", current_frequency)
            logging.info(
                "eyetracker %s frequency is set to %d"
                % (global_config.eyetracker_wrapper.serial_number, current_frequency)
            )


if __name__ == "__main__":
    global_config.init()
    app = QApplication(sys.argv)
    w = SettingDialog()
    w.show()
    sys.exit(app.exec_())
