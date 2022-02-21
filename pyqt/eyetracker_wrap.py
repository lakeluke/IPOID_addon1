# !/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import time
import logging
import tobii_research as tr


class EyeTrackerWrapper:
    @staticmethod
    def find_eyetrackers():
        eyetrackers = tr.find_all_eyetrackers()
        return eyetrackers

    @staticmethod
    def get_system_time_stamp():
        system_time_stamp = tr.get_system_time_stamp()
        return system_time_stamp

    def __init__(self, address='tet-tcp://'):
        address_pattern = 'tet-tcp://((([0-9]{1,3})\.){3}([0-9]{1,3}))'
        if re.match(address_pattern, address):
            try:
                self.eyetracker = tr.EyeTracker(address)
                self.address = self.eyetracker.address
                self.model = self.eyetracker.model
                self.device_name = self.eyetracker.device_name
                self.serial_number = self.eyetracker.serial_number
                self.clear_gaze_data()
                self.user_position = {}
            except:
                print('given address:{0} connect error!'.format(address))
        else:
            if address == 'tet-tcp://':
                eyetrackers = self.find_eyetrackers()
                if len(eyetrackers):
                    self.eyetracker = eyetrackers[0]
                    self.address = self.eyetracker.address
                    self.model = self.eyetracker.model
                    self.device_name = self.eyetracker.device_name
                    self.serial_number = self.eyetracker.serial_number
                    self.clear_gaze_data()
                    self.user_position = {}
                    print('connect default eyetracker')
                else:
                    self.eyetracker = None
                    print('no eyetracker was found!')
            else:
                print('given address:{0} invalid!'.format(address))

    def frequency_options(self):
        if self.eyetracker:
            return self.eyetracker.get_all_gaze_output_frequencies()
        else:
            return (60, 120, 250, 300)

    def get_frequency(self):
        if self.eyetracker:
            return self.eyetracker.get_gaze_output_frequency()

    def set_frequency(self, frequency=60):
        if self.eyetracker:
            self.eyetracker.set_gaze_output_frequency(frequency)

    def calibration_start(self):
        if self.eyetracker:
            self.calibration = tr.ScreenBasedCalibration(self.eyetracker)
            self.calibration.enter_calibration_mode()

    def calibration_collect(self, point, recollect=False):
        if recollect:
            self.calibration.discard_data(point[0], point[1])
        if self.calibration.collect_data(
                point[0], point[1]) != tr.CALIBRATION_STATUS_SUCCESS:
            # Try again if it didn't go well the first time.
            # Not all eye tracker models will fail at this point, but instead fail on ComputeAndApply.
            self.calibration.collect_data(point[0], point[1])

    def calibration_apply(self):
        calibration_result = self.calibration.compute_and_apply()
        return calibration_result

    def calibration_end(self):
        self.calibration.leave_calibration_mode()

    def get_calibration_data(self):
        if self.eyetracker:
            return self.eyetracker.retrieve_calibration_data()

    def apply_calibration_data(self, calibration_data):
        if self.eyetracker:
            self.eyetracker.apply_calibration_data(calibration_data)

    def clear_gaze_data(self):
        self.gaze_data = []
        self.current_gaze_data = {}

    def get_gaze_data(self):
        return self.gaze_data

    def get_current_gaze_data(self):
        return self.current_gaze_data

    def gaze_data_callback(self, gaze_data):
        self.current_gaze_data = gaze_data
        if not len(gaze_data):
            logging.error('gaze_data is null')
        elif gaze_data['left_gaze_point_validity'] or gaze_data[
                'right_gaze_point_validity']:
            self.gaze_data.append(gaze_data)

    def subscribe_gaze_data(self, ):
        self.clear_gaze_data()
        if self.eyetracker:
            try:
                self.eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA,
                                             self.gaze_data_callback,
                                             as_dictionary=True)
            except:
                self.unsubscribe_gaze_data()
                self.eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA,
                                             self.gaze_data_callback,
                                             as_dictionary=True)

    def unsubscribe_gaze_data(self):
        if self.eyetracker:
            self.eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA,
                                             self.gaze_data_callback)
            return self.gaze_data

    def user_position_guide_callback(self, user_position):
        self.user_position = user_position

    def subscribe_user_position(self):
        self.user_position = {}
        if self.eyetracker:
            try:
                self.eyetracker.subscribe_to(tr.EYETRACKER_USER_POSITION_GUIDE,
                                             self.user_position_guide_callback,
                                             as_dictionary=True)
            except:
                self.unsubscribe_user_position()
                self.eyetracker.subscribe_to(tr.EYETRACKER_USER_POSITION_GUIDE,
                                             self.user_position_guide_callback,
                                             as_dictionary=True)

    def unsubscribe_user_position(self):
        if self.eyetracker:
            self.eyetracker.unsubscribe_from(tr.EYETRACKER_USER_POSITION_GUIDE,
                                             self.user_position_guide_callback)

    def get_user_position(self):
        return self.user_position

    def get_track_box(self):
        if self.eyetracker:
            return self.eyetracker.get_track_box()


if __name__ == '__main__':
    eyetracker_wp = EyeTrackerWrapper()
    eyetracker_wp.set_frequency()
    eyetracker_wp.subscribe_gaze_data()
    time.sleep(1)
    eyetracker_wp.unsubscribe_gaze_data()
    gaze_data = eyetracker_wp.get_gaze_data()
    print(str(len(gaze_data)) + '@')
    print(gaze_data[-1])

    eyetracker_wp.subscribe_user_position()
    user_position = eyetracker_wp.get_user_position()
    print(user_position)
    time.sleep(2)
    eyetracker_wp.unsubscribe_user_position()

    print(eyetracker_wp.eyetracker.device_capabilities)
    print(eyetracker_wp.eyetracker.get_all_gaze_output_frequencies())
    print(eyetracker_wp.eyetracker.get_all_eye_tracking_modes())
