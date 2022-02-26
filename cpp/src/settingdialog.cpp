#include "settingdialog.h"
#include "ui_settingdialog.h"

SettingDialog::SettingDialog(QWidget *parent) : QDialog(parent),
                                                ui(new Ui::SettingDialog)
{
    ui->setupUi(this);
    this->eyetracker_frequency_list = global_config.get_eyetracker_wrapper()->get_frequency_options();
    this->default_eyetracker_frequency = global_config.get_value("eyetracker/frequency", 60).toFloat();
    this->set_eyetracker_frequency_options();
    this->init_connections();
}

SettingDialog::~SettingDialog()
{
    delete ui;
}

void SettingDialog::init_connections()
{
    connect(this, SIGNAL(settings_changed), this, SLOT(apply_setting));
};

void SettingDialog::set_eyetracker_frequency_options()
{
    for (int i = 0; i < this->eyetracker_frequency_list.size(); ++i)
        this->ui->frequency_combobox->insertItem(
            i, QString("%fHz").arg(this->eyetracker_frequency_list[i]));
    this->ui->frequency_combobox->setCurrentText(
        QString("%fHz").arg(this->default_eyetracker_frequency));
};

void SettingDialog::apply_setting()
{
    EyeTrackerWrapper *eyetracker_wrapper = global_config.get_eyetracker_wrapper();
    QString frequency_str = this->ui->frequency_combobox->currentText();
    float eyetracker_frequency = frequency_str.remove("Hz").toFloat();
    int imgshow_time = this->ui->imgshow_time_value->text().toInt();
    int imgshow_interval = this->ui->imgshow_interval_value->text().toInt();
    global_config.set_value("image_show/last_time", imgshow_time);
    global_config.set_value("image_show/time_interval", imgshow_interval);
    if (eyetracker_wrapper->eyetracker)
        eyetracker_wrapper->set_frequency(eyetracker_frequency);
    float current_frequency = eyetracker_wrapper->get_current_frequency();
    global_config.set_value("eyetracker/frequency", current_frequency);
    qInfo() << QString("eyetracker %s frequency is set to %f").arg(EyeTrackerWrapper::get_eyetracker_info(eyetracker_wrapper->eyetracker)["serial_number"].toString()).arg(current_frequency);
};

void SettingDialog::on_buttonBox_accepted()
{
    emit settings_changed();
};
