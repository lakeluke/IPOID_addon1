#include "calibrationwidget.h"
#include "myconfig.h"
#include <QKeyEvent>
#include <QMessageBox>
#include <chrono>
#include <thread>

extern MyConfig global_config;

CalibrationWidget::CalibrationWidget(QWidget *parent)
    : QWidget{parent}
{
    this->resolution = {1920, 1080};
    this->refresh_interval_ms = 40;
    this->point_show_time_ms = 1000;
    this->point_show_calibration_time_ms = 500;
    this->point_show_interval_ms = 200;
    this->refresh_num_each_point = this->point_show_time_ms / this->refresh_interval_ms;
    this->refresh_num_each_calibration = this->point_show_calibration_time_ms / this->refresh_interval_ms;

    this->init_ui();
    this->init_calibration_params();
    this->init_timer();
}

CalibrationWidget::~CalibrationWidget()
{
    delete point_show;
    delete main_layout;
}

void CalibrationWidget::init_ui()
{
    this->setObjectName("calibration_widget");
    this->resize(this->resolution[0], this->resolution[1]);
    this->move(0, 0);
    this->main_layout = new QGridLayout(this);
    this->main_layout->setContentsMargins(0, 0, 0, 0);
    this->main_layout->setSpacing(0);
    this->main_layout->setObjectName("main_layout");
    this->point_show = new PointShow(this);
    this->setContentsMargins(0, 0, 0, 0);
    this->point_show->setObjectName("point_show");
    this->point_show->setStyleSheet("background-color:#808080");
    this->main_layout->addWidget(this->point_show);
}

void CalibrationWidget::init_calibration_params()
{
    this->calibration_point_number = global_config.get_value(
                                                      "eyetracker/calibration_point_number", 9)
                                         .toUInt();
    this->calibration_point_dict = {
        {5, {{0.1, 0.1}, {0.9, 0.1}, {0.5, 0.5}, {0.1, 0.9}, {0.9, 0.9}}},
        {9, {{0.1, 0.1}, {0.5, 0.1}, {0.9, 0.1}, {0.1, 0.5}, {0.5, 0.5}, {0.9, 0.5}, {0.1, 0.9}, {0.5, 0.9}, {0.9, 0.9}}},
        {13, {{0.1, 0.1}, {0.5, 0.1}, {0.9, 0.1}, {0.3, 0.3}, {0.7, 0.3}, {0.1, 0.5}, {0.5, 0.5}, {0.9, 0.5}, {0.3, 0.7}, {0.7, 0.7}, {0.1, 0.9}, {0.5, 0.9}, {0.9, 0.9}}}};
    if (this->calibration_point_dict.contains(this->calibration_point_number))
        this->calibration_point_list = this->calibration_point_dict[this->calibration_point_number];
    else
    {
        qDebug() << QString("配置参数calibration_point_number错误！\n "
                            "必须为5, 9, 13三个值之一\n"
                            "此参数将被设置为默认值5");
        this->calibration_point_list = this->calibration_point_dict[5];
    }
};

void CalibrationWidget::init_timer()
{
    this->timer.stop();
    this->timer.setInterval(this->refresh_interval_ms);
    connect(&this->timer, SIGNAL(timeout()), this, SLOT(do_timer_timeout()));
};

void CalibrationWidget::process_calibration_result()
{
    QVariantList calibration_sample_list;
    if (this->calibration_result.mp_result)
    {
        TobiiResearchCalibrationStatus calibration_status = this->calibration_result.mp_result->status;
        if (calibration_status != TOBII_RESEARCH_CALIBRATION_SUCCESS)
        {
            QMessageBox::StandardButton qresult;
            qresult = QMessageBox::question(this, "矫正失败",
                                            tr("矫正状态：%s \n 是否重新矫正？").arg(calibration_status),
                                            QMessageBox::Yes | QMessageBox::No);
            if (qresult == QMessageBox::Yes)
            {
                this->start_calibration();
                return;
            }
        }
        QVector<TobiiResearchCalibrationEyeData> left_samples;
        /*
        right_samples = [];
        for (calibration_point : this->calibration_result.mp_result->calibration_points)
        {
            for (calibration_sample : calibration_point.calibration_samples)
            {
                left_sample = (calibration_sample.left_eye.position_on_display_area +
                               (calibration_sample.left_eye.validity, ));
                right_sample = (calibration_sample.right_eye.position_on_display_area +
                                (calibration_sample.right_eye.validity, ));
                left_samples.append(left_sample);
                right_samples.append(right_sample);
            }
        }
        calibration_sample_list = [ left_samples, right_samples ];
        */
    }
    this->calibration_finish.emit(this->calibration_point_list, calibration_sample_list);
};

void CalibrationWidget::start_calibration()
{
    this->eyetracker_wrap = global_config.get_eyetracker_wrapper();
    this->is_debug = global_config.get_value("mode/debug", false).toBool();
    this->current_point = 0;
    this->current_refresh = 0;
    if (this->eyetracker_wrap->eyetracker)
    {
        if (this->is_debug)
            QMessageBox::information(this, "调试模式", "未发现眼动仪，仅演示显示效果！");
        else
            QMessageBox::information(this, "矫正开启错误", "未发现眼动仪，请检查连接");
    }
    else
        this->eyetracker_wrap->calibration_start();
    this->showFullScreen();
    this->timer.start();
};

void CalibrationWidget::do_timer_timeout()
{
    if (this->current_point < this->calibration_point_number)
    {
        this->point_show->p_x = this->calibration_point_list[this->current_point][0];
        this->point_show->p_y = this->calibration_point_list[this->current_point][1];
        this->point_show->p_rad = 40.0 * (1 - this->current_refresh / this->refresh_num_each_point);
        this->point_show->update();
        if (this->current_refresh == this->refresh_num_each_point - this->refresh_num_each_calibration)
        {
            std::this_thread::sleep_for(std::chrono::milliseconds(500));
            if (this->eyetracker_wrap->eyetracker)
                this->eyetracker_wrap->calibration_collect(QPair<float, float>(this->point_show->p_x, this->point_show->p_y));
        }
        this->current_refresh = this->current_refresh + 1;
        if (this->current_refresh >= this->refresh_num_each_point)
        {
            this->current_point = this->current_point + 1;
            this->current_refresh = 0;
        }
    }
    else
    {
        this->timer.stop();
        if (this->eyetracker_wrap->eyetracker)
        {
            this->calibration_result = this->eyetracker_wrap->calibration_apply();
            this->eyetracker_wrap->calibration_end();
        }
        this->close();
        this->process_calibration_result();
    }
};

void CalibrationWidget::keyReleaseEvent(QKeyEvent *key_event)
{
    if (key_event->key() == Qt::Key_Q)
    {
        this->timer.stop();
        this->close();
        this->eyetracker_wrap->calibration_end();
        // this->calibration_finish->emit(this->calibration_point_list,[[],[],"calibration_key_Q exit"]);
    }
};
