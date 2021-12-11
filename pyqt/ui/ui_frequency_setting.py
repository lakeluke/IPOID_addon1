# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frequency_setting.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QPushButton, QRadioButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_frequency_setting(object):
    def setupUi(self, frequency_setting):
        if not frequency_setting.objectName():
            frequency_setting.setObjectName(u"frequency_setting")
        frequency_setting.resize(250, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frequency_setting.sizePolicy().hasHeightForWidth())
        frequency_setting.setSizePolicy(sizePolicy)
        frequency_setting.setMinimumSize(QSize(250, 300))
        frequency_setting.setMaximumSize(QSize(500, 600))
        self.centralwidget = QWidget(frequency_setting)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_freq = QFrame(self.centralwidget)
        self.frame_freq.setObjectName(u"frame_freq")
        self.frame_freq.setFrameShape(QFrame.StyledPanel)
        self.frame_freq.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_freq)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_freq_setting = QLabel(self.frame_freq)
        self.label_freq_setting.setObjectName(u"label_freq_setting")
        font = QFont()
        font.setFamilies([u"Consolas"])
        font.setPointSize(12)
        font.setBold(True)
        self.label_freq_setting.setFont(font)
        self.label_freq_setting.setLayoutDirection(Qt.LeftToRight)
        self.label_freq_setting.setFrameShape(QFrame.NoFrame)
        self.label_freq_setting.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_freq_setting)

        self.frame_freq_select = QFrame(self.frame_freq)
        self.frame_freq_select.setObjectName(u"frame_freq_select")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.frame_freq_select.sizePolicy().hasHeightForWidth())
        self.frame_freq_select.setSizePolicy(sizePolicy1)
        self.frame_freq_select.setMinimumSize(QSize(100, 150))
        self.frame_freq_select.setMaximumSize(QSize(600, 500))
        self.frame_freq_select.setFrameShape(QFrame.Box)
        self.frame_freq_select.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_freq_select)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.radio_60Hz = QRadioButton(self.frame_freq_select)
        self.radio_60Hz.setObjectName(u"radio_60Hz")
        sizePolicy.setHeightForWidth(self.radio_60Hz.sizePolicy().hasHeightForWidth())
        self.radio_60Hz.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setPointSize(12)
        self.radio_60Hz.setFont(font1)
        self.radio_60Hz.setLayoutDirection(Qt.LeftToRight)
        self.radio_60Hz.setChecked(True)
        self.radio_60Hz.setAutoRepeat(False)

        self.verticalLayout_2.addWidget(self.radio_60Hz, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.radio_120Hz = QRadioButton(self.frame_freq_select)
        self.radio_120Hz.setObjectName(u"radio_120Hz")
        sizePolicy.setHeightForWidth(self.radio_120Hz.sizePolicy().hasHeightForWidth())
        self.radio_120Hz.setSizePolicy(sizePolicy)
        self.radio_120Hz.setFont(font1)

        self.verticalLayout_2.addWidget(self.radio_120Hz, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.radio_250Hz = QRadioButton(self.frame_freq_select)
        self.radio_250Hz.setObjectName(u"radio_250Hz")
        sizePolicy.setHeightForWidth(self.radio_250Hz.sizePolicy().hasHeightForWidth())
        self.radio_250Hz.setSizePolicy(sizePolicy)
        self.radio_250Hz.setFont(font1)

        self.verticalLayout_2.addWidget(self.radio_250Hz, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.radio_300Hz = QRadioButton(self.frame_freq_select)
        self.radio_300Hz.setObjectName(u"radio_300Hz")
        sizePolicy.setHeightForWidth(self.radio_300Hz.sizePolicy().hasHeightForWidth())
        self.radio_300Hz.setSizePolicy(sizePolicy)
        self.radio_300Hz.setFont(font1)
        self.radio_300Hz.setLayoutDirection(Qt.LeftToRight)

        self.verticalLayout_2.addWidget(self.radio_300Hz, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 1)
        self.verticalLayout_2.setStretch(3, 1)

        self.verticalLayout_3.addWidget(self.frame_freq_select)

        self.btn_confirm = QPushButton(self.frame_freq)
        self.btn_confirm.setObjectName(u"btn_confirm")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.btn_confirm.sizePolicy().hasHeightForWidth())
        self.btn_confirm.setSizePolicy(sizePolicy2)
        font2 = QFont()
        font2.setPointSize(14)
        self.btn_confirm.setFont(font2)

        self.verticalLayout_3.addWidget(self.btn_confirm)

        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 6)
        self.verticalLayout_3.setStretch(2, 1)

        self.verticalLayout.addWidget(self.frame_freq)

        frequency_setting.setCentralWidget(self.centralwidget)

        self.retranslateUi(frequency_setting)

        QMetaObject.connectSlotsByName(frequency_setting)
    # setupUi

    def retranslateUi(self, frequency_setting):
        frequency_setting.setWindowTitle(QCoreApplication.translate("frequency_setting", u"MainWindow", None))
        self.label_freq_setting.setText(QCoreApplication.translate("frequency_setting", u"\u9891\u7387\u8bbe\u7f6e", None))
        self.radio_60Hz.setText(QCoreApplication.translate("frequency_setting", u"60Hz", None))
        self.radio_120Hz.setText(QCoreApplication.translate("frequency_setting", u"120Hz", None))
        self.radio_250Hz.setText(QCoreApplication.translate("frequency_setting", u"250Hz", None))
        self.radio_300Hz.setText(QCoreApplication.translate("frequency_setting", u"300Hz", None))
        self.btn_confirm.setText(QCoreApplication.translate("frequency_setting", u"\u786e\u8ba4", None))
    # retranslateUi

