#ifndef STARTPANEL_H
#define STARTPANEL_H

#include "eyetrackerwrapper.h"
#include "calibrationwidget.h"
#include "calibrationresultwidget.h"
#include "imageshowwidget.h"

#include <QMainWindow>
#include <QTimer>
#include <QPainter>
#include <QDir>

namespace Ui {
class StartPanel;
}

class StartPanel : public QMainWindow
{
    Q_OBJECT

signals:
    void start_calibration();
    void begin_test(const QString&);
    void continue_test(const QString&);

public slots:
    void on_action_setting_triggered();
    void on_btn_start_eyetracker_clicked();
    void on_btn_calibration_clicked();
    void on_btn_getdir_clicked();
    void on_btn_imgdb_apply_clicked();
    void on_btn_start_clicked();
    void begin_setting(const QString& participant_id);
    void do_timer_timeout();
    void solve_calibration_end();
    void solve_eye_detection_error();
    void finish_experiment();
    void image_show_pause();

private:
    class EyePosShow:public QWidget{
      public:
        explicit EyePosShow(QWidget *parent=nullptr);
        virtual void paintEvent(QPaintEvent*) override;

    };

public:
    explicit StartPanel(QWidget *parent = nullptr);
    ~StartPanel();

private:
    Ui::StartPanel *ui;
    StartPanel::EyePosShow *eye_show;
    QTimer *timer;

    bool is_calibrated;
    bool is_debug;
    int eyetracker_frequency;
    QDir dir_imgdb;
    QString participant_id;









};

#endif // STARTPANEL_H
