#ifndef CALIBRATIONRESULTWIDGET_H
#define CALIBRATIONRESULTWIDGET_H

#include "mytypedef.h"
#include "tobii_research_calibration.h"
#include <QFrame>
#include <QLayout>
#include <QPainter>
#include <QVariantList>
#include <QVector>
#include <QWidget>

class CalibrationResultWidget : public QWidget
{
    Q_OBJECT
private:
    class EyeDataShow : public QFrame
    {
    public:
        explicit EyeDataShow(QWidget *parent = nullptr);
        void set_eye_data(QVector<MyFPoint2D>, QVector<QVariantList>);

    protected:
        virtual void paintEvent(QPaintEvent *) override;
        void draw_eye_data(QPainter &);

    private:
        int calibration_point_rad;
        QVector<MyFPoint2D> calibration_point_list;
        QVector<QVariantList> eye_data_list;
    };

public:
    explicit CalibrationResultWidget(QWidget *parent = nullptr);
    void init_ui();

public slots:
    void draw_calibration_samples(TobiiResearchCalibrationResult*);

private:
    TobiiResearchCalibrationResult *calibration_result_ptr;
    QLayout *main_layout;
    EyeDataShow *left_result;
    EyeDataShow *right_result;
};

#endif // CALIBRATIONRESULTWIDGET_H
