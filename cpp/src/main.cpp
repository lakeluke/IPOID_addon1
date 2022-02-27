#include "infodialog.h"
#include "myconfig.h"
#include "startpanel.h"

#include <QApplication>
#include <QLocale>
#include <QObject>
#include <QTranslator>

MyConfig global_config("./config.json");

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    QTranslator translator;
    const QStringList uiLanguages = QLocale::system().uiLanguages();
    for (const QString &locale : uiLanguages)
    {
        const QString baseName = "IPOID_addon1_cpp_" + QLocale(locale).name();
        if (translator.load(":/i18n/" + baseName))
        {
            app.installTranslator(&translator);
            break;
        }
    }

    InfoDialog *info_dialog = new InfoDialog();
    info_dialog->show();
    StartPanel *start_panel = new StartPanel();
    QObject::connect(info_dialog, SIGNAL(begin_setting(QString)), start_panel, SLOT(begin_setting(QString)));
    int ret_code = app.exec();
    delete info_dialog;
    delete start_panel;
    return ret_code;
}
