import sys

from PySide6.QtCore import (Signal, Slot)
from PySide6.QtWidgets import (QApplication,QDialog)

from ui.ui_setting_dialog import Ui_setting_dialog

import global_config

class SettingDialog(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_setting_dialog()
        self.ui.setupUi(self)
        self.eyetracker_frequency_list = (60,120,250,300)
        self.default_eyetracker_frequency = global_config.get_value('eyetracker','frequency',60)
        self.set_eyetracker_frequency_options()
        self.init_connections()
    # custom signals
    settings_changed = Signal(dict)

    # class init methods
    def init_connections(self):
        self.ui.buttonBox.accepted.connect(self.on_buttonBox_accepted)


    def set_eyetracker_frequency_options(self):
        for i in range(0,len(self.eyetracker_frequency_list)):
            self.ui.frequency_combobox.insertItem(i, str(self.eyetracker_frequency_list[i])+'Hz')
        self.ui.frequency_combobox.setCurrentText(str(self.default_eyetracker_frequency)+'Hz')

    # custom slots
    @Slot()
    def on_buttonBox_accepted(self):
        settings = {'eyetracker':{},
                    'image_show':{}
                    }
        settings['eyetracker']['frequency'] = int(self.ui.frequency_combobox.currentText()[0:-2])
        settings['image_show']['last_time'] = int(self.ui.imgshow_time_value.text())
        settings['image_show']['time_interval'] =  int(self.ui.imgshow_interval_value.text())
        self.settings_changed.emit(settings)



if __name__ == '__main__':
    global_config.init()
    app = QApplication(sys.argv)
    w =SettingDialog()
    w.show()
    sys.exit(app.exec_())