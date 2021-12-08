
import sys

from PySide6.QtWidgets import QApplication

from start_panel import StartPanel
from info_dialog import InfoDialog
from main_window import MainWindow

app = QApplication(sys.argv)

info_dialog = InfoDialog()
start_panel = StartPanel()
main_window = MainWindow()

info_dialog.begin_test.connect(start_panel.begin_setting)

info_dialog.ui_load.show()

sys.exit(app.exec_())

