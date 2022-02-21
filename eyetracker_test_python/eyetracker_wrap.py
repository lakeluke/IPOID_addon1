import tobii_research as tr 
import re
import time
import os
import subprocess
import platform
import glob
from tobiiresearch.interop.interop import calibration_enter_calibration_mode

class EyeTrackerWrapper:
    @staticmethod
    def find_eyetrackers():
        eyetrackers = tr.find_all_eyetrackers()
        return eyetrackers
    
    def __init__(self, address='tet-tcp://'):
        address_pattern = 'tet-tcp://((([0-9]{1,3})\.){3}([0-9]{1,3}))'
        if re.match(address_pattern,address):
            try:
                self.eyetracker = tr.EyeTracker(address)
                self.address = self.eyetracker.address
                self.model = self.eyetracker.model
                self.device_name = self.eyetracker.device_name
                self.serial_number = self.eyetracker.serial_number
                self.clear_gaze_data()
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
                    print('connect default eyetracker')
                else:
                    print('no eyetracker was found!')
            else:
                print('given address:{0} invalid!'.format(address))
    
    
    def calibration_start(self):
        self.calibration = tr.ScreenBasedCalibration(self.eyetracker)
        self.calibration.enter_calibration_mode()
        
    def calibration_collect(self,point,recollect=False):
        if recollect:
            self.calibration.discard_data(point[0],point[1])
        if self.calibration.collect_data(point[0], point[1]) != tr.CALIBRATION_STATUS_SUCCESS:
            # Try again if it didn't go well the first time.
            # Not all eye tracker models will fail at this point, but instead fail on ComputeAndApply.
            self.calibration.collect_data(point[0], point[1])   

    def calibration_apply(self):
        calibration_result = self.calibration.compute_and_apply()
        return calibration_result
    
    def calibration_end(self):
        self.calibration.leave_calibration_mode()    

    def get_calibration_data(self):
        return self.eyetracker.retrieve_calibration_data()
    
    def apply_calibration_data(self,calibration_data):
        self.eyetracker.apply_calibration_data(calibration_data)

    def clear_gaze_data(self):
        self.gaze_data = []
        
    def get_gaze_data(self):
        return self.gaze_data
    
    def gaze_data_callback(self,gaze_data):
        self.gaze_data = gaze_data
        
    def subscribe_gaze_data(self,):
        self.eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA,
                                     self.gaze_data_callback,
                                     as_dictionary=True)
        
    def unsubscribe_gaze_data(self):
        self.eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback)
        return self.gaze_data


if __name__ == '__main__':
    eyetracker_wp = EyeTrackerWrapper()
    eyetracker_wp.subscribe_gaze_data()
    time.sleep(1)
    eyetracker_wp.unsubscribe_gaze_data()
    gaze_data = eyetracker_wp.get_gaze_data()
    print(gaze_data)
    print(eyetracker_wp.eyetracker.device_capabilities)
    print(eyetracker_wp.eyetracker.get_all_gaze_output_frequencies())
    print(eyetracker_wp.eyetracker.get_all_eye_tracking_modes())
    
    
    
    