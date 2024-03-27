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
# This example scripts shows how to record the target position in a
# smooth pursuit task. This scrip also shows how to record dynamic interest
# area and target position information to the EDF data file, so Data Viewer
# can recreate the interest area and playback the target movement.

# Last updated: 3/29/2021

from __future__ import division
from __future__ import print_function

import pylink
import os
import platform
import random
import time
import sys
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
from psychopy import visual, core, event, monitors, gui
from math import pi, sin
from string import ascii_letters, digits

# Switch to the script folder
script_path = os.path.dirname(sys.argv[0])
if len(script_path) != 0:
    os.chdir(script_path)

# Show only critical log message in the PsychoPy console
from psychopy import logging
logging.console.setLevel(logging.CRITICAL)

# Set this variable to True if you use the built-in retina screen as your
# primary display device on macOS. If have an external monitor, set this
# variable True if you choose to "Optimize for Built-in Retina Display"
# in the Displays preference settings.
use_retina = False

# Set this variable to True to run the script in "Dummy Mode"
dummy_mode = False

# Set this variable to True to run the task in full screen mode
# It is easier to debug the script in non-fullscreen mode
full_screen = True

# Store the parameters for Sinusoidal movement patterns in a list
# [movement_type, max_duration, amp_x, amp_y, phase_x, phase_y, freq_x, freq_y]
#
# y(t) = amplitude * sin(2 * pi * frequency * t + phase)
#
# a combination of these parameters will give you a movement in horizontal
# or vertical direction only, a circular movement, or a movement that follow
# a complex Lissajous curve. For a circular or elliptical movements, the phase
# in x and y directions should differ by pi/2 (direction of the difference matters)
#
# In the equation, frequency is cycles per second

trials = [
    ['Horizontal_L', 8.0, 350, 350, pi*3/2, 0, 1/8.0, 0],
    ['Horizontal_R', 8.0, 350, 350, pi/2, 0, 1/8.0, 0],
    ['Vertical_U', 8.0, 350, 350, 0, pi/2, 0, 1/8.0],
    ['Vertical_D', 8.0, 350, 350, 0, pi*3/2, 0, 1/8.0],
    ['Elliptic_L', 8.0, 350, 350, pi*3/2, 0, 1/8.0, 1/8.0],
    ['Elliptic_R', 8.0, 350, 350, pi/2, 0, 1/8.0, 1/8.0]
    ]

# Set up EDF data file name and local data folder
#
# The EDF data filename should not exceed 8 alphanumeric characters
# use ONLY number 0-9, letters, & _ (underscore) in the filename
edf_fname = 'TEST'

# Prompt user to specify an EDF data filename
# before we open a fullscreen window
dlg_title = 'Enter EDF File Name'
dlg_prompt = 'Please enter a file name with 8 or fewer characters\n' + \
             '[letters, numbers, and underscore].'

# loop until we get a valid filename
while True:
    dlg = gui.Dlg(dlg_title)
    dlg.addText(dlg_prompt)
    dlg.addField('File Name:', edf_fname)
    # show dialog and wait for OK or Cancel
    ok_data = dlg.show()
    if dlg.OK:  # if ok_data is not None
        print('EDF data filename: {}'.format(ok_data[0]))
    else:
        print('user cancelled')
        core.quit()
        sys.exit()

    # get the string entered by the experimenter
    tmp_str = dlg.data[0]
    # strip trailing characters, ignore the ".edf" extension
    edf_fname = tmp_str.rstrip().split('.')[0]

    # check if the filename is valid (length <= 8 & no special char)
    allowed_char = ascii_letters + digits + '_'
    if not all([c in allowed_char for c in edf_fname]):
        print('ERROR: Invalid EDF filename')
    elif len(edf_fname) > 8:
        print('ERROR: EDF filename should not exceed 8 characters')
    else:
        break

# Set up a folder to store the EDF data files and the associated resources
# e.g., files defining the interest areas used in each trial
results_folder = 'results'
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

# We download EDF data file from the EyeLink Host PC to the local hard
# drive at the end of each testing session, here we rename the EDF to
# include session start date/time
time_str = time.strftime("_%Y_%m_%d_%H_%M", time.localtime())
session_identifier = edf_fname + time_str

# create a folder for the current testing session in the "results" folder
session_folder = os.path.join(results_folder, session_identifier)
if not os.path.exists(session_folder):
    os.makedirs(session_folder)

# create a 'aoi' folder to save the VFRAME commands for each trial
aoi_folder = os.path.join(session_folder, 'aoi')
if not os.path.exists(aoi_folder):
    os.makedirs(aoi_folder)

# Step 1: Connect to the EyeLink Host PC
#
# The Host IP address, by default, is "100.1.1.1".
# the "el_tracker" objected created here can be accessed through the Pylink
# Set the Host PC address to "None" (without quotes) to run the script
# in "Dummy Mode"
if dummy_mode:
    el_tracker = pylink.EyeLink(None)
else:
    try:
        el_tracker = pylink.EyeLink("100.1.1.1")
    except RuntimeError as error:
        print('ERROR:', error)
        core.quit()
        sys.exit()

# Step 2: Open an EDF data file on the Host PC
edf_file = edf_fname + ".EDF"
try:
    el_tracker.openDataFile(edf_file)
except RuntimeError as err:
    print('ERROR:', err)
    # close the link if we have one open
    if el_tracker.isConnected():
        el_tracker.close()
    core.quit()
    sys.exit()

# Add a header text to the EDF file to identify the current experiment name
# This is OPTIONAL. If your text starts with "RECORDED BY " it will be
# available in DataViewer's Inspector window by clicking
# the EDF session node in the top panel and looking for the "Recorded By:"
# field in the bottom panel of the Inspector.
preamble_text = 'RECORDED BY %s' % os.path.basename(__file__)
el_tracker.sendCommand("add_file_preamble_text '%s'" % preamble_text)

# Step 3: Configure the tracker
#
# Put the tracker in offline mode before we change tracking parameters
el_tracker.setOfflineMode()

# Get the software version:  1-EyeLink I, 2-EyeLink II, 3/4-EyeLink 1000,
# 5-EyeLink 1000 Plus, 6-Portable DUO
eyelink_ver = 0  # set version to 0, in case running in Dummy mode
if not dummy_mode:
    vstr = el_tracker.getTrackerVersionString()
    eyelink_ver = int(vstr.split()[-1].split('.')[0])
    # print out some version info in the shell
    print('Running experiment on %s, version %d' % (vstr, eyelink_ver))

# File and Link data control
# what eye events to save in the EDF file, include everything by default
file_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT'
# what eye events to make available over the link, include everything by default
link_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,FIXUPDATE,INPUT'
# what sample data to save in the EDF data file and to make available
# over the link, include the 'HTARGET' flag to save head target sticker
# data for supported eye trackers
if eyelink_ver > 3:
    file_sample_flags = 'LEFT,RIGHT,GAZE,HREF,RAW,AREA,HTARGET,GAZERES,BUTTON,STATUS,INPUT'
    link_sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,AREA,HTARGET,STATUS,INPUT'
else:
    file_sample_flags = 'LEFT,RIGHT,GAZE,HREF,RAW,AREA,GAZERES,BUTTON,STATUS,INPUT'
    link_sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,INPUT'
el_tracker.sendCommand("file_event_filter = %s" % file_event_flags)
el_tracker.sendCommand("file_sample_data = %s" % file_sample_flags)
el_tracker.sendCommand("link_event_filter = %s" % link_event_flags)
el_tracker.sendCommand("link_sample_data = %s" % link_sample_flags)

# Optional tracking parameters
# Sample rate, 250, 500, 1000, or 2000, check your tracker specification
# if eyelink_ver > 2:
#     el_tracker.sendCommand("sample_rate 1000")
# Choose a calibration type, H3, HV3, HV5, HV13 (HV = horizontal/vertical),
el_tracker.sendCommand("calibration_type = HV9")
# Set a gamepad button to accept calibration/drift check target
# You need a supported gamepad/button box that is connected to the Host PC
el_tracker.sendCommand("button_function 5 'accept_target_fixation'")

# Step 4: set up a graphics environment for calibration
#
# Open a window, be sure to specify monitor parameters
mon = monitors.Monitor('myMonitor', width=53.0, distance=70.0)
win = visual.Window(fullscr=full_screen,
                    monitor=mon,
                    winType='pyglet',
                    units='pix')

# get the native screen resolution used by PsychoPy
scn_width, scn_height = win.size
# resolution fix for Mac retina displays
if 'Darwin' in platform.system():
    if use_retina:
        scn_width = int(scn_width/2.0)
        scn_height = int(scn_height/2.0)

# Pass the display pixel coordinates (left, top, right, bottom) to the tracker
# see the EyeLink Installation Guide, "Customizing Screen Settings"
el_coords = "screen_pixel_coords = 0 0 %d %d" % (scn_width - 1, scn_height - 1)
el_tracker.sendCommand(el_coords)

# Write a DISPLAY_COORDS message to the EDF file
# Data Viewer needs this piece of info for proper visualization, see Data
# Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
dv_coords = "DISPLAY_COORDS  0 0 %d %d" % (scn_width - 1, scn_height - 1)
el_tracker.sendMessage(dv_coords)

# Configure a graphics environment (genv) for tracker calibration
genv = EyeLinkCoreGraphicsPsychoPy(el_tracker, win)
print(genv)  # print out the version number of the CoreGraphics library

# Set background and foreground colors for the calibration target
# in PsychoPy, (-1, -1, -1)=black, (1, 1, 1)=white, (0, 0, 0)=mid-gray
foreground_color = (-1, -1, -1)
background_color = win.color
genv.setCalibrationColors(foreground_color, background_color)

# Set up the calibration target
#
# The target could be a "circle" (default), a "picture", a "movie" clip,
# or a rotating "spiral". To configure the type of calibration target, set
# genv.setTargetType to "circle", "picture", "movie", or "spiral", e.g.,
# genv.setTargetType('picture')
#
# Use gen.setPictureTarget() to set a "picture" target
# genv.setPictureTarget(os.path.join('images', 'fixTarget.bmp'))
#
# Use genv.setMovieTarget() to set a "movie" target
# genv.setMovieTarget(os.path.join('videos', 'calibVid.mov'))

# Use the default calibration target ('circle')
genv.setTargetType('circle')

# Configure the size of the calibration target (in pixels)
# this option applies only to "circle" and "spiral" targets
genv.setTargetSize(24)

# Beeps to play during calibration, validation and drift correction
# parameters: target, good, error
#     target -- sound to play when target moves
#     good -- sound to play on successful operation
#     error -- sound to play on failure or interruption
# Each parameter could be ''--default sound, 'off'--no sound, or a wav file
genv.setCalibrationSounds('', '', '')

# resolution fix for macOS retina display issues
if use_retina:
    genv.fixMacRetinaDisplay()

# Request Pylink to use the PsychoPy window we opened above for calibration
pylink.openGraphicsEx(genv)


# define a few helper functions for trial handling


def clear_screen(win):
    """ clear up the PsychoPy window"""

    win.fillColor = genv.getBackgroundColor()
    win.flip()


def show_msg(win, text, wait_for_keypress=True):
    """ Show task instructions on screen"""

    msg = visual.TextStim(win, text,
                          color=genv.getForegroundColor(),
                          wrapWidth=scn_width/2)
    clear_screen(win)
    msg.draw()
    win.flip()

    # wait indefinitely, terminates upon any key press
    if wait_for_keypress:
        event.waitKeys()
        clear_screen(win)


def terminate_task():
    """ Terminate the task gracefully and retrieve the EDF data file

    file_to_retrieve: The EDF on the Host that we would like to download
    win: the current window used by the experimental script
    """

    el_tracker = pylink.getEYELINK()

    if el_tracker.isConnected():
        # Terminate the current trial first if the task terminated prematurely
        error = el_tracker.isRecording()
        if error == pylink.TRIAL_OK:
            abort_trial()

        # Put tracker in Offline mode
        el_tracker.setOfflineMode()

        # Clear the Host PC screen and wait for 500 ms
        el_tracker.sendCommand('clear_screen 0')
        pylink.msecDelay(500)

        # Close the edf data file on the Host
        el_tracker.closeDataFile()

        # Show a file transfer message on the screen
        msg = 'EDF data is transferring from EyeLink Host PC...'
        show_msg(win, msg, wait_for_keypress=False)

        # Download the EDF data file from the Host PC to a local data folder
        # parameters: source_file_on_the_host, destination_file_on_local_drive
        local_edf = os.path.join(session_folder, session_identifier + '.EDF')
        try:
            el_tracker.receiveDataFile(edf_file, local_edf)
        except RuntimeError as error:
            print('ERROR:', error)

        # Close the link to the tracker.
        el_tracker.close()

    # close the PsychoPy window
    win.close()

    # quit PsychoPy
    core.quit()
    sys.exit()


def abort_trial():
    """Ends recording """

    el_tracker = pylink.getEYELINK()

    # Stop recording
    if el_tracker.isRecording():
        # add 100 ms to catch final trial events
        pylink.pumpDelay(100)
        el_tracker.stopRecording()

    # clear the screen
    clear_screen(win)
    # Send a message to clear the Data Viewer screen
    bgcolor_RGB = (116, 116, 116)
    el_tracker.sendMessage('!V CLEAR %d %d %d' % bgcolor_RGB)

    # send a message to mark trial end
    el_tracker.sendMessage('TRIAL_RESULT %d' % pylink.TRIAL_ERROR)

    return pylink.TRIAL_ERROR


def run_trial(trial_pars, trial_index):
    """ Helper function specifying the events that will occur in a single trial

    trial_pars - a list containing trial parameters, i.e.,
           [movement, max_duration, amp_x, amp_y, phase_x, phase_y,
           freq_x, freq_y]
    trial_index - record the order of trial presentation in the task
    """

    # parse the movement pattern parameters
    movement, dur, amp_x, amp_y, phase_x, phase_y, freq_x, freq_y = trial_pars

    # prepare the pursuit target and the clock
    target = visual.GratingStim(win, tex=None, mask='circle', size=25)
    target.color = (1, -1, -1)

    # get a reference to the currently active EyeLink connection
    el_tracker = pylink.getEYELINK()

    # put the tracker in the offline mode first
    el_tracker.setOfflineMode()

    # send a "TRIALID" message to mark the start of a trial, see Data
    # Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
    el_tracker.sendMessage('TRIALID %d' % trial_index)

    # record_status_message : show some info on the Host PC
    # here we show how many trial has been tested
    status_msg = 'TRIAL number %d, %s' % (trial_index, movement)
    el_tracker.sendCommand("record_status_message '%s'" % status_msg)

    # draw a reference grid on the Host PC screen
    # For details, See section 25.7 'Drawing Commands' in the
    # EyeLink Programmers Guide manual
    line_hor = (scn_width/2.0 - amp_x, scn_height/2.0,
                scn_width/2.0 + amp_x, scn_height/2.0)
    line_ver = (scn_width/2.0, scn_height/2.0 - amp_y,
                scn_width/2.0, scn_height/2.0 + amp_x)
    el_tracker.sendCommand('clear_screen 0')  # clear the host Display
    el_tracker.sendCommand('draw_line %d %d %d %d 15' % line_hor)
    el_tracker.sendCommand('draw_line %d %d %d %d 15' % line_ver)

    # drift check
    # we recommend drift-check at the beginning of each trial
    # the doDriftCorrect() function requires target position in integers
    # the last two arguments:
    # draw_target (1-default, 0-draw the target then call doDriftCorrect)
    # allow_setup (1-press ESCAPE to recalibrate, 0-not allowed)
    #
    # Skip drift-check if running the script in Dummy Mode

    dc_x = amp_x*sin(phase_x) + scn_width/2.0
    dc_y = scn_height/2.0 - amp_y*sin(phase_y)

    while not dummy_mode:
        # terminate the task if no longer connected to the tracker or
        # user pressed Ctrl-C to terminate the task
        if (not el_tracker.isConnected()) or el_tracker.breakPressed():
            terminate_task()
            return pylink.ABORT_EXPT

        # draw a custom drift-correction target; here the "draw_target"
        # parameter is set to 0, i.e., user draw the target instead
        target.pos = (amp_x * sin(phase_x), amp_y * sin(phase_y))
        target.draw()
        win.flip()
        # drift-check and re-do camera setup if ESCAPE is pressed
        try:
            error = el_tracker.doDriftCorrect(int(dc_x), int(dc_y), 0, 1)
            # break following a success drift-check
            if error is not pylink.ESC_KEY:
                break
        except:
            pass

    # put tracker in idle/offline mode before recording
    el_tracker.setOfflineMode()

    # Start recording
    # arguments: sample_to_file, events_to_file, sample_over_link,
    # event_over_link (1-yes, 0-no)
    try:
        el_tracker.startRecording(1, 1, 1, 1)
    except RuntimeError as error:
        print("ERROR:", error)
        abort_trial()
        return pylink.TRIAL_ERROR

    # Allocate some time for the tracker to cache some samples
    pylink.pumpDelay(100)

    # Send a message to clear the Data Viewer screen, get it ready for
    # drawing the pictures during visualization
    bgcolor_RGB = (116, 116, 116)
    el_tracker.sendMessage('!V CLEAR %d %d %d' % bgcolor_RGB)

    # open a INTEREST AREA SET file to make a dynamic IA for the target
    ias = 'IA_%d.ias' % trial_index
    ias_file = open(os.path.join(aoi_folder, ias), 'w')

    # initial target position
    time_elapsed = 0
    tar_x = amp_x*sin(2 * pi * freq_x * time_elapsed + phase_x)
    tar_y = amp_y*sin(2 * pi * freq_y * time_elapsed + phase_y)

    ia_radius = 60  # radius of the elliptical IA
    frame_num = 0  # keep track of the frames displayed

    while True:
        # abort the current trial if the tracker is no longer recording
        error = el_tracker.isRecording()
        if error is not pylink.TRIAL_OK:
            el_tracker.sendMessage('tracker_disconnected')
            abort_trial()
            return error

        # check keyboard events
        for keycode, modifier in event.getKeys(modifiers=True):
            # Abort a trial if "ESCAPE" is pressed
            if keycode == 'escape':
                el_tracker.sendMessage('trial_skipped_by_user')
                # clear the screen
                clear_screen(win)
                # abort trial
                abort_trial()
                return pylink.SKIP_TRIAL

            # Terminate the task if Ctrl-c
            if keycode == 'c' and (modifier['ctrl'] is True):
                el_tracker.sendMessage('terminated_by_user')
                terminate_task()
                return pylink.ABORT_EXPT

        # draw the target
        target.pos = (tar_x, tar_y)
        target.draw()
        win.flip()
        frame_num += 1
        flip_time = core.getTime()

        if frame_num == 1:
            # send a message to mark movement onset
            el_tracker.sendMessage('TARGET_ONSET')

            # record a message to let Data Viewer know where to find
            # the dynamic IA file for the current trial.
            ias_path = os.path.join('aoi', ias)
            el_tracker.sendMessage('!V IAREA FILE %s' % ias_path)

            # pursuit start time
            movement_start = flip_time
        else:
            # save the Interest Area info following movement onset
            ia_pars = (-1 * round((pre_frame_time - movement_start) * 1000),
                       -1 * round((flip_time - movement_start) * 1000) + 1,
                       int(scn_width/2.0 + pre_x - ia_radius),
                       int(scn_height/2.0 - pre_y - ia_radius),
                       int(scn_width/2.0 + pre_x + ia_radius),
                       int(scn_height/2.0 - pre_y + ia_radius))

            ia_msg = '%d %d ELLIPSE 1 %d %d %d %d TARGET\n' % ia_pars
            ias_file.write(ia_msg)

            # log the target position after each screen refresh
            tar_pos = (tar_x + int(scn_width/2), int(scn_height/2) - tar_y)
            tar_pos_msg = '!V TARGET_POS target %d, %d 1 0' % tar_pos
            el_tracker.sendMessage(tar_pos_msg)

            # OPTIONAL - send over another message to request Data Viewer
            # to draw the pursuit target when visualizing the data
            el_tracker.sendMessage('!V CLEAR 128 128 128')
            tar_msg = '!V FIXPOINT 255 0 0 255 0 0 %d %d 50 50' % tar_pos
            el_tracker.sendMessage(tar_msg)

        # keep track of target position and frame timing
        pre_frame_time = flip_time
        pre_x = tar_x
        pre_y = tar_y

        # update target position and draw the target
        time_elapsed = flip_time - movement_start
        tar_x = amp_x*sin(2 * pi * freq_x * time_elapsed + phase_x)
        tar_y = amp_y*sin(2 * pi * freq_y * time_elapsed + phase_y)

        # check for time out
        if time_elapsed >= dur:
            # send over a message to log movement offset
            el_tracker.sendMessage('TARGET_OFFSET')
            break

    # clear the screen
    clear_screen(win)
    el_tracker.sendMessage('blank_screen')
    # send a message to clear the Data Viewer screen as well
    el_tracker.sendMessage('!V CLEAR 128 128 128')

    # close the IAS file that contain the dynamic IA definition
    ias_file.close()

    # stop recording; add 100 msec to catch final events before stopping
    pylink.pumpDelay(100)
    el_tracker.stopRecording()

    # record trial variables to the EDF data file, for details, see Data
    # Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
    movement, dur, amp_x, amp_y, phase_x, phase_y, freq_x, freq_y
    el_tracker.sendMessage('!V TRIAL_VAR movement %s' % movement)
    el_tracker.sendMessage('!V TRIAL_VAR max_duration %d' % int(dur*1000))
    el_tracker.sendMessage('!V TRIAL_VAR amp_x %.02f' % amp_x)
    pylink.msecDelay(4)  # take a break of 4 millisecond
    el_tracker.sendMessage('!V TRIAL_VAR amp_y %.02f' % amp_y)
    el_tracker.sendMessage('!V TRIAL_VAR phase_x %.02f' % (phase_x/pi*180))
    el_tracker.sendMessage('!V TRIAL_VAR phase_y %.02f' % (phase_y/pi*180))
    pylink.msecDelay(4)  # take a break of 4 millisecond
    el_tracker.sendMessage('!V TRIAL_VAR freq_x %.02f' % freq_x)
    el_tracker.sendMessage('!V TRIAL_VAR freq_y %.02f' % freq_y)

    # send a 'TRIAL_RESULT' message to mark the end of trial, see Data
    # Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
    el_tracker.sendMessage('TRIAL_RESULT %d' % pylink.TRIAL_OK)


# Step 5: Set up the camera and calibrate the tracker
#
# Show the task instructions
task_msg = 'In the task, please follow the RED dot with your gaze\n' + \
    'You may press the SPACEBAR to end a trial\n' + \
    'or press Ctrl-C to if you need to quit the task early\n'
if dummy_mode:
    task_msg = task_msg + '\nNow, Press ENTER to start the task'
else:
    task_msg = task_msg + '\nNow, Press ENTER twice to calibrate tracker'
show_msg(win, task_msg)

# skip this step if running the script in Dummy Mode
if not dummy_mode:
    try:
        el_tracker.doTrackerSetup()
    except RuntimeError as err:
        print('ERROR:', err)
        el_tracker.exitCalibration()

# construct a list of 4 trials
test_list = trials[:]*1

# randomize the trial list
random.shuffle(test_list)

trial_index = 1
for trial_pars in test_list:
    run_trial(trial_pars, trial_index)
    trial_index += 1

# Step 7: disconnect, download the EDF file, then terminate the task
terminate_task()
