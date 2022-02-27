#include "eyetrackerwrapper.h"
#include <QRegularExpression>

EyeTrackerWrapper::EyeTrackerWrapper()
{
    TobiiResearchEyeTrackers *eyetrackers = nullptr;
    TobiiResearchStatus result;
    result = tobii_research_find_all_eyetrackers(&eyetrackers);
    if (result != TOBII_RESEARCH_STATUS_OK)
    {
        qDebug() << QString("Finding trackers failed. Error: %1").arg(result);
        goto CLEAR_EYETRACKER;
    }
    else if (eyetrackers->count > 0)
    {
    qDebug() << QString("Find %1 eyetrackers").arg(eyetrackers->count);
        eyetracker = eyetrackers->eyetrackers[0];
        EyeTrackerInfo info = this->get_eyetracker_info(eyetracker);
        this->address = info["address"].toString();
        this->serial_number = info["serial_number"].toString();
        this->device_name = info["device_name"].toString();
        this->model = info["model"].toString();
        tobii_research_get_track_box(this->eyetracker, &this->tbx);
        tobii_research_get_eyetracker(this->address.toLatin1().data(), &this->eyetracker);
        tobii_research_free_eyetrackers(eyetrackers);
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
            qDebug() << QString("Finding tracker of address: %1 failed. Error: %2").arg(address).arg(status)
                     << QString("Use Default Constructor");
            new (this) EyeTrackerWrapper();
        }
        else
        {
            EyeTrackerInfo info = this->get_eyetracker_info(this->eyetracker);
            this->address = info["address"].toString();
            this->serial_number = info["serial_number"].toString();
            this->device_name = info["device_name"].toString();
            this->model = info["model"].toString();
            tobii_research_get_track_box(this->eyetracker, &this->tbx);
        };
    }
    else
    {
        qDebug() << QString("Given address: %1 format invalid").arg(address)
                 << QString("Use Default Constructor");
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
        tobii_research_get_gaze_output_frequency(this->eyetracker, &current_frequency);
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

void EyeTrackerWrapper::calibration_collect(const MyFPoint2D &cpoint, bool recollect)
{
    if (eyetracker)
    {
        TobiiResearchNormalizedPoint2D point = {cpoint[0], cpoint[1]};
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

TobiiResearchCalibrationResult* EyeTrackerWrapper::calibration_apply()
{
    TobiiResearchCalibrationResult *presult;
    if (eyetracker)
    {
        TobiiResearchStatus status;
        status = tobii_research_screen_based_calibration_compute_and_apply(eyetracker, &presult);
        if (status == TOBII_RESEARCH_STATUS_OK && presult->status == TOBII_RESEARCH_CALIBRATION_SUCCESS)
        {
            qDebug() << QString("Compute and apply returned %1 and collected at %2 points.").arg(status).arg(presult->calibration_point_count);
        }
        else
        {
            qDebug() << QString("Calibration failed!");
        }
    }
    return presult;
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

void EyeTrackerWrapper::subscribe_gaze_data(tobii_research_gaze_data_callback gaze_data_callback,
                                            TobiiResearchGazeData &gaze_data)
{
    if (eyetracker)
    {
        TobiiResearchStatus status = tobii_research_subscribe_to_gaze_data(eyetracker,
                                                                           gaze_data_callback,
                                                                           &gaze_data);
        if (status != TOBII_RESEARCH_STATUS_OK)
        {
            tobii_research_unsubscribe_from_gaze_data(eyetracker, gaze_data_callback);
            tobii_research_subscribe_to_gaze_data(eyetracker,
                                                  gaze_data_callback,
                                                  &gaze_data);
        }
    }
};

void EyeTrackerWrapper::unsubscribe_gaze_data(tobii_research_gaze_data_callback callback_func)
{
    if (this->eyetracker)
    {
        tobii_research_unsubscribe_from_gaze_data(this->eyetracker, callback_func);
    }
};

// user position guide
void EyeTrackerWrapper::subscribe_user_position(tobii_research_user_position_guide_callback callback_func,TobiiResearchUserPositionGuide& user_position)
{
    if (this->eyetracker)
    {
        TobiiResearchStatus status;
        status = tobii_research_subscribe_to_user_position_guide(this->eyetracker, callback_func, &user_position);
        if (status != TOBII_RESEARCH_STATUS_OK)
        {
            tobii_research_unsubscribe_from_user_position_guide(this->eyetracker, callback_func);
            tobii_research_subscribe_to_user_position_guide(this->eyetracker,
                                                            callback_func,
                                                            &user_position);
        }
    }
};

void EyeTrackerWrapper::unsubscribe_user_position(tobii_research_user_position_guide_callback callback_func)
{
    if (this->eyetracker)
    {
        tobii_research_unsubscribe_from_user_position_guide(this->eyetracker, callback_func);
    }
};

TobiiResearchTrackBox EyeTrackerWrapper::get_track_box()
{
    return this->tbx;
};

EyeTrackerWrapper::EyeTrackerInfo EyeTrackerWrapper::get_info()
{
    return EyeTrackerWrapper::get_eyetracker_info(this->eyetracker);
};
// other static methods
EyeTrackerWrapper::EyeTrackers EyeTrackerWrapper::find_eyetrackers()
{
    EyeTrackerWrapper::EyeTrackers eyetrackers;
    TobiiResearchStatus result;
    result = tobii_research_find_all_eyetrackers(&eyetrackers.mp_eyetrackers);
    if (result != TOBII_RESEARCH_STATUS_OK)
    {
        qDebug() << QString("Finding trackers failed.").arg(result);
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

QVariantHash convert_to_QVariantHash(TobiiResearchCalibrationPoint cali_point)
{
    QVariantHash hash_table;
    hash_table["pos_dpa"] = QList<QVariant>({cali_point.position_on_display_area.x,
                                             cali_point.position_on_display_area.y});
    QList<QVariant> calibration_samples;
    calibration_samples.reserve(cali_point.calibration_sample_count);
    for (size_t i = 0; i < cali_point.calibration_sample_count; ++i)
    {
        TobiiResearchCalibrationSample sample = cali_point.calibration_samples[i];
        QVariantHash data;
        QVariantHash left_eye, right_eye;
        left_eye["pos_dpa"] = QList<QVariant>({sample.left_eye.position_on_display_area.x,
                                               sample.left_eye.position_on_display_area.y});
        left_eye["validity"] = sample.left_eye.validity;
        right_eye["pos_dpa"] = QList<QVariant>({sample.right_eye.position_on_display_area.x,
                                                sample.right_eye.position_on_display_area.y});
        right_eye["validity"] = sample.right_eye.validity;
        data["left_eye"] = left_eye;
        data["right_eye"] = right_eye;
        calibration_samples[i] = data;
    }
    hash_table["calibration_samples"] = calibration_samples;
    return hash_table;
};

QVariantHash convert_to_QVariantHash(TobiiResearchGazePoint gaze_point)
{
    QVariantHash hash_table;
    hash_table["pos_dpa"] = QList<QVariant>({gaze_point.position_on_display_area.x,
                                             gaze_point.position_on_display_area.y});
    hash_table["pos_ucs"] = QList<QVariant>({gaze_point.position_in_user_coordinates.x,
                                             gaze_point.position_in_user_coordinates.y,
                                             gaze_point.position_in_user_coordinates.z});
    hash_table["validity"] = gaze_point.validity;
    return hash_table;
};

QVariantHash convert_to_QVariantHash(TobiiResearchGazeOrigin gaze_origin)
{
    QVariantHash hash_table;
    hash_table["pos_tbcs"] = QList<QVariant>({gaze_origin.position_in_track_box_coordinates.x,
                                              gaze_origin.position_in_track_box_coordinates.y,
                                              gaze_origin.position_in_track_box_coordinates.z});
    hash_table["pos_ucs"] = QList<QVariant>({gaze_origin.position_in_user_coordinates.x,
                                             gaze_origin.position_in_user_coordinates.y,
                                             gaze_origin.position_in_user_coordinates.z});
    hash_table["validity"] = gaze_origin.validity;
    return hash_table;
};

QVariantHash convert_to_QVariantHash(TobiiResearchGazeData gaze_data)
{
    QVariantHash hash_table;
    hash_table["device_time_stamp"] = QString("%1").arg(gaze_data.device_time_stamp);
    hash_table["system_time_stamp"] = QString("%1").arg(gaze_data.system_time_stamp);
    QVariantHash left_eye, right_eye;
    left_eye["gaze_point"] = convert_to_QVariantHash(gaze_data.left_eye.gaze_point);
    left_eye["gaze_origin"] = convert_to_QVariantHash(gaze_data.left_eye.gaze_origin);
    right_eye["gaze_point"] = convert_to_QVariantHash(gaze_data.right_eye.gaze_point);
    right_eye["gaze_origin"] = convert_to_QVariantHash(gaze_data.right_eye.gaze_origin);
    QVariantHash pupil_data;
    pupil_data["diameter"] = gaze_data.left_eye.pupil_data.diameter;
    pupil_data["validity"] = gaze_data.left_eye.pupil_data.validity;
    left_eye["pupil_data"] = pupil_data;
    pupil_data["diameter"] = gaze_data.right_eye.pupil_data.diameter;
    pupil_data["validity"] = gaze_data.right_eye.pupil_data.validity;
    right_eye["pupil_data"] = pupil_data;
    hash_table["left_eye"] = left_eye;
    hash_table["right_eye"] = right_eye;
    return hash_table;
};
