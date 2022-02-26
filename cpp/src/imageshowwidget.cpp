#include "imageshowwidget.h"
#include <QDir>
#include <QJsonArray>
#include <QKeyEvent>
#include <QLayout>
#include <QMessageBox>
#include <QTime>
#include <algorithm>

static TobiiResearchGazeData global_gaze_data;
static QList<TobiiResearchGazeData> global_gaze_data_list;
void gaze_data_callback(TobiiResearchGazeData *tr_gaze_data, void *user_data)
{
    memcpy(user_data, tr_gaze_data, sizeof(*tr_gaze_data));
    if ((tr_gaze_data->left_eye.gaze_point.validity == TOBII_RESEARCH_VALIDITY_VALID) ||
        (tr_gaze_data->right_eye.gaze_point.validity == TOBII_RESEARCH_VALIDITY_VALID))
        global_gaze_data_list.append(*tr_gaze_data);
};

ImageShowWidget::ImageShowWidget(QWidget *parent)
    : QWidget{parent}
{
    this->image_layout = new QGridLayout(this);
    this->image_display = new QLabel(this);
    this->resolution = {1920, 1080};
    this->eyetracker_wrap = global_config.get_eyetracker_wrapper();
    this->load_config();
    this->init_ui();
    this->state = 1 << this->DisplayState::START;
    this->init_timer();
    this->init_connections();
    this->load_images();
    this->countdown = 0;
};
void ImageShowWidget::init_ui()
{
    this->setObjectName("image_show_widget");
    this->resize(this->resolution[0], this->resolution[1]);
    this->move(0, 0);
    this->image_layout->setObjectName("image_layout");
    this->image_layout->setContentsMargins(0, 0, 0, 0);
    this->image_layout->setSpacing(5);
    this->image_display->setLineWidth(0);
    this->image_display->setAlignment(Qt::AlignCenter);
    this->image_display->setObjectName("image_display");
    this->image_display->setStyleSheet("background-color:#808080");
    this->image_layout->addWidget(this->image_display);
};
void ImageShowWidget::load_config()
{
    this->eyetracker_frequency = global_config.get_value("eyetracker/frequency", 60).toInt();
    this->image_show_time = (global_config.get_value("image_show/last_time", 10).toInt() * 1000);
    this->image_show_interval = (global_config.get_value("image_show/time_interval", 3).toInt() * 1000);
    this->dir_imgdb = global_config.get_value("database", "path").toString();
    this->dir_out_data = global_config.get_value("data", "path").toString();
    this->is_debug = global_config.get_value("mode", "debug").toBool();
    this->detect_error_interval_ms = 20;
    this->imgshow_timer_interval_ms = 100;
    this->image_suffix = {".bmp", ".png", ".jpg", ".jpeg"};
    this->eye_detect_error_count = 0;
};
void ImageShowWidget::init_timer()
{
    this->imgshow_timer = new QTimer(this);
    this->imgshow_timer->stop();
    this->imgshow_timer->setInterval(this->imgshow_timer_interval_ms);
    this->detect_error_timer = new QTimer(this);
    this->detect_error_timer->stop();
    this->detect_error_timer->setInterval(this->detect_error_interval_ms);
};
void ImageShowWidget::init_connections()
{
    connect(this->imgshow_timer, SIGNAL(timeout()), this, SLOT(do_timer_timeout()));
    if (this->eyetracker_wrap->eyetracker)
        connect(this->detect_error_timer, SIGNAL(timeout()), this, SLOT(do_error_detection()));
    connect(this, SIGNAL(eye_detection_error(QString)), this, SLOT(pause(QString)));
    connect(this, SIGNAL(experiment_error(QString)), this, SLOT(pause(QString)));
    connect(this, SIGNAL(experiment_pause(QString)), this, SLOT(pause(QString)));
    connect(this, SIGNAL(experiment_finished(QString)), this, SLOT(pause(QString)));
};

void ImageShowWidget::load_images()
{
    this->image_num = 0;
    this->image_list.clear();
    this->cur_image_index = 0;
    QDir dir = QDir(this->dir_imgdb);
    bool imgdb_exist = dir.exists();
    if (!imgdb_exist)
    {
        emit experiment_error("imgdb directory not exist");
        return;
    }
    QStringList ls_imgdb = dir.entryList();
    for (QString img_file : ls_imgdb)
    {
        QFileInfo fileinfo = QFileInfo(img_file);
        QString suffix = fileinfo.suffix();
        if (this->image_suffix.contains(suffix))
            this->image_list.append(img_file);
    }
    this->image_num = this->image_list.size();
    std::random_shuffle(this->image_list.begin(), this->image_list.end());
    this->state = this->state | (1 << this->DisplayState::READY);
};

void ImageShowWidget::subscribe_eye_data()
{
    this->eye_detect_error_count = 0;
    if (this->eyetracker_wrap->eyetracker)
    {
        if (this->is_subscribed)
            global_gaze_data_list.clear();
        else
            this->eyetracker_wrap->subscribe_gaze_data(gaze_data_callback, global_gaze_data);
        this->is_subscribed = true;
    }
    else
    {
        if (this->is_debug)
        {
            if (this->cur_image_index <= 0)
                QMessageBox::information(this, "调试模式!", "未发现眼动仪,仅演示效果!");
        }
        else
            QMessageBox::warning(this, "警告", "未发现眼动仪");
    }
};

void ImageShowWidget::save_eye_data(const QString &filetype)
{
    auto gaze_data = global_gaze_data_list;
    if (filetype.contains("txt"))
    {
        QFile file(this->current_eye_data_file_name + ".txt");
        file.open(QIODevice::Append);
        for (TobiiResearchGazeData gaze_data_sample : gaze_data)
        {
            QString time_stamp_str = QString("%ld\t%ld\t")
                                         .arg(gaze_data_sample.device_time_stamp)
                                         .arg(gaze_data_sample.system_time_stamp);
            QString left_eye_data_str = QString("(%f,%f)\t(%f,%f,%f)\t%d\t"
                                                "%f\t%d\t"
                                                "(%f\t%f\t%f)\t(%f\t%f\t%f)\t%d\t")
                                            .arg(gaze_data_sample.left_eye.gaze_point.position_on_display_area.x)
                                            .arg(gaze_data_sample.left_eye.gaze_point.position_on_display_area.y)
                                            .arg(gaze_data_sample.left_eye.gaze_point.position_in_user_coordinates.x)
                                            .arg(gaze_data_sample.left_eye.gaze_point.position_in_user_coordinates.y)
                                            .arg(gaze_data_sample.left_eye.gaze_point.position_in_user_coordinates.z)
                                            .arg(gaze_data_sample.left_eye.gaze_point.validity)
                                            .arg(gaze_data_sample.left_eye.pupil_data.diameter)
                                            .arg(gaze_data_sample.left_eye.pupil_data.validity)
                                            .arg(gaze_data_sample.left_eye.gaze_origin.position_in_user_coordinates.x)
                                            .arg(gaze_data_sample.left_eye.gaze_origin.position_in_user_coordinates.y)
                                            .arg(gaze_data_sample.left_eye.gaze_origin.position_in_user_coordinates.z)
                                            .arg(gaze_data_sample.left_eye.gaze_origin.position_in_track_box_coordinates.x)
                                            .arg(gaze_data_sample.left_eye.gaze_origin.position_in_track_box_coordinates.y)
                                            .arg(gaze_data_sample.left_eye.gaze_origin.position_in_track_box_coordinates.z)
                                            .arg(gaze_data_sample.left_eye.gaze_origin.validity);
            QString right_eye_data_str = QString("(%f,%f)\t(%f,%f,%f)\t%d\t"
                                                 "%f\t%d\t"
                                                 "(%f\t%f\t%f)\t(%f\t%f\t%f)\t%d\t")
                                             .arg(gaze_data_sample.right_eye.gaze_point.position_on_display_area.x)
                                             .arg(gaze_data_sample.right_eye.gaze_point.position_on_display_area.y)
                                             .arg(gaze_data_sample.right_eye.gaze_point.position_in_user_coordinates.x)
                                             .arg(gaze_data_sample.right_eye.gaze_point.position_in_user_coordinates.y)
                                             .arg(gaze_data_sample.right_eye.gaze_point.position_in_user_coordinates.z)
                                             .arg(gaze_data_sample.right_eye.gaze_point.validity)
                                             .arg(gaze_data_sample.right_eye.pupil_data.diameter)
                                             .arg(gaze_data_sample.right_eye.pupil_data.validity)
                                             .arg(gaze_data_sample.right_eye.gaze_origin.position_in_user_coordinates.x)
                                             .arg(gaze_data_sample.right_eye.gaze_origin.position_in_user_coordinates.y)
                                             .arg(gaze_data_sample.right_eye.gaze_origin.position_in_user_coordinates.z)
                                             .arg(gaze_data_sample.right_eye.gaze_origin.position_in_track_box_coordinates.x)
                                             .arg(gaze_data_sample.right_eye.gaze_origin.position_in_track_box_coordinates.y)
                                             .arg(gaze_data_sample.right_eye.gaze_origin.position_in_track_box_coordinates.z)
                                             .arg(gaze_data_sample.right_eye.gaze_origin.validity);
            QString gaze_data_str = time_stamp_str + left_eye_data_str + right_eye_data_str;
            file.write(gaze_data_str.toUtf8());
            file.write("\n");
        }
        file.close();
    }
    if (filetype.contains("json"))
    {
        QFile file(this->current_eye_data_file_name + ".json");
        file.open(QIODevice::Append);
        QJsonArray gaze_data_json = QJsonArray();
        for (TobiiResearchGazeData gaze_data_sample : gaze_data)
        {
            QJsonObject gaze_sample_object = QJsonObject::fromVariantHash(convert_to_QVariantHash(gaze_data_sample));
            gaze_data_json.append(gaze_sample_object);
        }

        file.close();
    };
}
void ImageShowWidget::begin_test(QString participant_id)
{
    this->setWindowState(Qt::WindowMaximized);
    this->setWindowFlag(Qt::FramelessWindowHint);
    this->participant_id = participant_id;
    this->eyetracker_wrap = global_config.get_eyetracker_wrapper();
    this->cur_image_index = -1;
    this->state = this->state | (1 << this->DisplayState::IMAGE);
    this->countdown = 0;
    this->eye_detect_error_count = 0;
    this->is_subscribed = false;
    this->do_timer_timeout();
    this->showFullScreen();
};
void ImageShowWidget::continue_test(QString participant_id)
{
    // this->setWindowState(Qt::WindowMaximized);
    // this->setWindowFlag(Qt::FramelessWindowHint);
    this->participant_id = participant_id;
    this->state = this->state | (1 << this->DisplayState::READY); // Ready bit set to 1
    this->countdown = 0;
    if (this->state | (1 << this->DisplayState::IMAGE))
    {
        this->cur_image_index = this->cur_image_index - 1;
        this->state = this->state & (~(1 << this->DisplayState::IMAGE));
    }
    else
    {
        this->state = this->state | (1 << this->DisplayState::IMAGE);
    }
    this->is_subscribed = false;
    this->do_timer_timeout();
    this->eye_detect_error_count = 0;
    this->showFullScreen();
};
void ImageShowWidget::pause(QString str)
{
    this->imgshow_timer->stop();
    this->detect_error_timer->stop();
    if (this->eyetracker_wrap->eyetracker)
    {
        this->eyetracker_wrap->unsubscribe_gaze_data(gaze_data_callback);
    }
    this->state = this->state & (~(1 << this->DisplayState::READY));
    this->close();
    QString pause_msg = "程序暂停：" + str;
    QMessageBox::warning(this, "pause", pause_msg);
};

void ImageShowWidget::do_timer_timeout()
{
    this->countdown = this->countdown - this->imgshow_timer_interval_ms;
    if (this->countdown < this->imgshow_timer_interval_ms)
    {
        this->countdown = 0;
        this->imgshow_timer->stop();
        if (this->state & (1 << this->DisplayState::READY))
        {
            if (this->state & (1 << this->DisplayState::IMAGE))
            {
                if (this->state | (1 << this->DisplayState::START))
                    this->state = this->state & (~(1 << this->DisplayState::START));
                else
                    this->save_eye_data("txt,json");
                this->detect_error_timer->stop();
                this->state = this->state & (~(1 << this->DisplayState::IMAGE));
                this->countdown = this->image_show_interval;
                this->cur_pixmap = QPixmap();
                this->image_display->setPixmap(this->cur_pixmap);
                this->imgshow_timer->start();
            }
            else
            {
                if (this->cur_image_index < this->image_num - 1)
                {
                    this->cur_image_index = this->cur_image_index + 1;
                    this->cur_image_name = this->image_list[this->cur_image_index].split(".")[0];
                    QDir qdir_imgdb = QDir(this->dir_imgdb);
                    this->cur_image_file = qdir_imgdb.absoluteFilePath(this->image_list[this->cur_image_index]);
                    this->cur_image.load(this->cur_image_file);
                    this->cur_pixmap = QPixmap::fromImage(this->cur_image);
                    this->image_display->setPixmap(this->cur_pixmap);
                    QChar sep = QDir::separator();
                    this->current_eye_data_file_name = QDir(this->dir_out_data).absolutePath() +
                                                       sep + this->participant_id +
                                                       sep + this->cur_image_name;
                    QString time_str = QTime::currentTime().toString("HH:mm:ss.zzz");
                    this->state = this->state | (1 << this->DisplayState::IMAGE);
                    this->countdown = this->image_show_time;
                    this->subscribe_eye_data();
                    this->imgshow_timer->start();
                    if (this->eyetracker_wrap->eyetracker)
                        this->detect_error_timer->start();
                }
                else
                {
                    this->experiment_finished("finish");
                    return;
                }
            }
        }
        else
            qWarning("enter imgshow timeout solver error");
    }
};
void ImageShowWidget::do_error_detection()
{
    TobiiResearchGazeData current_gaze_data = global_gaze_data;
    if (current_gaze_data.left_eye.gaze_point.validity == 0 &&
        current_gaze_data.right_eye.gaze_point.validity == 0)
        this->eye_detect_error_count = this->eye_detect_error_count + 1;
    else
        this->eye_detect_error_count = 0;
    if (this->eye_detect_error_count >= int(
                                            (this->image_show_time / this->detect_error_interval_ms) * 0.75))
        this->detect_error_timer->stop();
    this->imgshow_timer->stop();
    if (this->eyetracker_wrap->eyetracker)
        this->eyetracker_wrap->unsubscribe_gaze_data(gaze_data_callback);
    global_gaze_data_list.clear();
    this->eye_detect_error_count = 0;
    QString dlgTitle = "信息框";
    QString strInfo = "眼动仪捕捉眼动信息失败，请调整坐姿!";
    QMessageBox::information(this, dlgTitle, strInfo);
    emit eye_detection_error("捕捉眼睛失败");
};

void ImageShowWidget::keyReleaseEvent(QKeyEvent *event)
{
    if (event->key() == Qt::Key_P)
        emit experiment_pause("key pause");

    if (event->key() == Qt::Key_Q)
        emit experiment_pause("key quit");
};
