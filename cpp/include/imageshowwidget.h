#ifndef IMAGESHOWWIDGET_H
#define IMAGESHOWWIDGET_H
#include "myconfig.h"
#include <QWidget>
#include <QLabel>

typedef struct{
    int x;
    int y;
} MyPoint2D;

class ImageShowWidget : public QWidget
{
    Q_OBJECT
public:
    explicit ImageShowWidget(QWidget *parent = nullptr);
    void init_ui();
    void init_timer();
    void init_connections();
    void load_config();
    void load_images();
    void subscribe_eye_data();
    void save_eye_data();

signals:
    void eye_detection_error(QString);
    void experiment_error(QString);
    void experiment_pause(QString);
    void experiment_finished();

public slots:
    void begin_test(const QString& participant_id);
    void continue_test(const QString& participant_id);
    void pause(const QString& str);

private slots:
    void do_timer_timeout();
    void do_error_detection();

private:
    virtual void keyReleaseEvent(QKeyEvent*)override;
    enum DisplayState{START=0,READY=1,IMAGE=2,ERROR=3,FINISH=4};
    DisplayState state;
    int countdown;
    MyPoint2D resolution;
    QLayout* image_layout;
    QLabel* image_display;
    QTimer* imgshow_timer;
    QTimer* detect_error_timer;

};

#endif // IMAGESHOWWIDGET_H
