#ifndef EYETRACKERWRAPPER_H
#define EYETRACKERWRAPPER_H
#include "mytypedef.h"
#include "tobii_research.h"
#include "tobii_research_calibration.h"
#include "tobii_research_eyetracker.h"
#include "tobii_research_streams.h"
#include <QHash>
#include <QPair>
#include <QString>
#include <QVariant>
#include <QVector>
#include <QtDebug>

class EyeTrackerWrapper
{
public:
    // define some useful data type
    typedef QHash<QString, QVariant> EyeTrackerInfo;
    struct CalibrationResult
    {
        CalibrationResult() : mp_result(nullptr){};
        ~CalibrationResult()
        {
            if (mp_result)
                tobii_research_free_screen_based_calibration_result(mp_result);
        };
        TobiiResearchCalibrationResult *mp_result;
    };
    struct EyeTrackers
    {
        EyeTrackers() : mp_eyetrackers(nullptr){};
        ~EyeTrackers()
        {
            if (mp_eyetrackers)
                tobii_research_free_eyetrackers(mp_eyetrackers);
        }
        TobiiResearchEyeTrackers *mp_eyetrackers;
    };

public:
    EyeTrackerWrapper();
    EyeTrackerWrapper(const QString &address);
    ~EyeTrackerWrapper(){};

    void set_frequency(const float frequency);
    float get_current_frequency();
    QVector<float> get_frequency_options();
    // calibration
    void calibration_start();
    void calibration_collect(const MyFPoint2D &point, bool recollect = false);
    CalibrationResult calibration_apply();
    void calibration_end();
    // gaze_data
    void subscribe_gaze_data(tobii_research_gaze_data_callback, TobiiResearchGazeData &);
    void unsubscribe_gaze_data(tobii_research_gaze_data_callback);
    // user position guide
    void subscribe_user_position();
    void unsubscribe_user_position();
    TobiiResearchUserPositionGuide get_user_position();
    void user_position_guide_callback(TobiiResearchUserPositionGuide *user_pos, void *user_data);
    // other information
    TobiiResearchTrackBox get_track_box();
    EyeTrackerInfo get_info();

public:
    static EyeTrackers find_eyetrackers();
    static int64_t get_system_time_stamp();
    static EyeTrackerInfo get_eyetracker_info(TobiiResearchEyeTracker *eyetracker);

public:
    TobiiResearchEyeTracker *eyetracker;

private:
    QString address;
    QString model;
    QString device_name;
    QString serial_number;
    TobiiResearchUserPositionGuide user_position;
};

QVariantHash convert_to_QVariantHash(TobiiResearchCalibrationPoint);
QVariantHash convert_to_QVariantHash(TobiiResearchGazeOrigin);
QVariantHash convert_to_QVariantHash(TobiiResearchGazePoint);
QVariantHash convert_to_QVariantHash(TobiiResearchGazeData);

#endif // EYETRACKERWRAPPER_H
