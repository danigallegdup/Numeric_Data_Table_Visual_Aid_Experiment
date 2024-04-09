#
# Copyright (c) 1996-2021, SR Research Ltd., All Rights Reserved
#
# For use by SR Research licencees only. Redistribution and use in source
# and binary forms, with or without modification, are NOT permitted.
#
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in
# the documentation and/or other materials provided with the distribution.
#
# Neither name of SR Research Ltd nor the name of contributors may be used
# to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS ``AS
# IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# DESCRIPTION:
# This script shows how to connect, setup, control and use an EyeLink
# eye tracker to record and most importantly, to retrieve eye EVENTS
# (fixations, saccades, etc.).
#
# In order to eliminate dependency on third party display software like
# Pygame, this example does not present any visual stimuli during trials.
# The script will first show a gray screen, you press ENTER to transfer
# the camera image from the Host PC, and Press C & V to calibrate and
# validate; then, press O to start the experimental trials.
#
# The experiment is made up of three trials. A trial starts with a drift
# check screen (with a fixation dot at the center), followed by a
# 5-second blank screen. During this time, the Host PC screen shows
# fixation update events (cross), fixation end events (number)
# and saccade start and end events (line).
#
# This Pylink code demonstrates the following steps:
# 1-initializing connection to the tracker
# 2-initializing display-side graphics
# 3-initializing data file
# 4-setting up tracking, recording and calibration options
# 5-initial tracker calibration
# 6-Loop over all trials (run_trials)
#
# 6.1-verify connection to tracker and perform a drift-check, i.e.,
#     checking if recalibration is needed (do_trial)
# 6.2-start actual recording of samples and events to the data file
#     and make both available over the link (do_trial)
# 6.3-enter real-time mode and mark trial start time (do_trial)
# 6.4-stub to insert code that loads the initial visual stimulus (do_trial)
# 6.5-mark the time initial visual stimulus came on (do_trial)
# 6.6-wait and make sure we get the start signal for link samples
#     then mark which eye is being tracked (do_trial)
# 6.7-flush outstanding input from response box (do_trial)
# 6.8-open a plain text file to save data; then, poll for newest sample
#     over the link while verifying that tracker
#     is still recording, and termination or setup have not been requested
#     and that the trial time has not exceeded the trial duration (do_trial)
#     save the sample data into a plain text file
# 6.9-end real-time mode, stop recording and clear key presses (end_trial)
# 6.10-record various event counts and mock trial result to EDF file (do_trial)
#
# 7-close and transfer data file from host to display pc
# 8-close EyeLink connection and quit display-side graphics
#
# Last updated: 3/17/2021

from __future__ import division
from __future__ import print_function

import time
import sys
import os
import pylink


# so resource stimuli like images and sounds can be located with relative paths
script_path = os.path.dirname(sys.argv[0])
if len(script_path) != 0:
    os.chdir(script_path)

# some global constants
RIGHT_EYE = 1
LEFT_EYE = 0
BINOCULAR = 2

N_TRIALS = 3
TRIAL_DUR = 5000


# show some task instructions
inst = "Press ENTER to show the camera image, C to calibrate, V to \n" + \
        "validate the tracker, Press O to start recording.\n" +\
        "\nAt the beginning of a trial, a dot will show up on the \n" + \
        "screen; look at it and press the SPACEBAR to move on. Then, \n" + \
        "a blank screen will be presented for 5 seconds. \n" +\
        "Just look around, gaze position will be marked on the Host PC."

print("\nThe script will first show a blank screen.\n" + inst)
if sys.version_info > (3,0):
    ok = input("\nPress 'Y' to continue, 'N' to quit: ")
else: 
    ok = raw_input("\nPress 'Y' to continue, 'N' to quit: ")
if ok not in ['Y', 'y']:
    sys.exit()

# set this variable to True to run the script in "Dummy Mode"
dummy_mode = False

# we set the video mode to current video mode then get the update the value.
SCN_WIDTH = 0
SCN_HEIGHT = 0

# create three trial conditions and store their parameters in list
trial_condition = ['condition1', 'condition2', 'condition3']

# set up a folder to store the data files
results_folder = 'results'
if not os.path.exists(results_folder):
    os.makedirs(results_folder)


def end_trial():
    """Ends recording

    We add 100 msec of data to catch final events"""

    # get the currently active tracker object (connection)
    el_active = pylink.getEYELINK()

    pylink.endRealTimeMode()
    pylink.pumpDelay(100)
    el_active.stopRecording()

    while el_active.getkey():
        pass


def do_trial(trial):
    """ Run a single trial """

    # initialize sample data and button input variables
    new_smp = None
    smp = None

    # open a plain text file to save the sample data
    txt_file = os.path.join('results', 'samples_trial_%d.txt' % (trial + 1))
    sample_txt = open(txt_file, 'w')

    # get the currently active tracker object (connection)
    el_active = pylink.getEYELINK()

    # show some info about the current trial on the Host PC screen
    pars_to_show = (trial_condition[trial], trial + 1, N_TRIALS)
    status_message = 'Link event example, %s, Trial %d/%d' % pars_to_show
    el_tracker.sendCommand("record_status_message '%s'" % status_message)

    # log a TRIALID message to mark trial start, before starting to record.
    # EyeLink Data Viewer defines the start of a trial by the TRIALID message.
    el_tracker.sendMessage("TRIALID %d" % trial)

    # clear tracker display to black
    el_tracker.sendCommand("clear_screen 0")

    # perform a drift-check(/correction) at the start of each trial
    while True:
        # check whether we are still connected to the tracker
        if not el_tracker.isConnected():
            return pylink.ABORT_EXPT

        # drift-check; re-do camera setup, if needed
        try:
            error = el_tracker.doDriftCorrect(int(SCN_WIDTH/2.0),
                                              int(SCN_HEIGHT/2.0), 1, 1)
            # if the "ESC" key is pressed, get back to Camera Setup
            if error != pylink.ESC_KEY:
                break
            else:
                el_tracker.doTrackerSetup()
        except:
            pass

    # switch tracker to idle mode
    el_tracker.setOfflineMode()

    # start recording samples and events; save them to the EDF file and
    # make them available over the link
    error = el_tracker.startRecording(1, 1, 1, 1)
    if error:
        return error

    # begin the real-time mode
    pylink.beginRealTimeMode(100)

    # INSERT CODE TO DRAW INITIAL DISPLAY HERE

    # log a message to mark the time at which the initial display came on
    el_tracker.sendMessage("SYNCTIME")

    # wait for link data to arrive
    try:
        el_tracker.waitForBlockStart(100, 1, 1)
    except RuntimeError:
        # wait time expired without link data
        if pylink.getLastError()[0] == 0:
            end_trial()
            print("ERROR: No link data received!")
            return pylink.TRIAL_ERROR
        # for any other status simply re-raise the exception
        else:
            raise

    # determine which eye(s) is/are available
    eye_used = el_tracker.eyeAvailable()
    if eye_used == RIGHT_EYE:
        el_tracker.sendMessage("EYE_USED 1 RIGHT")
    elif eye_used == LEFT_EYE or eye_used == BINOCULAR:
        el_tracker.sendMessage("EYE_USED 0 LEFT")
        eye_used = LEFT_EYE
    else:
        print("Error in getting the eye information!")
        return pylink.TRIAL_ERROR

    # reset keys and buttons on tracker
    el_tracker.flushKeybuttons(0)

    # get trial start time
    start_time = pylink.currentTime()
    # poll link events and samples
    while True:
        # first check if recording is aborted
        # (returns 0 if no error, otherwise return codes, e.g.,
        # REPEAT_TRIAL, SKIP_TRIAL, ABORT_EXPT, TRIAL_ERROR )
        error = el_tracker.isRecording()
        if error != pylink.TRIAL_OK:
            end_trial()
            return error

        # check if trial duration exceeded
        if pylink.currentTime() > (start_time + TRIAL_DUR):
            el_tracker.sendMessage("TIMEOUT")
            end_trial()
            break

        # program termination or ALT-F4 or CTRL-C keys
        if el_tracker.breakPressed():
            end_trial()
            return pylink.ABORT_EXPT

        # check for local ESC key to abort trial (useful in debugging)
        elif el_tracker.escapePressed():
            end_trial()
            return pylink.SKIP_TRIAL

        # do we have a sample in the sample buffer?
        # and does it differ from the one we've seen before?
        new_smp = el_tracker.getNewestSample()
        if new_smp is not None:
            if(smp is None or new_smp.getTime() != smp.getTime()):
                # it is a new sample, mark it for future comparisons
                smp = new_smp
                # Check if the new sample has data for the eye
                # currently being tracked,
                if eye_used == RIGHT_EYE and smp.isRightSample():
                    gaze = smp.getRightEye().getGaze()
                    pupil = smp.getRightEye().getPupilSize()
                elif eye_used != RIGHT_EYE and smp.isLeftSample():
                    gaze = smp.getLeftEye().getGaze()
                    pupil = smp.getLeftEye().getPupilSize()

                # INSERT OWN CODE (EX: GAZE-CONTINGENT GRAPHICS)

                # save the sample time stamp and gaze position in the TXT file
                # IMPORTANT: Sample data is saved in EDF data files on the Host
                # PC users do not need to (and we do not recommend) recording
                # sample data this way. We write samples to the TXT file here
                # only for illustration purposes.
                print(gaze, pupil)
                smp_to_save = (smp.getTime(), gaze[0], gaze[1])
                sample_txt.write('%.1f\t%.2f\t%.2f\n' % smp_to_save)

    # close the TXT file
    sample_txt.close()

    # record the trial variable in a message recognized by Data Viewer
    el_active.sendMessage("!V TRIAL_VAR trial %d" % trial)

    # return exit record status
    ret_value = el_active.getRecordingStatus()

    # end real-time mode
    pylink.endRealTimeMode()

    return ret_value


def run_trials():
    """ This function is used to run individual trials and
        handles the trial return values

    Returns a successful trial with 0, aborting experiment with ABORT_EXPT (3);
    It also handles the case of re-running a trial.
    """

    # get the currently active tracker object (connection)
    el_tracker = pylink.getEYELINK()

    for trial in range(N_TRIALS):
        # first check if the connection to the tracker is still alive
        if(not el_tracker.isConnected() or el_tracker.breakPressed()):
            break

        while True:
            ret_value = do_trial(trial)

            if (ret_value == pylink.TRIAL_OK):
                el_tracker.sendMessage("TRIAL OK")
                break
            elif (ret_value == pylink.SKIP_TRIAL):
                el_tracker.sendMessage("TRIAL ABORTED")
                break
            elif (ret_value == pylink.ABORT_EXPT):
                el_tracker.sendMessage("EXPERIMENT ABORTED")
                return pylink.ABORT_EXPT
            elif (ret_value == pylink.REPEAT_TRIAL):
                el_tracker.sendMessage("TRIAL REPEATED")
            else:
                el_tracker.sendMessage("TRIAL ERROR")
                break
    return 0


# ------ The experiment starts from here -----------------------

# Step 1: initialize a tracker object with a Host IP address
# The Host IP address by default is "100.1.1.1"
# the "el_tracker" objected created here can be accessed through the Pylink
# function .getEYELINK(); this is useful when you need to refer to the tracker
# object when defining a function
#
# Set the Host PC address to "None" (without quotes) to run the script
# in "Dummy Mode" (note this script cannot run in dummy mode, as we need to
# extract eye movement date during recording
if dummy_mode:
    el_tracker = pylink.EyeLink(None)
    print('ERROR: This task requires real-time gaze data.\n' +
          'It cannot run in Dummy mode (with a simulated connection).')
    sys.exit()
else:
    try:
        el_tracker = pylink.EyeLink("100.1.1.1")
    except RuntimeError as error:
        print('ERROR:', error)
        sys.exit()

# Step 2: Initializes the graphics (for calibration & stimulus presentation)
# INSERT THIRD PARTY GRAPHICS (e.g., Pygame) INITIALIZATION HERE IF NEEDED
pylink.openGraphics((SCN_WIDTH, SCN_HEIGHT), 32)

#query the current display info. I we started with 0 for SCN_WIDTH and SCN_HEIGHT,
#we will have updated values. Otherwise, we should have same values. unless
#the setvideo mode call fails.
disp = pylink.getDisplayInformation()
SCN_WIDTH = disp.width
SCN_HEIGHT = disp.height


# Step 3: Open an EDF data file on the Host PC
edf_file_name = "TEST.EDF"
el_tracker.openDataFile(edf_file_name)

# add a preamble text (data file header)
preamble_text = 'RECORDED BY %s' % os.path.basename(__file__)
el_tracker.sendCommand("add_file_preamble_text '%s'" % preamble_text)

# Step 4: setting up tracking, recording and calibration options
# we first flush all key presses and put the tracker in the offline mode
pylink.flushGetkeyQueue()
el_tracker.setOfflineMode()

# The tracker needs to know the resolution of the screen the
# subject is viewing
pix_msg = "screen_pixel_coords 0 0 %d %d" % (SCN_WIDTH - 1, SCN_HEIGHT - 1)
el_tracker.sendCommand(pix_msg)
# The Data Viewer software also needs to know the screen
# resolution for correct visualization
dv_msg = "DISPLAY_COORDS  0 0 %d %d" % (SCN_WIDTH - 1, SCN_HEIGHT - 1)
el_tracker.sendMessage(dv_msg)

# Get the software version:  1-EyeLink I, 2-EyeLink II, 3/4-EyeLink 1000,
# 5-EyeLink 1000 Plus, 6-Portable DUO
eyelink_ver = 0  # set version to 0, in case running in Dummy mode
if not dummy_mode:
    vstr = el_tracker.getTrackerVersionString()
    eyelink_ver = int(vstr.split()[-1].split('.')[0])
    # print out some version info in the shell
    print('Running experiment on %s, version %d' % (vstr, eyelink_ver))

# Select what data to save in the EDF file, for a detailed discussion
# of the data flags, see the EyeLink User Manual, "Setting File Contents"
file_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT'
file_sample_flags = 'LEFT,RIGHT,GAZE,HREF,RAW,AREA,HTARGET,GAZERES,BUTTON,STATUS,INPUT'
if eyelink_ver < 4:
    file_sample_flags = 'LEFT,RIGHT,GAZE,HREF,RAW,AREA,GAZERES,BUTTON,STATUS,INPUT'
el_tracker.sendCommand("file_event_filter = %s" % file_event_flags)
el_tracker.sendCommand("file_sample_data = %s" % file_sample_flags)

# Select what data is available over the link (for online data accessing)
link_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,FIXUPDATE,INPUT'
link_sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,AREA,HTARGET,STATUS,INPUT'
if eyelink_ver < 4:
    link_sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,INPUT'
el_tracker.sendCommand("link_event_filter = %s" % link_event_flags)
el_tracker.sendCommand("link_sample_data = %s" % link_sample_flags)

# Set the calibration target and background color
pylink.setCalibrationColors((0, 0, 0), (128, 128, 128))

# select best size for calibration target
pylink.setTargetSize(int(SCN_WIDTH/70.0), int(SCN_WIDTH/300.))

# Set the calibraiton and drift correction sound
pylink.setCalibrationSounds("", "", "")
pylink.setDriftCorrectSounds("", "", "")

# Step 5: Do the tracker setup at the beginning of the experiment.
el_tracker.doTrackerSetup()

# Step 6: Run trials. make sure display-tracker connection is established
# and no program termination or ALT-F4 or CTRL-C pressed
if el_tracker.isConnected() and not el_tracker.breakPressed():
    run_trials()

# Step 7: File transfer and cleanup
if el_tracker is not None:
    el_tracker.setOfflineMode()
    pylink.msecDelay(500)

    # Close the edf data file on the Host
    el_tracker.closeDataFile()

    # transfer the edf file to the Display PC and rename it
    local_file_name = os.path.join(results_folder, edf_file_name)

    try:
        el_tracker.receiveDataFile(edf_file_name, local_file_name)
    except RuntimeError as error:
        print('ERROR:', error)

# Step 8: close EyeLink connection and quit display-side graphics
el_tracker.close()
# Close the experiment graphics
pylink.closeGraphics()
