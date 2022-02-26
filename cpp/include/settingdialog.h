#ifndef SETTINGDIALOG_H
#define SETTINGDIALOG_H

#include "myconfig.h"
#include <QDialog>
extern MyConfig global_config;
namespace Ui
{
    class SettingDialog;
}

class SettingDialog : public QDialog
{
    Q_OBJECT

public:
    explicit SettingDialog(QWidget *parent = nullptr);
    ~SettingDialog();
    void init_connections();
    void set_eyetracker_frequency_options();

private slots:
    void apply_setting();
    void on_buttonBox_accepted();

private:
    Ui::SettingDialog *ui;
    QVector<float> eyetracker_frequency_list;
    float default_eyetracker_frequency;
signals:
    void settings_changed();
};

#endif // SETTINGDIALOG_H
