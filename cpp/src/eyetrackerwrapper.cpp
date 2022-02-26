#include "eyetrackerwrapper.h"
#include <QRegularExpression>

EyeTrackerWrapper::EyeTrackerWrapper()
{
    TobiiResearchEyeTrackers *eyetrackers = nullptr;
    TobiiResearchStatus result;
    result = tobii_research_find_all_eyetrackers(&eyetrackers);
    if (result != TOBII_RESEARCH_STATUS_OK)
    {
        qDebug() << QString("Finding trackers failed. Error: %d\n").arg(result);
        goto CLEAR_EYETRACKER;
    }
    else if (eyetrackers->count > 0)
    {
        qDebug() << QString("Find %d eyetrackers").arg(eyetrackers->count);
        eyetracker = eyetrackers->eyetrackers[0];
        EyeTrackerInfo info = this->get_eyetracker_info(eyetracker);
        this->address = info["address"].toString();
        this->serial_number = info["serial_number"].toString();
        this->device_name = info["device_name"].toString();
        this->model = info["model"].toString();
        tobii_research_get_eyetracker(this->address.toLatin1().data(), &this->eyetracker);
        tobii_research_free_eyetrackers(eyetrackers);
        this->clear_gaze_data();
        return;
    }
CLEAR_EYETRACKER:
{
    this->eyetracker = nullptr;
    this->address.clear();
    this->serial_number.clear();
    this->device_name.clear();
    this->model.clear();
}
};

EyeTrackerWrapper::EyeTrackerWrapper(const QString &address)
{
    QString address_pattern = "tet-tcp://((([0-9]{1,3})\\.){3}([0-9]{1,3}))";
    QRegularExpression regexp(address_pattern);
    QRegularExpressionMatch match;
    match = regexp.match(address);
    if (match.hasMatch())
    {
        TobiiResearchStatus status;
        status = tobii_research_get_eyetracker(address.toLatin1().data(), &this->eyetracker);
        if (status != TOBII_RESEARCH_STATUS_OK)
        {
            qDebug() << QString("Finding tracker of address: %s failed. Error: %d\n").arg(address).arg(status)
                     << QString("Use Default Constructor\n");
            new (this) EyeTrackerWrapper();
        }
        else
        {
            EyeTrackerInfo info = this->get_eyetracker_info(this->eyetracker);
            this->address = info["address"].toString();
            this->serial_number = info["serial_number"].toString();
            this->device_name = info["device_name"].toString();
            this->model = info["model"].toString();
            this->clear_gaze_data();
        };
    }
    else
    {
        qDebug() << QString("Given address: %s format invalid\n").arg(address)
                 << QString("Use Default Constructor\n");
        new (this) EyeTrackerWrapper();
    };
};

void EyeTrackerWrapper::set_frequency(const float frequency)
{
    if (this->eyetracker)
    {
        tobii_research_set_gaze_output_frequency(this->eyetracker, frequency);
    }
};
float EyeTrackerWrapper::get_current_frequency()
{
    float current_frequency;
    if (this->eyetracker)
    {
        TobiiResearchStatus status = tobii_research_get_gaze_output_frequency(this->eyetracker, &current_frequency);
        return current_frequency;
    }
    return -1;
}
QVector<float> EyeTrackerWrapper::get_frequency_options()
{
    QVector<float> freq;
    TobiiResearchGazeOutputFrequencies *frequencies = nullptr;
    if (this->eyetracker)
    {
        tobii_research_get_all_gaze_output_frequencies(this->eyetracker, &frequencies);
        for (size_t i = 0; i < frequencies->frequency_count; i++)
        {
            freq.append(frequencies->frequencies[i]);
        }
    }
    return freq;
};

// calibration
void EyeTrackerWrapper::calibration_start()
{
    if (this->eyetracker)
    {
        tobii_research_screen_based_calibration_enter_calibration_mode(this->eyetracker);
    }
};

void EyeTrackerWrapper::calibration_collect(const QPair<float, float> cpoint, bool recollect)
{
    if (eyetracker)
    {
        TobiiResearchNormalizedPoint2D point = {cpoint.first, cpoint.second};
        if (recollect)
        {
            tobii_research_screen_based_calibration_discard_data(eyetracker, point.x, point.y);
        }
        TobiiResearchStatus status;
        status = tobii_research_screen_based_calibration_collect_data(eyetracker, point.x, point.y);
        if (status != TOBII_RESEARCH_STATUS_OK)
        {
            tobii_research_screen_based_calibration_collect_data(eyetracker, point.x, point.y);
        }
    }
};

EyeTrackerWrapper::CalibrationResult EyeTrackerWrapper::calibration_apply()
{
    CalibrationResult calibration_result;
    TobiiResearchCalibrationResult *presult = calibration_result.mp_result;
    if (eyetracker)
    {
        TobiiResearchStatus status;
        status = tobii_research_screen_based_calibration_compute_and_apply(eyetracker, &presult);
        if (status == TOBII_RESEARCH_STATUS_OK && presult->status == TOBII_RESEARCH_CALIBRATION_SUCCESS)
        {
            qDebug() << QString("Compute and apply returned %i and collected at %zu points.\n").arg(status).arg(presult->calibration_point_count);
        }
        else
        {
            qDebug() << QString("Calibration failed!\n");
        }
    }
    return calibration_result;
};

void EyeTrackerWrapper::calibration_end()
{
    if (eyetracker)
    {
        tobii_research_screen_based_calibration_leave_calibration_mode(eyetracker);
    }
};

/*  TobiiResearchCalibrationData* EyeTrackerWrapper::get_calibration_data(){};
    void EyeTrackerWrapper::apply_calibration_data(TobiiResearchCalibrationData* calibration_data){}; */

// gaze_data

void EyeTrackerWrapper::subscribe_gaze_data()
{
    this->clear_gaze_data();
    if (eyetracker)
    {
        TobiiResearchStatus status = tobii_research_subscribe_to_gaze_data(eyetracker,
                                                                           &EyeTrackerWrapper::gaze_data_callback,
                                                                           &EyeTrackerWrapper::current_gaze_data);
        if (status != TOBII_RESEARCH_STATUS_OK)
        {
            tobii_research_unsubscribe_from_gaze_data(eyetracker, &EyeTrackerWrapper::gaze_data_callback);
            tobii_research_subscribe_to_gaze_data(eyetracker,
                                                  &EyeTrackerWrapper::gaze_data_callback,
                                                  &EyeTrackerWrapper::current_gaze_data);
        }
    }
};

void EyeTrackerWrapper::unsubscribe_gaze_data()
{
    if (this->eyetracker)
    {
        tobii_research_unsubscribe_from_gaze_data(this->eyetracker, &EyeTrackerWrapper::gaze_data_callback);
    }
};

// user position guide

void EyeTrackerWrapper::subscribe_user_position()
{
    if (this->eyetracker)
    {
        TobiiResearchStatus status;
        status = tobii_research_subscribe_to_user_position_guide(this->eyetracker,
                                                                 &EyeTrackerWrapper::user_position_guide_callback,
                                                                 &EyeTrackerWrapper::user_position);
        if (status != TOBII_RESEARCH_STATUS_OK)
        {
            tobii_research_unsubscribe_from_user_position_guide(eyetracker, &EyeTrackerWrapper::user_position_guide_callback);
            tobii_research_subscribe_to_user_position_guide(eyetracker,
                                                            &EyeTrackerWrapper::user_position_guide_callback,
                                                            &EyeTrackerWrapper::user_position);
        }
    }
};
void EyeTrackerWrapper::unsubscribe_user_position()
{
    if (this->eyetracker)
    {
        tobii_research_unsubscribe_from_user_position_guide(eyetracker, &EyeTrackerWrapper::user_position_guide_callback);
    }
};

// static methods
void EyeTrackerWrapper::clear_gaze_data()
{
    EyeTrackerWrapper::gaze_data.clear();
};

QVector<TobiiResearchGazeData> EyeTrackerWrapper::get_gaze_data()
{
    return EyeTrackerWrapper::gaze_data;
};

TobiiResearchGazeData EyeTrackerWrapper::get_current_gaze_data()
{
    return EyeTrackerWrapper::current_gaze_data;
};

TobiiResearchUserPositionGuide EyeTrackerWrapper::get_user_position()
{
    return EyeTrackerWrapper::user_position;
};

void EyeTrackerWrapper::gaze_data_callback(TobiiResearchGazeData *gaze_data, void *user_data)
{
    memcpy(user_data, gaze_data, sizeof(*gaze_data));
    if ((gaze_data->left_eye.gaze_point.validity == TOBII_RESEARCH_VALIDITY_VALID) ||
        (gaze_data->right_eye.gaze_point.validity == TOBII_RESEARCH_VALIDITY_VALID))
        EyeTrackerWrapper::gaze_data.append(*gaze_data);
};

void EyeTrackerWrapper::user_position_guide_callback(TobiiResearchUserPositionGuide *user_position_guide, void *user_data)
{
    memcpy(user_data, user_position_guide, sizeof(*user_position_guide));
};

TobiiResearchTrackBox EyeTrackerWrapper::get_track_box()
{
    TobiiResearchTrackBox track_box;
    if (this->eyetracker)
    {
        tobii_research_get_track_box(this->eyetracker, &track_box);
    }
    return track_box;
};

EyeTrackerWrapper::EyeTrackers EyeTrackerWrapper::find_eyetrackers()
{
    EyeTrackerWrapper::EyeTrackers eyetrackers;
    TobiiResearchStatus result;
    result = tobii_research_find_all_eyetrackers(&eyetrackers.mp_eyetrackers);
    if (result != TOBII_RESEARCH_STATUS_OK)
    {
        qDebug() << QString("Finding trackers failed. Error: %d\n").arg(result);
    }
    return eyetrackers;
};

int64_t EyeTrackerWrapper::get_system_time_stamp()
{
    int64_t time_stamp_us;
    tobii_research_get_system_time_stamp(&time_stamp_us);
    return time_stamp_us;
};

EyeTrackerWrapper::EyeTrackerInfo EyeTrackerWrapper::get_eyetracker_info(TobiiResearchEyeTracker *eyetracker)
{
    EyeTrackerInfo info;
    char *address = nullptr;
    char *serial_number = nullptr;
    char *device_name = nullptr;
    char *model = nullptr;
    tobii_research_get_address(eyetracker, &address);
    tobii_research_get_serial_number(eyetracker, &serial_number);
    tobii_research_get_device_name(eyetracker, &device_name);
    tobii_research_get_model(eyetracker, &model);
    info["address"] = QString(address);
    info["serial_number"] = QString(serial_number);
    info["device_name"] = QString(device_name);
    info["model"] = QString(model);
    tobii_research_free_string(address);
    tobii_research_free_string(serial_number);
    tobii_research_free_string(device_name);
    return info;
};
