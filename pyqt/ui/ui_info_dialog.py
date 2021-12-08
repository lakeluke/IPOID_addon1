# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'info_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QWidget)

class Ui_InfoDialog(object):
    def setupUi(self, InfoDialog):
        if not InfoDialog.objectName():
            InfoDialog.setObjectName(u"InfoDialog")
        InfoDialog.resize(556, 419)
        self.gridLayout_2 = QGridLayout(InfoDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.groupBox_participant_info = QGroupBox(InfoDialog)
        self.groupBox_participant_info.setObjectName(u"groupBox_participant_info")
        font = QFont()
        font.setPointSize(14)
        self.groupBox_participant_info.setFont(font)
        self.gridLayout = QGridLayout(self.groupBox_participant_info)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_2 = QGroupBox(self.groupBox_participant_info)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setFont(font)
        self.horizontalLayout = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_man = QRadioButton(self.groupBox_2)
        self.btn_man.setObjectName(u"btn_man")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_man.sizePolicy().hasHeightForWidth())
        self.btn_man.setSizePolicy(sizePolicy1)
        self.btn_man.setChecked(True)

        self.horizontalLayout.addWidget(self.btn_man)

        self.btn_woman = QRadioButton(self.groupBox_2)
        self.btn_woman.setObjectName(u"btn_woman")
        sizePolicy1.setHeightForWidth(self.btn_woman.sizePolicy().hasHeightForWidth())
        self.btn_woman.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.btn_woman)


        self.gridLayout.addWidget(self.groupBox_2, 0, 3, 2, 3)

        self.label_name = QLabel(self.groupBox_participant_info)
        self.label_name.setObjectName(u"label_name")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_name.sizePolicy().hasHeightForWidth())
        self.label_name.setSizePolicy(sizePolicy2)
        self.label_name.setFont(font)

        self.gridLayout.addWidget(self.label_name, 0, 0, 1, 1)

        self.tEdit_name = QLineEdit(self.groupBox_participant_info)
        self.tEdit_name.setObjectName(u"tEdit_name")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(8)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.tEdit_name.sizePolicy().hasHeightForWidth())
        self.tEdit_name.setSizePolicy(sizePolicy3)
        self.tEdit_name.setFont(font)

        self.gridLayout.addWidget(self.tEdit_name, 0, 2, 1, 1)

        self.tEdit_major = QLineEdit(self.groupBox_participant_info)
        self.tEdit_major.setObjectName(u"tEdit_major")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(9)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.tEdit_major.sizePolicy().hasHeightForWidth())
        self.tEdit_major.setSizePolicy(sizePolicy4)
        self.tEdit_major.setFont(font)

        self.gridLayout.addWidget(self.tEdit_major, 3, 2, 1, 4)

        self.tEdit_id = QLineEdit(self.groupBox_participant_info)
        self.tEdit_id.setObjectName(u"tEdit_id")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(9)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.tEdit_id.sizePolicy().hasHeightForWidth())
        self.tEdit_id.setSizePolicy(sizePolicy5)
        self.tEdit_id.setFont(font)
        self.tEdit_id.setMaxLength(10)

        self.gridLayout.addWidget(self.tEdit_id, 2, 2, 1, 4)

        self.label_major = QLabel(self.groupBox_participant_info)
        self.label_major.setObjectName(u"label_major")
        sizePolicy2.setHeightForWidth(self.label_major.sizePolicy().hasHeightForWidth())
        self.label_major.setSizePolicy(sizePolicy2)
        self.label_major.setFont(font)

        self.gridLayout.addWidget(self.label_major, 3, 0, 1, 1)

        self.label_id = QLabel(self.groupBox_participant_info)
        self.label_id.setObjectName(u"label_id")
        sizePolicy2.setHeightForWidth(self.label_id.sizePolicy().hasHeightForWidth())
        self.label_id.setSizePolicy(sizePolicy2)
        self.label_id.setFont(font)

        self.gridLayout.addWidget(self.label_id, 2, 0, 1, 2)

        self.horizontalSpacer = QSpacerItem(425, 24, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 4, 0, 1, 5)

        self.label_age = QLabel(self.groupBox_participant_info)
        self.label_age.setObjectName(u"label_age")
        sizePolicy2.setHeightForWidth(self.label_age.sizePolicy().hasHeightForWidth())
        self.label_age.setSizePolicy(sizePolicy2)
        self.label_age.setFont(font)

        self.gridLayout.addWidget(self.label_age, 1, 0, 1, 1)

        self.btn_submit = QPushButton(self.groupBox_participant_info)
        self.btn_submit.setObjectName(u"btn_submit")
        sizePolicy1.setHeightForWidth(self.btn_submit.sizePolicy().hasHeightForWidth())
        self.btn_submit.setSizePolicy(sizePolicy1)
        self.btn_submit.setFont(font)

        self.gridLayout.addWidget(self.btn_submit, 4, 5, 1, 1)

        self.tEdit_age = QLineEdit(self.groupBox_participant_info)
        self.tEdit_age.setObjectName(u"tEdit_age")
        sizePolicy3.setHeightForWidth(self.tEdit_age.sizePolicy().hasHeightForWidth())
        self.tEdit_age.setSizePolicy(sizePolicy3)
        self.tEdit_age.setFont(font)
        self.tEdit_age.setMaxLength(2)

        self.gridLayout.addWidget(self.tEdit_age, 1, 2, 1, 1)

        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 1)
        self.gridLayout.setRowStretch(3, 1)
        self.gridLayout.setRowStretch(4, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 5)
        self.gridLayout.setColumnStretch(3, 1)
        self.gridLayout.setColumnStretch(4, 1)
        self.gridLayout.setColumnStretch(5, 1)

        self.gridLayout_2.addWidget(self.groupBox_participant_info, 0, 0, 1, 1)

        QWidget.setTabOrder(self.tEdit_name, self.tEdit_age)
        QWidget.setTabOrder(self.tEdit_age, self.btn_man)
        QWidget.setTabOrder(self.btn_man, self.btn_woman)
        QWidget.setTabOrder(self.btn_woman, self.tEdit_id)
        QWidget.setTabOrder(self.tEdit_id, self.tEdit_major)
        QWidget.setTabOrder(self.tEdit_major, self.btn_submit)

        self.retranslateUi(InfoDialog)

        QMetaObject.connectSlotsByName(InfoDialog)
    # setupUi

    def retranslateUi(self, InfoDialog):
        InfoDialog.setWindowTitle(QCoreApplication.translate("InfoDialog", u"Dialog", None))
        self.groupBox_participant_info.setTitle(QCoreApplication.translate("InfoDialog", u"\u8bf7\u586b\u5199\u60a8\u7684\u6d4b\u8bd5\u4fe1\u606f", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("InfoDialog", u"\u6027\u522b", None))
        self.btn_man.setText(QCoreApplication.translate("InfoDialog", u"\u7537", None))
        self.btn_woman.setText(QCoreApplication.translate("InfoDialog", u"\u5973", None))
        self.label_name.setText(QCoreApplication.translate("InfoDialog", u"\u59d3\u540d\uff1a", None))
        self.tEdit_id.setInputMask(QCoreApplication.translate("InfoDialog", u"9999999999;_", None))
        self.label_major.setText(QCoreApplication.translate("InfoDialog", u"\u4e13\u4e1a\uff1a", None))
        self.label_id.setText(QCoreApplication.translate("InfoDialog", u"\u6d4b\u8bd5\u7f16\u53f7\uff1a", None))
        self.label_age.setText(QCoreApplication.translate("InfoDialog", u"\u5e74\u9f84\uff1a", None))
        self.btn_submit.setText(QCoreApplication.translate("InfoDialog", u"\u786e\u5b9a", None))
        self.tEdit_age.setInputMask(QCoreApplication.translate("InfoDialog", u"99;_", None))
    # retranslateUi

