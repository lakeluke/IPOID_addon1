#ifndef STARTPANEL_H
#define STARTPANEL_H

#include "calibrationresultwidget.h"
#include "calibrationwidget.h"
#include "eyetrackerwrapper.h"
#include "imageshowwidget.h"
#include "myconfig.h"
#include "settingdialog.h"
#include <QMainWindow>
#include <QPainter>
#include <QTimer>
#include <array>
namespace Ui
{
    class StartPanel;
}

extern MyConfig global_config;
typedef std::array<float, 3> MyFPoint3D;

class StartPanel : public QMainWindow
{
    Q_OBJECT
private:
    class EyePosShow : public QWidget
    {
    public:
        explicit EyePosShow(QWidget *parent = nullptr);
        virtual void paintEvent(QPaintEvent *) override;

    public:
        std::array<MyFPoint3D, 2> eye_pos_adcs;
        int current_rad;
        bool IsPainter;
        int W, H;
    };

signals:
    void start_calibration();
    void begin_test(const QString &);
    void continue_test(const QString &);

public slots:
    void on_action_setting_triggered();
    void on_btn_start_eyetracker_clicked();
    void on_btn_calibration_clicked();
    void on_btn_getdir_clicked();
    void on_btn_imgdb_apply_clicked();
    void on_btn_start_clicked();
    void begin_setting(const QString &participant_id);
    void do_timer_timeout();
    void solve_calibration_end();
    void solve_eye_detection_error();
    void finish_experiment();
    void image_show_pause();

public:
    explicit StartPanel(QWidget *parent = nullptr);
    ~StartPanel();

private:
    void init_connections();

private:
    Ui::StartPanel *ui;
    QTimer *timer;
    StartPanel::EyePosShow *eye_show;
    CalibrationWidget *calibration_widget;
    CalibrationResultWidget *calibration_result;
    ImageShowWidget *image_show_widget;
    SettingDialog *setting_dialog;

    bool is_debug;
    bool is_calibrated;
    bool experiment_started;
    bool eyetracker_subscribed;
    float eyetracker_frequency;
    QString dir_imgdb;
    QString participant_id;
    EyeTrackerWrapper *eyetracker_wrap;
};

#endif // STARTPANEL_H
