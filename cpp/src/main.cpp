#include "infodialog.h"
#include "myconfig.h"
#include "startpanel.h"

#include <QApplication>
#include <QObject>
#include <QLocale>
#include <QTranslator>


MyConfig global_config;

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QTranslator translator;
    const QStringList uiLanguages = QLocale::system().uiLanguages();
    for (const QString &locale : uiLanguages) {
        const QString baseName = "IPOID_addon1_cpp_" + QLocale(locale).name();
        if (translator.load(":/i18n/" + baseName)) {
            app.installTranslator(&translator);
            break;
        }
    }

    InfoDialog info_dialog;
    info_dialog.show();
    // StartPanel start_panel;
    // QObject::connect(&info_dialog,SIGNAL(begin_setting(std::string)),&start_panel,SLOT(begin_setting(std::string)));
    return app.exec();
}
