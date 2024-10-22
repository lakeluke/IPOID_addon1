#include "startpanel.h"
#include "ui_startpanel.h"
#include <QDir>
#include <QFileDialog>
#include <QMessageBox>
#include <QtMath>

static TobiiResearchUserPositionGuide global_user_position;
void user_position_guide_callback(TobiiResearchUserPositionGuide *user_position_guide, void *user_data)
{
    memcpy(user_data, user_position_guide, sizeof(*user_position_guide));
};
StartPanel::EyePosShow::EyePosShow(QWidget *parent) : QWidget(parent)
{
    this->eye_pos_adcs[0] = {0, 0, 0}; // left_eye_pos
    this->eye_pos_adcs[1] = {0, 0, 0}; // right_eye_pos
    this->current_rad = 10;
    this->IsPainter = false;
};

void StartPanel::EyePosShow::paintEvent(QPaintEvent *event)
{
    QWidget::paintEvent(event);
    if (this->IsPainter == true)
    {
        this->W = this->width();
        this->H = this->height() * 0.8;
        QPainter painter;
        painter.begin(this);
        {
            QPen pen = QPen(Qt::white, 1, Qt::SolidLine);
            painter.setPen(pen);
            QBrush brush = QBrush(Qt::white, Qt::SolidPattern);
            painter.setBrush(brush);
            QRect rect_status = QRect(0, 0.9 * this->height(),
                                      this->width(), 0.1 * this->height());
            QRect rect_pos = QRect(0, 0,
                                   this->width(), 0.9 * this->height());
            painter.fillRect(rect_pos, Qt::black);
            // paint two eye position
            int eye_find = 0;
            for (auto point_pos : this->eye_pos_adcs)
            {
                if (point_pos[0] > 0 && point_pos[0] < 1 &&
                    point_pos[1] > 0 && point_pos[0] < 1)
                {
                    float relative_x = 1 - point_pos[0];
                    float relative_y = point_pos[1];
                    painter.drawEllipse(
                        QPoint(relative_x * this->W, relative_y * this->H),
                        this->current_rad, this->current_rad);
                    eye_find++;
                }
            }
            // change rect_status color
            if (eye_find == 0)
                painter.fillRect(rect_status, Qt::red);
            else if (eye_find == 1)
                painter.fillRect(rect_status, Qt::yellow);
            else if (eye_find == 2)
                painter.fillRect(rect_status, Qt::green);
        }
        painter.end();
    }
};

StartPanel::StartPanel(QWidget *parent) : QMainWindow(parent),
                                          ui(new Ui::StartPanel)
{
    ui->setupUi(this);
    this->setWindowTitle("实验主控制台");
    this->ui->btn_calibration->setEnabled(false);
    this->ui->btn_start->setEnabled(false);
    this->eye_show = new EyePosShow(ui->widget_eyepos);
    this->eye_show->setObjectName("eye_show");
    this->ui->widget_eyepos_layout->addWidget(this->eye_show);

    // init some params
    this->is_calibrated = false;
    this->eyetracker_frequency = global_config.get_value("eyetracker/frequency", 60.0f).toFloat();
    this->is_debug = global_config.get_value("mode/debug", true).toBool();
    this->dir_imgdb = global_config.get_value("database/path", "./imgdb").toString();
    this->ui->lineEdit_imgdb_dir->setText(this->dir_imgdb);
    this->participant_id = "debug";
    this->eyetracker_wrap = global_config.get_eyetracker_wrapper();
    this->experiment_started = false;
    this->eyetracker_subscribed = false;
    this->timer = new QTimer();
    this->timer->stop();
    this->timer->setInterval(40);
    this->init_connections();
};

StartPanel::~StartPanel()
{
    delete ui;
    delete timer;
};

void StartPanel::init_connections()
{
    connect(this->timer, SIGNAL(timeout()), this, SLOT(do_timer_timeout()));
};

void StartPanel::on_action_setting_triggered()
{
    this->eyetracker_wrap->unsubscribe_user_position(user_position_guide_callback);
    this->eyetracker_subscribed = false;
    this->setting_dialog = new SettingDialog(this);
    connect(this->setting_dialog,SIGNAL(settings_changed()),this,SLOT(on_btn_start_eyetracker_clicked()));
    this->setting_dialog->show();
};

void StartPanel::on_btn_start_eyetracker_clicked()
{
    if (!this->eyetracker_wrap->eyetracker)
    {
        global_config.load_eyetracker();
        this->ui->eyetracker_info->clear();
        this->ui->eyetracker_info->appendPlainText(
            "there is no eyetracker detected, please check your connection and"
            " settings, then click the button again!");
    }
    else
    {
        if (this->eyetracker_subscribed)
        {
            this->timer->stop();
            QMessageBox::information(this, "提示", "重新向眼动仪请求位置数据，请稍等1～2秒");
            this->eyetracker_wrap->unsubscribe_user_position(user_position_guide_callback);
            this->eyetracker_subscribed = false;
        }
        this->ui->eyetracker_info->clear();
        auto eyetracker_info = EyeTrackerWrapper::get_eyetracker_info(this->eyetracker_wrap->eyetracker);
        float frequency = this->eyetracker_wrap->get_current_frequency();
        this->ui->eyetracker_info->appendPlainText(
            "Address:" + eyetracker_info["address"].toString());
        this->ui->eyetracker_info->appendPlainText(
            "Model: " + eyetracker_info["model"].toString());
        this->ui->eyetracker_info->appendPlainText(
            "Name: " + eyetracker_info["device_name"].toString());
        this->ui->eyetracker_info->appendPlainText(
            "Serial number: " + eyetracker_info["serial_number"].toString());
        this->ui->eyetracker_info->appendPlainText(
            QString("Gaze output frequency: %1").arg(frequency));
        this->eyetracker_wrap->subscribe_user_position(user_position_guide_callback,global_user_position);
        this->eyetracker_subscribed = true;
        this->eye_show->IsPainter = true;

        this->timer->start();
        this->ui->btn_calibration->setEnabled(true);
    }
};

void StartPanel::on_btn_calibration_clicked()
{
    // query whether to enter calibration
    auto query_result = QMessageBox::question(this, "提示", "是否开始校准？",
                                              QMessageBox::Yes | QMessageBox::No,
                                              QMessageBox::Yes);
    if (query_result == QMessageBox::Yes)
    {
        this->timer->stop();
        this->calibration_widget = new CalibrationWidget();
        this->calibration_result = new CalibrationResultWidget();
        connect(this, SIGNAL(start_calibration()), this->calibration_widget, SLOT(start_calibration()));
        connect(this->calibration_widget, SIGNAL(calibration_finish(TobiiResearchCalibrationResult*)),
                this->calibration_result, SLOT(draw_calibration_samples(TobiiResearchCalibrationResult*)));
        connect(this->calibration_widget, SIGNAL(calibration_finish(TobiiResearchCalibrationResult*)),
                this, SLOT(solve_calibration_end()));
        emit start_calibration();
        if(this->is_debug){
            this->is_calibrated = true;
        }

    }
};

void StartPanel::on_btn_getdir_clicked()
{
    QString str_dir = QFileDialog::getExistingDirectory();
    if (str_dir.trimmed().size() <= 0)
        return;
    this->ui->lineEdit_imgdb_dir->setText(str_dir);
};

void StartPanel::on_btn_imgdb_apply_clicked()
{
    this->dir_imgdb = this->ui->lineEdit_imgdb_dir->text();
    QDir dir;
    bool is_exist = dir.exists(this->dir_imgdb);
    if (!is_exist)
    {
        QMessageBox::warning(this, "错误警告", "路径不存在！");
        return;
    }
    global_config.set_value("database/path", this->dir_imgdb);
    if(this->is_calibrated)
        this->ui->btn_start->setEnabled(true);
    else if(this->is_debug){
        QMessageBox::warning(this,"调试模式","眼动仪未矫正!");
        this->ui->btn_start->setEnabled(true);
    }
};

void StartPanel::on_btn_start_clicked()
{
    QDir dir(this->dir_imgdb);
    if (!dir.exists())
    {
        QString msg = QString("数据库地址：%1 无效,请检查是否已应用").arg(this->dir_imgdb);
        QMessageBox::warning(this, "警告", msg);
        return;
    }
    if (!this->eyetracker_wrap->eyetracker){
        if (this->is_debug)
            QMessageBox::warning(this, "调试模式", "未检测到眼动仪设备，下面将只显示页面，不记录信息");
        else
        {
            QMessageBox::warning(this, "错误", "未检测到眼动仪设备，请检查连接");
            return;
        }
    }
    if (!this->experiment_started)
    {
        this->experiment_started = true;
        this->timer->stop();
        this->image_show_widget = new ImageShowWidget();
        connect(this, SIGNAL(begin_test(QString)), this->image_show_widget, SLOT(begin_test(QString)));
        connect(this, SIGNAL(continue_test(QString)), this->image_show_widget, SLOT(continue_test(QString)));
        connect(this->image_show_widget, SIGNAL(eye_detection_error(QString)), this, SLOT(solve_eye_detection_error()));
        connect(this->image_show_widget, SIGNAL(experiment_pause(QString)), this, SLOT(image_show_pause()));
        connect(this->image_show_widget, SIGNAL(experiment_finished(QString)), this, SLOT(finish_experiment()));
        emit begin_test(this->participant_id);
    }
    else
    {
        this->timer->stop();
        emit continue_test(this->participant_id);
    }
};

void StartPanel::begin_setting(QString participant_id)
{
    this->participant_id = participant_id;
    this->show();
};

void StartPanel::do_timer_timeout()
{
    TobiiResearchUserPositionGuide &user_position = global_user_position;
    if (user_position.left_eye.validity || user_position.right_eye.validity)
    {
        MyFPoint3D left_data = {
            user_position.left_eye.user_position.x,
            user_position.left_eye.user_position.y,
            user_position.left_eye.user_position.z};
        MyFPoint3D right_data = {
            user_position.right_eye.user_position.x,
            user_position.right_eye.user_position.y,
            user_position.right_eye.user_position.z};

        this->eye_show->eye_pos_adcs[0] = left_data;
        this->eye_show->eye_pos_adcs[1] = right_data;
        this->eye_show->update();
        TobiiResearchTrackBox track_box = this->eyetracker_wrap->get_track_box();
        MyFPoint3D track_box_base = {
            track_box.front_upper_right.x,
            track_box.front_upper_right.y,
            track_box.front_upper_right.z,
        };
        MyFPoint3D track_box_size = {track_box.back_lower_left.x - track_box.front_upper_right.x,
                                     track_box.back_lower_left.y - track_box.front_upper_right.y,
                                     track_box.back_lower_left.z - track_box.front_upper_right.z};
        float left_z = 0, right_z = 0, left_d2c = 1, right_d2c = 1;
        if (user_position.left_eye.validity)
        {
            left_z = left_data[2] * track_box_size[2] + track_box_base[2];
            left_d2c = qSqrt(qPow((left_data[0] - 0.5), 2) +
                             qPow((left_data[1] - 0.5), 2) +
                             qPow((left_data[2] - 0.5), 2));
        }
        if (user_position.right_eye.validity)
        {
            right_z = right_data[2] * track_box_size[2] + track_box_base[2];
            right_d2c = qSqrt(qPow((right_data[0] - 0.5), 2) +
                              qPow((right_data[1] - 0.5), 2) +
                              qPow((right_data[2] - 0.5), 2));
        }
        int distance = 0.5 * (left_z + right_z) / 10;
        int d2c = 100 - int(0.5 * (left_d2c + right_d2c) * 100);
        this->ui->pgb_h->setValue(d2c);
        if (distance < 45)
        {
            this->ui->pgb_v->setValue(45);
            this->ui->distance->setText("45");
        }
        else if (distance > 75)
        {
            this->ui->pgb_v->setValue(75);
            this->ui->distance->setText("75");
        }
        else
        {
            this->ui->pgb_v->setValue(distance);
            this->ui->distance->setText(QString("%1").arg(distance));
        }
    }else{
        this->eye_show->eye_pos_adcs={};
        this->eye_show->update();
        this->ui->pgb_h->setValue(0);
    }
};

void StartPanel::solve_calibration_end()
{
    if (!this->is_calibrated)
        this->is_calibrated = true;
    QDir dir(this->dir_imgdb);
    if(dir.exists()){
        this->ui->btn_start->setEnabled(true);
    };
    this->timer->start();
};

void StartPanel::solve_eye_detection_error()
{
    this->ui->btn_start->setText("继续实验");
    this->timer->start();
};

void StartPanel::finish_experiment()
{
    this->eyetracker_wrap->unsubscribe_user_position(&user_position_guide_callback);
    QMessageBox::information(this,"实验结束","感谢您的参与!");
    this->image_show_widget->close();
    this->close();
};

void StartPanel::image_show_pause()
{
    this->timer->start();
    this->show();
};
