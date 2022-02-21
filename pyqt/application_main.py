# !/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

from PySide6.QtWidgets import QApplication

from start_panel import StartPanel
from info_dialog import InfoDialog
import global_config

global_config.init()

app = QApplication(sys.argv)

info_dialog = InfoDialog()
start_panel = StartPanel()

info_dialog.begin_setting.connect(start_panel.begin_setting)

info_dialog.info_show()

sys.exit(app.exec_())

