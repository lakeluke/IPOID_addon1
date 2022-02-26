#ifndef CALIBRATIONWIDGET_H
#define CALIBRATIONWIDGET_H

#include "eyetrackerwrapper.h"
#include <QLayout>
#include <QTimer>
#include <QVector>
#include <QWidget>
#include <array>

typedef std::array<int, 2> MyRes;
typedef std::array<float, 2> MyFPoint2D;

class CalibrationWidget : public QWidget
{
    Q_OBJECT
private:
    class PointShow : public QWidget
    {
    public:
        explicit PointShow(QWidget *parent = nullptr);

    protected:
        virtual void paintEvent(QPaintEvent *) override;

    public:
        void draw_circle(QPainter &);
        float p_x;
        float p_y;
        int p_rad;
    };

signals:
    void calibration_finish();

public slots:
    void start_calibration();
    void do_timer_timeout();

public:
    explicit CalibrationWidget(QWidget *parent = nullptr);
    ~CalibrationWidget();

protected:
    virtual void keyReleaseEvent(QKeyEvent *) override;

private:
    void init_ui();
    void init_calibration_params();
    void init_timer();
    void process_calibration_result();

private:
    EyeTrackerWrapper *eyetracker_wrap;

    MyRes resolution;
    bool is_debug;
    // time interval settings
    uint refresh_interval_ms;
    uint point_show_time_ms;
    uint point_show_calibration_time_ms;
    uint point_show_interval_ms;
    uint refresh_num_each_point;
    uint refresh_num_each_calibration;
    // ui component
    QLayout *main_layout;
    PointShow *point_show;
    // calibration params
    uint calibration_point_number;
    QVector<MyFPoint2D> calibration_point_list;
    QHash<int, QVector<MyFPoint2D>> calibration_point_dict;
    // timer flags
    QTimer timer;
    uint current_point;
    uint current_refresh;

public:
    EyeTrackerWrapper::CalibrationResult calibration_result;
};

#endif // CALIBRATIONWIDGET_H
