from __future__ import division, print_function
import os
import sys
import pylink
import subprocess


"""
This program: Call it start.py
1) sets up eye tracker, and allows the the user to calibrate, validate and record Fixation and Saccades
    # 1-initializing connection to the tracker
    # 2-initializing display-side graphics
    # 3-initializing data file
    # 4-setting up tracking, recording and calibration options
    # 5-initial tracker calibration
2) Calls the experiment.py script to run the experiment passing el_tracker as a parameter 

"""



# Set your screen resolution here
SCN_WIDTH = 1920
SCN_HEIGHT = 1080

# Dummy mode flag - set to True if no real tracker is connected
dummy_mode = False

# Create a results folder to store data files
results_folder = 'results'
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

def initialize_tracker():
    """Initializes the EyeLink tracker."""
    if dummy_mode:
        el_tracker = pylink.EyeLink(None)
        print('Dummy mode activated. No real-time eye tracking data will be available.')
    else:
        try:
            el_tracker = pylink.EyeLink("100.1.1.1")
        except RuntimeError as error:
            print('ERROR:', error)
            sys.exit()
    return el_tracker

def setup_display(el_tracker):
    """Initializes the display-side graphics."""
    pylink.openGraphics((SCN_WIDTH, SCN_HEIGHT), 32)

def setup_data_file(el_tracker):
    """Opens an EDF data file on the Host PC."""
    edf_file_name = "TEST.EDF"
    el_tracker.openDataFile(edf_file_name)
    preamble_text = 'RECORDED BY %s' % os.path.basename(__file__)
    el_tracker.sendCommand("add_file_preamble_text '%s'" % preamble_text)

def setup_tracker_options(el_tracker):
    """Sets up tracking, recording, and calibration options."""
    el_tracker.setOfflineMode()
    pix_msg = "screen_pixel_coords 0 0 %d %d" % (SCN_WIDTH - 1, SCN_HEIGHT - 1)
    el_tracker.sendCommand(pix_msg)
    el_tracker.sendCommand("calibration_type = HV9")
    el_tracker.sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT")
    el_tracker.sendCommand("file_sample_data = GAZE,GAZERES,HREF,AREA,STATUS,INPUT")

def calibrate_tracker(el_tracker):
    """Performs the initial calibration of the tracker."""
    el_tracker.doTrackerSetup()

def main():
    # Step 1: Initialize the EyeLink tracker
    el_tracker = initialize_tracker()

    # Change to the script directory
    script_path = os.path.dirname(sys.argv[0])
    if script_path:
        os.chdir(script_path)

    # Step 2: Initialize display-side graphics
    setup_display(el_tracker)

    # Step 3: Initialize data file
    setup_data_file(el_tracker)

    # Step 4: Set up tracker options
    setup_tracker_options(el_tracker)

    # Step 5: Perform initial calibration
    calibrate_tracker(el_tracker)

    # Cleanup
    if el_tracker is not None:
        el_tracker.close()

    subprocess.call(["python", "./adding_eyeTracker_data.py", el_tracker])

if __name__ == "__main__":
    main()
