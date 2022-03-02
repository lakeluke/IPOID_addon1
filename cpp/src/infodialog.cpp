#include "infodialog.h"
#include "ui_infodialog.h"

#include <QJsonDocument>
#include <QJsonObject>
#include <QMessageBox>
#include <QtDebug>

InfoDialog::InfoDialog(QWidget *parent)
    : QDialog(parent), ui(new Ui::InfoDialog)
{
    ui->setupUi(this);
    this->setWindowTitle(tr("实验参与者信息填写"));
    this->is_debug = global_config.get_value("mode/debug", false).toBool();
    this->out_data_path = global_config.get_value("data/path", "./outdata").toString();
    this->participant_id = tr("debug");
    this->info_path = this->out_data_path.absoluteFilePath(this->participant_id);
    this->info_data = {{"name", ""}, {"age", ""}, {"id", ""}, {"major", ""}, {"sex", ""}};

    this->setup_connections();
}

InfoDialog::~InfoDialog()
{
    delete ui;
}

void InfoDialog::setup_connections(){};

QStringList InfoDialog::check_info()
{
    info_data["name"] = this->ui->tEdit_name->text();
    info_data["age"] = this->ui->tEdit_age->text();
    info_data["id"] = this->ui->tEdit_id->text();
    info_data["major"] = this->ui->tEdit_major->text();
    if (this->ui->btn_man->isChecked())
        info_data["sex"] = tr("男");
    else if (this->ui->btn_woman->isChecked())
        info_data["sex"] = tr("女");
    QStringList invalid_fields;
    QStringList fields_to_check = {"name", "age", "id"};
    for (QString &field : fields_to_check)
    {
        if (info_data.contains(field))
        {
            QString value = info_data[field].toString().trimmed();
            if (value.size() == 0)
                invalid_fields.append(field);
        }
        else
        {
            qCritical() << tr("can't find field %1 in QHash info_data").arg(field);
        }
    }
    return invalid_fields;
};

void InfoDialog::terminate()
{
    this->participant_info_file.setFileName(this->info_path.absoluteFilePath("participant_info.json"));
    QJsonObject info_obj = QJsonObject::fromVariantHash(this->info_data);
    QJsonDocument info_doc(info_obj);
    bool ok = this->participant_info_file.open(QIODevice::WriteOnly);
    if (ok)
    {
        this->participant_info_file.write(info_doc.toJson());
        this->participant_info_file.close();
        qInfo() << "participant info json file write success!";
    }
    else
    {
        qDebug() << "participant info json file write error!";
    }
    emit begin_setting(this->participant_id);
    this->close();
};

void InfoDialog::on_btn_submit_clicked()
{
    QStringList invalid_fields = this->check_info();
    if (invalid_fields.size())
    {
        QString msg_title = tr("信息填写错误");
        QHash<QString, QString> field_dict = {{"name", tr("姓名")}, {"age", tr("年龄")}, {"id", tr("学号/编号")}};
        QString invalid_fields_str;
        for (QString &field : invalid_fields)
        {
            invalid_fields_str.append(field_dict[field]).append(" ");
        }
        invalid_fields_str.append(tr("未填写!"));
        QMessageBox::warning(this, msg_title, invalid_fields_str);
        if (!this->is_debug)
            return;
        else
        {
            QString msg_text = invalid_fields_str.append("is invalid! id is set to 'debug'");
            QMessageBox::warning(this, msg_title, msg_text);
            this->info_data["id"] = this->participant_id;
            this->terminate();
            return;
        }
    }
    QMessageBox::StandardButton submit_choose = QMessageBox::question(this,
                                                                      tr("信息提交确认"),
                                                                      tr("信息填写完成,是否确认提交？"),
                                                                      QMessageBox::Yes | QMessageBox::Cancel,
                                                                      QMessageBox::Yes);
    if (submit_choose == QMessageBox::Yes)
    {
        this->participant_id = this->info_data["id"].toString();
        this->info_path = this->out_data_path.absoluteFilePath(this->participant_id);
        if (!this->info_path.exists())
        {
            this->out_data_path.mkpath(this->participant_id);
            this->terminate();
        }
        else
        {
            QMessageBox::StandardButton is_cover = QMessageBox::question(this,
                                                                         tr("提示"),
                                                                         tr("该编号已存在，是否覆盖？ \n"
                                                                            "覆盖(Yes) 自动重编号(No) 手动修改编号(Cancel)"),
                                                                         QMessageBox::Yes | QMessageBox::No | QMessageBox::Cancel,
                                                                         QMessageBox::No);
            if (is_cover == QMessageBox::Yes)
                this->terminate();
            else if (is_cover == QMessageBox::No)
            {
                int repeat_no = 1;
                QString repeat_str = QString("_rep%1").arg(repeat_no);
                this->info_path = this->out_data_path.absoluteFilePath(this->participant_id + repeat_str);
                while (this->info_path.exists())
                {
                    repeat_no += 1;
                    repeat_str = QString("_rep%1").arg(repeat_no);
                    this->info_path = this->out_data_path.absoluteFilePath(this->participant_id + repeat_str);
                }
                this->participant_id += repeat_str;
                this->info_path.mkpath(this->info_path.absolutePath());
                this->terminate();
            } 
            else
            {
                QMessageBox::information(this, tr("取消覆盖"), tr("你可以修改编号后再提交"));
                return;
            }
        }
    }
    else
    {
        QMessageBox::information(this, tr("取消提交"), tr("你可以继续填写信息"));
        return;
    }
};
