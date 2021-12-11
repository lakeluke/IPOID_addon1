from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFormLayout, QGroupBox, QLabel,
    QSizePolicy, QVBoxLayout, QWidget)


class SettingDialog(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.init_ui()


    def init_ui(self):
        self.setObjectName(u"setting_dialog")
        self.resize(300, 200)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.eyetracker_settings = QGroupBox(self)
        self.eyetracker_settings.setObjectName(u"eyetracker_settings")
        self.formLayout = QFormLayout(self.eyetracker_settings)
        self.formLayout.setObjectName(u"formLayout")

        self.frequency_label = QLabel(self.eyetracker_settings)
        self.frequency_label.setObjectName(u"frequency_label")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.frequency_label)
        self.frequency_combobox = QComboBox(self.eyetracker_settings)
        self.frequency_combobox.setObjectName(u"frequency_combobox")
        self.frequency_combobox.setEditable(False)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.frequency_combobox)

        self.verticalLayout.addWidget(self.eyetracker_settings)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("setting_dialog", u"Dialog", None))
        self.eyetracker_settings.setTitle(
            QCoreApplication.translate("setting_dialog", u"\u773c\u52a8\u4eea\u53c2\u6570\u8bbe\u7f6e", None))
        self.frequency_label.setText(QCoreApplication.translate("setting_dialog", u"\u9891\u7387", None))