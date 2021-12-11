# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frequency_setting2.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

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

class Ui_setting_dialog(object):
    def setupUi(self, setting_dialog):
        if not setting_dialog.objectName():
            setting_dialog.setObjectName(u"setting_dialog")
        setting_dialog.resize(272, 214)
        self.verticalLayout = QVBoxLayout(setting_dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.eyetracker_settings = QGroupBox(setting_dialog)
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

        self.buttonBox = QDialogButtonBox(setting_dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(setting_dialog)
        self.buttonBox.accepted.connect(setting_dialog.accept)
        self.buttonBox.rejected.connect(setting_dialog.reject)

        QMetaObject.connectSlotsByName(setting_dialog)
    # setupUi

    def retranslateUi(self, setting_dialog):
        setting_dialog.setWindowTitle(QCoreApplication.translate("setting_dialog", u"Dialog", None))
        self.eyetracker_settings.setTitle(QCoreApplication.translate("setting_dialog", u"\u773c\u52a8\u4eea\u53c2\u6570\u8bbe\u7f6e", None))
        self.frequency_label.setText(QCoreApplication.translate("setting_dialog", u"\u9891\u7387", None))
    # retranslateUi

