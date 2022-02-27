QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++11

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    src/calibrationresultwidget.cpp \
    src/calibrationwidget.cpp \
    src/imageshowwidget.cpp \
    src/eyetrackerwrapper.cpp \
    src/infodialog.cpp \
    src/main.cpp \
    src/myconfig.cpp \
    src/settingdialog.cpp \
    src/startpanel.cpp

HEADERS += \
    include/calibrationresultwidget.h \
    include/calibrationwidget.h \
    include/imageshowwidget.h \
    include/eyetrackerwrapper.h \
    include/infodialog.h \
    include/myconfig.h \
    include/settingdialog.h \
    include/startpanel.h \
    include/mytypedef.h

TRANSLATIONS += \
    IPOID_addon1_cpp_zh_CN.ts
CONFIG += lrelease
CONFIG += embed_translations

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

FORMS += \
    ui/infodialog.ui \
    ui/settingdialog.ui \
    ui/startpanel.ui

DISTFILES += \
    IPOID_addon1_cpp_zh_CN.ts

INCLUDEPATH += $$PWD/include

unix:!macx{
HEADERS += include/linux/tobii_research.h \
           include/linux/tobii_research_calibration.h \
           include/linux/tobii_research_eyetracker.h \
           include/linux/tobii_research_streams.h
INCLUDEPATH += $$PWD/include/linux
LIBS += -L$$PWD/lib/linux -ltobii_research
}

win32{
HEADERS += include/win/tobii_research.h \
           include/win/tobii_research_calibration.h \
           include/win/tobii_research_eyetracker.h \
           include/win/tobii_research_streams.h
INCLUDEPATH += $$PWD/include/win
LIBS += -L$$PWD/lib/win -ltobii_research
}
