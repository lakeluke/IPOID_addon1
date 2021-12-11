# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setting_dialog.ui'
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
    QLineEdit, QSizePolicy, QVBoxLayout, QWidget)

class Ui_setting_dialog(object):
    def setupUi(self, setting_dialog):
        if not setting_dialog.objectName():
            setting_dialog.setObjectName(u"setting_dialog")
        setting_dialog.resize(285, 340)
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

        self.imgshow_settings = QGroupBox(setting_dialog)
        self.imgshow_settings.setObjectName(u"imgshow_settings")
        self.formLayout_2 = QFormLayout(self.imgshow_settings)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.imgshow_time_label = QLabel(self.imgshow_settings)
        self.imgshow_time_label.setObjectName(u"imgshow_time_label")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.imgshow_time_label)

        self.imgshow_time_value = QLineEdit(self.imgshow_settings)
        self.imgshow_time_value.setObjectName(u"imgshow_time_value")
        self.imgshow_time_value.setCursorMoveStyle(Qt.VisualMoveStyle)
        self.imgshow_time_value.setClearButtonEnabled(False)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.imgshow_time_value)

        self.imgshow_interval_label = QLabel(self.imgshow_settings)
        self.imgshow_interval_label.setObjectName(u"imgshow_interval_label")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.imgshow_interval_label)

        self.imgshow_interval_value = QLineEdit(self.imgshow_settings)
        self.imgshow_interval_value.setObjectName(u"imgshow_interval_value")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.imgshow_interval_value)


        self.verticalLayout.addWidget(self.imgshow_settings)

        self.buttonBox = QDialogButtonBox(setting_dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

#if QT_CONFIG(shortcut)
        self.frequency_label.setBuddy(self.frequency_combobox)
        self.imgshow_time_label.setBuddy(self.imgshow_time_value)
        self.imgshow_interval_label.setBuddy(self.imgshow_interval_value)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(setting_dialog)
        self.buttonBox.accepted.connect(setting_dialog.accept)
        self.buttonBox.rejected.connect(setting_dialog.reject)

        QMetaObject.connectSlotsByName(setting_dialog)
    # setupUi

    def retranslateUi(self, setting_dialog):
        setting_dialog.setWindowTitle(QCoreApplication.translate("setting_dialog", u"Dialog", None))
        self.eyetracker_settings.setTitle(QCoreApplication.translate("setting_dialog", u"\u773c\u52a8\u4eea\u53c2\u6570\u8bbe\u7f6e", None))
        self.frequency_label.setText(QCoreApplication.translate("setting_dialog", u"\u9891\u7387", None))
        self.frequency_combobox.setCurrentText("")
        self.imgshow_settings.setTitle(QCoreApplication.translate("setting_dialog", u"\u56fe\u7247\u663e\u793a\u8bbe\u7f6e", None))
        self.imgshow_time_label.setText(QCoreApplication.translate("setting_dialog", u"\u56fe\u7247\u663e\u793a\u65f6\u95f4(\u6beb\u79d2ms)", None))
        self.imgshow_time_value.setInputMask(QCoreApplication.translate("setting_dialog", u"99999;-", None))
        self.imgshow_time_value.setText(QCoreApplication.translate("setting_dialog", u"10000", None))
        self.imgshow_interval_label.setText(QCoreApplication.translate("setting_dialog", u"\u56fe\u7247\u663e\u793a\u95f4\u9694(\u6beb\u79d2ms)", None))
        self.imgshow_interval_value.setInputMask(QCoreApplication.translate("setting_dialog", u"99999;-", u"1-999999"))
        self.imgshow_interval_value.setText(QCoreApplication.translate("setting_dialog", u"03000", None))
    # retranslateUi

