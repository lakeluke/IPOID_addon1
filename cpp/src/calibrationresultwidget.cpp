#include "calibrationresultwidget.h"

CalibrationResultWidget::EyeDataShow::EyeDataShow(QWidget *parent):QFrame(parent)
{
    this->setFrameShape(QFrame::Box);
    this->setFrameShadow(QFrame::Raised);
    this->setLineWidth(2);
    this->setStyleSheet("background-color:white");
    this->calibration_point_rad = 10;
    this->calibration_point_list = {{0.5, 0.5}, {0.1, 0.1}, {0.9, 0.1}, {0.9, 0.9}, {0.1, 0.9}};
};

void CalibrationResultWidget::EyeDataShow::set_eye_data(QVector<MyFPoint2D> calibration_point_list,
                                                        QVector<QVariantList> eye_data_list)
{
    this->calibration_point_list = calibration_point_list;
    this->eye_data_list = eye_data_list;
};

void CalibrationResultWidget::EyeDataShow::paintEvent(QPaintEvent *event)
{
    QFrame::paintEvent(event);
    QPainter painter;
    painter.begin(this);
    this->draw_eye_data(painter);
    painter.end();
};

void CalibrationResultWidget::EyeDataShow::draw_eye_data(QPainter &painter)
{
    QPen pen = QPen(Qt::black, 1, Qt::SolidLine);
    painter.setPen(pen);
    QBrush brush;
    brush.setColor(Qt::white);
    brush.setStyle(Qt::SolidPattern);
    painter.setBrush(brush);
    // draw calibration points
    for (MyFPoint2D point : this->calibration_point_list)
    {
        painter.drawEllipse(QPoint(point[0] * this->width(), point[1] * this->height()),
                            this->calibration_point_rad, this->calibration_point_rad);
    }

    pen = QPen(Qt::green, 3, Qt::SolidLine);
    painter.setPen(pen);
    for (QVariantList eye_pos : this->eye_data_list)
    {
        if (eye_pos[2].toString() == "validity_valid_and_used")
        {
            painter.drawPoint(QPoint(eye_pos[0].toInt() * this->width(), eye_pos[1].toInt() * this->height()));
        }
    }
};

CalibrationResultWidget::CalibrationResultWidget(QWidget *parent)
    : QWidget{parent}
{
    this->init_ui();
};

void CalibrationResultWidget::init_ui()
{
    this->setWindowTitle("眼动矫正结果");
    this->setObjectName("CalibrationResultWidget");
    this->resize(960, 480);
    this->setStyleSheet("background-color:0x161616");
    // this->setContentsMargins(6, 6, 6, 6);
    this->main_layout = new QHBoxLayout(this);
    this->main_layout->setObjectName("main_layout");
    this->left_result = new EyeDataShow(this);
    this->right_result = new EyeDataShow(this);
    this->main_layout->addWidget(this->left_result);
    this->main_layout->addWidget(this->right_result);
};

void CalibrationResultWidget::draw_calibration_samples(TobiiResearchCalibrationResult *result)
{
    QVector<MyFPoint2D> calibration_point_list;
    QVector<QVariantList> left_eye_data_list;
    QVector<QVariantList> right_eye_data_list;
    if (result)
    {
        for (size_t i = 0; i < result->calibration_point_count; ++i)
        {
            auto tr_cali_point = result->calibration_points[i];
            calibration_point_list.append({tr_cali_point.position_on_display_area.x,
                                           tr_cali_point.position_on_display_area.y});
            for (size_t j = 0; j < tr_cali_point.calibration_sample_count; ++j)
            {
                auto tr_cali_sample = tr_cali_point.calibration_samples[j];
                left_eye_data_list.append({tr_cali_sample.left_eye.position_on_display_area.x,
                                           tr_cali_sample.left_eye.position_on_display_area.y,
                                           tr_cali_sample.left_eye.validity});
                right_eye_data_list.append({tr_cali_sample.right_eye.position_on_display_area.x,
                                            tr_cali_sample.right_eye.position_on_display_area.y,
                                            tr_cali_sample.right_eye.validity});
            }
        }
    };
    this->left_result->set_eye_data(calibration_point_list, left_eye_data_list);
    this->right_result->set_eye_data(calibration_point_list, right_eye_data_list);
    this->left_result->update();
    this->right_result->update();
    this->show();
};
