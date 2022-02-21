class Demos:
    # other usage demoes 
    @staticmethod
    def set_device_name(eyetracker,new_name):
        current_device_name = eyetracker.device_name
        try:
            eyetracker.set_device_name(new_name)
            print("The eye tracker changed name to {0}".format(device_name))
        except tr.EyeTrackerFeatureNotSupportedError:
            print("This eye tracker doesn't support changing the device name.")
        except tr.EyeTrackerLicenseError:
            print("You need a higher level license to change the device name.")


    @staticmethod
    def set_eye_tracking_mode(eyetracker,mode=None):
        if mode:
            eyetracker.set_eye_tracking_mode(mode)
        else:
            initial_eye_tracking_mode = eyetracker.get_eye_tracking_mode()
            print("The eye tracker's initial eye tracking mode is {0}.".format(initial_eye_tracking_mode))
            try:
                for eye_tracking_mode in eyetracker.get_all_eye_tracking_modes():
                    eyetracker.set_eye_tracking_mode(eye_tracking_mode)
                    print("Eye tracking mode set to {0}.".format(eye_tracking_mode))
            finally:
                eyetracker.set_eye_tracking_mode(initial_eye_tracking_mode)
                print("Eye tracking mode reset to {0}.".format(initial_eye_tracking_mode))
               
    @staticmethod
    def set_gaze_output_frequency(frequency=None):
        if frequency:
            eyetracker.set_gaze_output_frequency(frequency)
        else:
            initial_gaze_output_frequency = eyetracker.get_gaze_output_frequency()
            print("The eye tracker's initial gaze output frequency is {0} Hz.".format(initial_gaze_output_frequency))
            try:
                for gaze_output_frequency in eyetracker.get_all_gaze_output_frequencies():
                    eyetracker.set_gaze_output_frequency(gaze_output_frequency)
                    print("Gaze output frequency set to {0} Hz.".format(gaze_output_frequency))
            finally:
                eyetracker.set_gaze_output_frequency(initial_gaze_output_frequency)
                print("Gaze output frequency reset to {0} Hz.".format(initial_gaze_output_frequency))
    
    @staticmethod
    def get_and_set_display_area(eyetracker):
        display_area = eyetracker.get_display_area()

        print("Got display area from tracker with serial number {0}:".format(eyetracker.serial_number))

        print("Bottom Left: {0}".format(display_area.bottom_left))
        print("Bottom Right: {0}".format(display_area.bottom_right))
        print("Height: {0}".format(display_area.height))
        print("Top Left: {0}".format(display_area.top_left))
        print("Top Right: {0}".format(display_area.top_right))
        print("Width: {0}".format(display_area.width))

        # To set the display area it is possible to either use a previously saved instance of
        # the class Display area, or create a new one as shown bellow.
        new_display_area_dict = dict()
        new_display_area_dict['top_left'] = display_area.top_left
        new_display_area_dict['top_right'] = display_area.top_right
        new_display_area_dict['bottom_left'] = display_area.bottom_left

        new_display_area = tr.DisplayArea(new_display_area_dict)

        eyetracker.set_display_area(new_display_area)
    
    @staticmethod
    def get_system_time_stamp():
        system_time_stamp = tr.get_system_time_stamp()
        return system_time_stamp    
    
    @staticmethod
    def get_track_box(eyetracker):
        track_box = eyetracker.get_track_box()
        print("Got track box from tracker with serial number {0} with corners:".format(eyetracker.serial_number))
        print("Back Lower Left: {0}".format(track_box.back_lower_left))
        print("Back Lower Right: {0}".format(track_box.back_lower_right))
        print("Back Upper Left: {0}".format(track_box.back_upper_left))
        print("Back Upper Right: {0}".format(track_box.back_upper_right))
        print("Front Lower Left: {0}".format(track_box.front_lower_left))
        print("Front Lower Right: {0}".format(track_box.front_lower_right))
        print("Front Upper Left: {0}".format(track_box.front_upper_left))
        print("Front Upper Right: {0}".format(track_box.front_upper_right))

    @staticmethod
    def notification_callback(notification, data):
        print("Notification {0} received at time stamp {1}.".format(notification, data.system_time_stamp))

    @staticmethod
    def notifications(eyetracker):
        all_notifications =\
            (tr.EYETRACKER_NOTIFICATION_CONNECTION_LOST,
            tr.EYETRACKER_NOTIFICATION_CONNECTION_RESTORED,
            tr.EYETRACKER_NOTIFICATION_CALIBRATION_MODE_ENTERED,
            tr.EYETRACKER_NOTIFICATION_CALIBRATION_MODE_LEFT,
            tr.EYETRACKER_NOTIFICATION_CALIBRATION_CHANGED,
            tr.EYETRACKER_NOTIFICATION_TRACK_BOX_CHANGED,
            tr.EYETRACKER_NOTIFICATION_DISPLAY_AREA_CHANGED,
            tr.EYETRACKER_NOTIFICATION_GAZE_OUTPUT_FREQUENCY_CHANGED,
            tr.EYETRACKER_NOTIFICATION_EYE_TRACKING_MODE_CHANGED,
            tr.EYETRACKER_NOTIFICATION_DEVICE_FAULTS,
            tr.EYETRACKER_NOTIFICATION_DEVICE_WARNINGS)

        # Subscribe to all notifications.
        for notification in all_notifications:
            eyetracker.subscribe_to(notification,
                                    lambda x, notification=notification: Demos.notification_callback(notification, x))
            print("Subscribed to {0} for eye tracker with serial number {1}.".
                format(notification, eyetracker.serial_number))

        # Trigger some notifications
        calibration = tr.ScreenBasedCalibration(eyetracker)

        calibration.enter_calibration_mode()

        calibration.leave_calibration_mode()

        # Unsubscribe from notifications.
        for notification in all_notifications:
            eyetracker.unsubscribe_from(notification)
            print("Unsubscribed from {0}.".format(notification))
    
    @staticmethod
    def stream_error_callback(stream_error_data):
        print(stream_error_data)
        
    @staticmethod
    def eye_image_callback(eye_image_data):
        # TX300 not support eye_image
        print(eye_image_data)
    
    @staticmethod
    def stream_errors(eyetracker):
        print("Subscribing to stream errors for eye tracker with serial number {0}.".format(eyetracker.serial_number))
        eyetracker.subscribe_to(tr.EYETRACKER_STREAM_ERRORS, Demos.stream_error_callback, as_dictionary=True)
    
        # Trigger an error by subscribing to something not supported.
        eyetracker.subscribe_to(tr.EYETRACKER_EYE_IMAGES, Demos.eye_image_callback)
        time.sleep(1)
        eyetracker.unsubscribe_from(tr.EYETRACKER_EYE_IMAGES, Demos.eye_image_callback)

        eyetracker.subscribe_to(tr.EYETRACKER_TIME_SYNCHRONIZATION_DATA,
                                Demos.time_synchronization_data_callback, as_dictionary=True)
        # Wait while some time synchronization data is collected.
        time.sleep(2)
        eyetracker.unsubscribe_from(tr.EYETRACKER_TIME_SYNCHRONIZATION_DATA,
                                    Demos.time_synchronization_data_callback)
        eyetracker.unsubscribe_from(tr.EYETRACKER_STREAM_ERRORS, Demos.stream_error_callback)
        print("Unsubscribed from stream errors.")
   
    @staticmethod
    def time_synchronization_data_callback(time_synchronization_data):
        print(time_synchronization_data)
   
    @staticmethod
    def time_synchronization_data(eyetracker):
        print("Subscribing to time synchronization data for eye tracker with serial number {0}.".
              format(eyetracker.serial_number))
        eyetracker.subscribe_to(tr.EYETRACKER_TIME_SYNCHRONIZATION_DATA,
                                Demos.time_synchronization_data_callback, as_dictionary=True)
    
        # Wait while some time synchronization data is collected.
        time.sleep(2)
    
        eyetracker.unsubscribe_from(tr.EYETRACKER_TIME_SYNCHRONIZATION_DATA,
                                    Demos.time_synchronization_data_callback)
        print("Unsubscribed from time synchronization data.")
    
    user_position_guide = None
    @staticmethod
    def user_position_guide_callback(user_position_guide):
        Demos.user_position_guide = user_position_guide
    
    @staticmethod
    def user_position_guide(eyetracker):
        print("Subscribing to user position guide for eye tracker with serial number {0}.".format(eyetracker.serial_number))
        eyetracker.subscribe_to(tr.EYETRACKER_USER_POSITION_GUIDE, Demos.user_position_guide_callback, as_dictionary=True)
        # Wait while some user position guide is collected.
        time.sleep(2)
        eyetracker.unsubscribe_from(tr.EYETRACKER_USER_POSITION_GUIDE, Demos.user_position_guide_callback)
        print("Unsubscribed from user position guide.")
        print("Last received user position guide package:")
        print(Demos.user_position_guide)
        
    @staticmethod
    def call_eyetracker_manager():
        try:
            os_type = platform.system()
            ETM_PATH = ''
            DEVICE_ADDRESS = ''
            if os_type == "Windows":
                ETM_PATH = glob.glob(os.environ["LocalAppData"] +
                                    "/TobiiProEyeTrackerManager/app-*/TobiiProEyeTrackerManager.exe")[0]
                DEVICE_ADDRESS = "tet-tcp://169.254.78.123"
            elif os_type == "Linux":
                ETM_PATH = "/opt/TobiiProEyeTrackerManager/tobiiproeyetrackermanager"
                DEVICE_ADDRESS = 'tet-tcp://169.254.78.123'
            elif os_type == "Darwin":
                ETM_PATH = "/Applications/TobiiProEyeTrackerManager.app/Contents/MacOS/TobiiProEyeTrackerManager"
                DEVICE_ADDRESS = 'tet-tcp://169.254.78.123'
            else:
                print("Unsupported...")
                exit(1)
            eyetracker = tr.EyeTracker(DEVICE_ADDRESS)
            mode = "displayarea"
            etm_p = subprocess.Popen([ETM_PATH,
                                    # "--device-address=" + eyetracker.address,
                                    # "--mode=" + mode
                                    ],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=False)
            stdout, stderr = etm_p.communicate()  # Returns a tuple with (stdout, stderr)
            if etm_p.returncode == 0:
                print("Eye Tracker Manager was called successfully!")
            else:
                print("Eye Tracker Manager call returned the error code: " + str(etm_p.returncode))
                errlog = None
                if os_type == "Windows":
                    errlog = stdout  # On Windows ETM error messages are logged to stdout
                else:
                    errlog = stderr
                for line in errlog.splitlines():
                    if line.startswith("ETM Error:"):
                        print(line)
        except Exception as e:
            print(e)  
