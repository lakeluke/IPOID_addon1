#ifndef INFODIALOG_H
#define INFODIALOG_H

#include "myconfig.h"
#include <QDialog>
#include <QDir>
#include <QHash>
#include <QString>
#include <QVector>

extern MyConfig global_config;

QT_BEGIN_NAMESPACE
namespace Ui
{
    class InfoDialog;
}
QT_END_NAMESPACE

class InfoDialog : public QDialog
{
    Q_OBJECT
signals:
    void begin_setting(QString);
public:
    InfoDialog(QWidget *parent = nullptr);
    ~InfoDialog();

private:
    Ui::InfoDialog *ui;
    bool is_debug;
    QDir out_data_path;
    QDir info_path;
    QVariantHash info_data;
    QString participant_id;
    QFile participant_info_file;

    void setup_connections();
    QStringList check_info();
    void terminate();

public slots:
    void info_show() { this->show(); };
    void on_btn_submit_clicked();
};
#endif // INFODIALOG_H
