"""
The class:
manages the connection to the eye tracker, 
configure the eye tracker settings,
runs calibration and validation procedures,
start and stop recording of eye movements,
handles trials,
and save both the raw data and the processed eye movement events to files.
"""

import pylink
import os

class EyeTrackerHandler:
    def __init__(self, dummy_mode=False, edf_filename="TEST.EDF"):
        self.dummy_mode = dummy_mode
        self.edf_filename = edf_filename
        self.el_tracker = None
        self.trial_condition = ['condition1', 'condition2', 'condition3']
        self.results_folder = 'results'
        self.setup_eye_tracker()

    def initialize(self, ip_address="100.1.1.1"):
        """
        Initialize the connection to the EyeLink tracker and perform other initial setups
        """
        if self.dummy_mode:
            self.el_tracker = pylink.EyeLink(None)
        else:
            try:
                self.el_tracker = pylink.EyeLink(ip_address)
                self.connected = True
            except RuntimeError as e:
                print(f"Failed to connect to the EyeLink: {e}")
                self.connected = False
        self.el_tracker.openDataFile(self.edf_filename)
        print("EyeLink Initialized")
    
    def setup_eye_tracker(self):
        if not os.path.exists(self.results_folder):
            os.makedirs(self.results_folder)
        
        if self.dummy_mode:
            self.el_tracker = pylink.EyeLink(None)
        else:
            self.el_tracker = pylink.EyeLink("100.1.1.1")
        
        pylink.openGraphics()
        self.el_tracker.openDataFile(self.edf_filename)
        preamble_text = 'RECORDED BY EyeTrackerHandler'
        self.el_tracker.sendCommand(f"add_file_preamble_text '{preamble_text}'")
        self.configure_tracker_settings()

    def configure_tracker_settings(self):
        self.el_tracker.setOfflineMode()
        scn_width, scn_height = pylink.getDisplayInformation().width, pylink.getDisplayInformation().height
        self.el_tracker.sendCommand(f"screen_pixel_coords 0 0 {scn_width - 1} {scn_height - 1}")
        self.el_tracker.sendMessage(f"DISPLAY_COORDS  0 0 {scn_width - 1} {scn_height - 1}")
        self.el_tracker.sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT")
        self.el_tracker.sendCommand("file_sample_data = LEFT,RIGHT,GAZE,HREF,RAW,AREA,HTARGET,GAZERES,BUTTON,STATUS,INPUT")
        self.el_tracker.sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,FIXUPDATE,INPUT")
        self.el_tracker.sendCommand("link_sample_data = LEFT,RIGHT,GAZE,GAZERES,AREA,HTARGET,STATUS,INPUT")
        pylink.setCalibrationColors((0, 0, 0), (128, 128, 128))
        pylink.setTargetSize(int(scn_width/70.0), int(scn_width/300.))
        pylink.setCalibrationSounds("", "", "")
        pylink.setDriftCorrectSounds("", "", "")

    def do_calibration(self):
        """
        Calibrate the Eye Tracker
        """
        if self.connected:
            self.el_tracker.doTrackerSetup()
        else:
            print("EyeLink Tracker not connected.")
    
    def start_recording(self, trial_id):
        """
        Initiate the trial session and start the data recording
        """
        if self.connected:
            self.el_tracker.sendCommand('set_idle_mode')
            # More settings can be applied here
            self.el_tracker.startRecording(1, 1, 1, 1)
            pylink.beginRealTimeMode(100)  # Start real-time mode to reduce data delays
            self.el_tracker.sendMessage(f"TRIALID {trial_id}")
        else:
            print("EyeLink Tracker not connected.")
    
    def stop_recording(self):
        """
        End the trial and stop the data recording
        """
        if self.connected:
            pylink.endRealTimeMode()
            pylink.pumpDelay(100)  # Include a short delay
            self.el_tracker.stopRecording()
        else:
            print("EyeLink Tracker not connected.")
    
    def close(self):
        """
        Perform cleanup and close the connection to the eye tracker
        """
        if self.el_tracker is not None:
            self.el_tracker.setOfflineMode()
            pylink.msecDelay(500)
            self.el_tracker.closeDataFile()
            self.el_tracker.receiveDataFile(self.edf_filename, os.path.basename(self.edf_filename))
            self.el_tracker.close()
        print("EyeLink Closed")

    def run_trials(self, n_trials=3, trial_duration=5000):
        for trial in range(n_trials):
            if not self.el_tracker.isConnected() or self.el_tracker.breakPressed():
                break
            self.do_trial(trial, trial_duration)
    
    def do_trial(self, trial, trial_duration):
        # This method will be responsible for running a single trial
        # It should include logic for:
        # - Performing drift correction
        # - Starting and stopping recording
        # - Processing and saving eye movement data
        # Please refer to the provided script for detailed implementation.
        pass

    def cleanup(self):
        if self.el_tracker is not None:
            self.el_tracker.setOfflineMode()
            pylink.msecDelay(500)
            self.el_tracker.closeDataFile()
            local_file_name = os.path.join(self.results_folder, self.edf_filename)
            self.el_tracker.receiveDataFile(self.edf_filename, local_file_name)
            self.el_tracker.close()
            pylink.closeGraphics()

# Example of using this class
if __name__ == "__main__":
    et_handler = EyeTrackerHandler(dummy_mode=False, edf_filename="experiment.EDF")
    et_handler.initialize(ip_address="100.1.1.1")
    et_handler.do_calibration()
    for trial_id in range(3):  # For 3 trials
        print(f"Starting trial {trial_id}")
        et_handler.start_recording(trial_id=trial_id)
        # [Run your experiment trial here]
        print(f"Trial {trial_id} complete")
        et_handler.stop_recording()
    et_handler.close()
