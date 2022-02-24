#ifndef EYETRACKERWRAPPER_H
#define EYETRACKERWRAPPER_H
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
    QVector<float> get_frequency_options();
    // calibration
    void calibration_start();
    void calibration_collect(const QPair<float, float> point, bool recollect = false);
    CalibrationResult calibration_apply();
    void calibration_end();
    // gaze_data
    void clear_gaze_data();
    void subscribe_gaze_data();
    void unsubscribe_gaze_data();
    // user position guide
    void subscribe_user_position();
    void unsubscribe_user_position();
    // other information
    TobiiResearchTrackBox get_track_box();

public:
    static EyeTrackers find_eyetrackers();
    static int64_t get_system_time_stamp();
    static EyeTrackerInfo get_eyetracker_info(TobiiResearchEyeTracker *eyetracker);
    static QVector<TobiiResearchGazeData> get_gaze_data();
    static TobiiResearchGazeData get_current_gaze_data();
    static TobiiResearchUserPositionGuide get_user_position();
    static void gaze_data_callback(TobiiResearchGazeData *gaze_data, void *user_data);
    static void user_position_guide_callback(TobiiResearchUserPositionGuide *user_pos, void *user_data);

public:
    TobiiResearchEyeTracker *eyetracker;

private:
    QString address;
    QString model;
    QString device_name;
    QString serial_number;
    static QVector<TobiiResearchGazeData> gaze_data;
    static TobiiResearchGazeData current_gaze_data;
    static TobiiResearchUserPositionGuide user_position;
};

QVariantHash convert_to_QVariantHash(TobiiResearchCalibrationPoint);
QVariantHash convert_to_QVariantHash(TobiiResearchGazeData);

#endif // EYETRACKERWRAPPER_H
