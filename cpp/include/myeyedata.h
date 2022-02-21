#ifndef MYEYEDATA_H
#define MYEYEDATA_H
#include <vector>

struct Point2D{
    float x,y;
};

struct Point3D{
    float x,y,z;
};

enum CalibrationEyeValidity{
    UNKNOWN = 0,
    VALID_AND_USED = 1,
    VALID_BUT_NOT_USED = 2,
    INVALID_AND_NOT_USED = 3
};

struct CalibrationEyeData{
    Point2D pos_on_dp_area;
    CalibrationEyeValidity validity;
};

struct CalibrationSample{
    CalibrationEyeData left_eye;
    CalibrationEyeData right_eye;
};

enum CalibrationStatus{
    FAILURE = 0,
    SUCCESS = 1,
    SUCCESS_LEFT_EYE = 2,
    SUCCESS_RIGHT_EYE = 3
};

struct CalibrationPoint{
    Point2D pos_on_dp_area;
    std::vector<CalibrationSample> calibration_samples;
};

struct CalibrationResult{
    std::vector<CalibrationPoint> calibration_points;
    CalibrationStatus status;
};

struct GazePoint{
    Point2D pos_on_dp_area;
    Point3D pos_ucs;
    bool validity;
};

struct PupilData{
    float diameter;
    bool validity;
};

struct GazeOrigin{
    Point3D pos_ucs;
    Point3D pos_tbcs;
    bool validity;
};


#ifdef TOBII_RESEARCH_H_

#endif

#endif // MYEYEDATA_H
