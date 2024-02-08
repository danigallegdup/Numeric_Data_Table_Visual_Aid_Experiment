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
# This is a basic example for long recordings, e.g., in an MRI setup.
# With a long recording, we start and stop recording at the beginning and
# end of a testing session (run), rather than at the beginning and end of
# each experimental trial. We still send the TRIALID and TRIAL_RESULT
# messages to the tracker, and Data Viewer will still be able to segment the
# long recording into small segments (trials)
#
# In this simple illustration, the duration of each trial is 6 secs, we show
# a picture for 4-sec, then show a fixation cross for 2-sec. This fixation
# cross can be use as a reference point for online drift-correction
#
# In this task, stimulus timing is controlled by screen refreshes. For
# simplicity, we will not discard the first TR and implement timing protocols
# for improving statistical power
#
# Last updated: 5/21/2021


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
from PIL import Image
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

# Store the parameters of all trials in a list, [condition, image]
trials = [
    ['cond_1', 'img_1.jpg'],
    ['cond_2', 'img_2.jpg'],
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

# Optional -- Shrink the spread of the calibration/validation targets
# if the default outermost targets are not all visible in the bore.
# The default <x, y display proportion> is 0.88, 0.83 (88% of the display
# horizontally and 83% vertically)
el_tracker.sendCommand('calibration_area_proportion 0.88 0.83')
el_tracker.sendCommand('validation_area_proportion 0.88 0.83')

# Optional: online drift correction.
# See the EyeLink 1000 / EyeLink 1000 Plus User Manual
#
# Online drift correction to mouse-click position:
# el_tracker.sendCommand('driftcorrect_cr_disable = OFF')
# el_tracker.sendCommand('normal_click_dcorr = ON')

# Online drift correction to a fixed location, e.g., screen center
# el_tracker.sendCommand('driftcorrect_cr_disable = OFF')
# el_tracker.sendCommand('online_dcorr_refposn %d,%d' % (int(scn_width/2.0),
#                                                        int(scn_height/2.0)))
# el_tracker.sendCommand('online_dcorr_button = ON')
# el_tracker.sendCommand('normal_click_dcorr = OFF')

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

# Use a picture as the calibration target
genv.setTargetType('picture')
genv.setPictureTarget(os.path.join('images', 'fixTarget.bmp'))

# Configure the size of the calibration target (in pixels)
# this option applies only to "circle" and "spiral" targets
# genv.setTargetSize(24)

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


def run_trial(trial_pars, trial_index, block_num, block_len, scan_clock):
    """ Helper function specifying the events that will occur in a single trial

    trial_pars - a list containing trial parameters, e.g.,
                ['cond_1', 'img_1.jpg']
    trial_index - record the order of trial presentation in the task
    block_num - block number
    block_len - length of a block
    scan_clock - a global clock to track stimulus timing
    """

    # stimulus timing
    trial_duration = 6.0
    image_duration = 4.0
    tmp_trial_index = trial_index - (block_num - 1) * block_len
    image_onset_time = (tmp_trial_index - 1) * trial_duration
    fix_onset_time = image_onset_time + image_duration

    # unpacking the trial parameters
    cond, pic = trial_pars

    # get a reference to the currently active EyeLink connection
    el_tracker = pylink.getEYELINK()

    # send a "TRIALID" message to mark the start of a trial, see Data
    # Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
    # Skip this message for the first trial
    if tmp_trial_index > 1:
        el_tracker.sendMessage('TRIALID %d' % trial_index)

    # For illustration purpose,
    # send interest area messages to record in the EDF data file
    # here we draw a rectangular IA, for illustration purposes
    # format: !V IAREA RECTANGLE <id> <left> <top> <right> <bottom> [label]
    # for all supported interest area commands, see the Data Viewer Manual,
    # "Protocol for EyeLink Data to Viewer Integration"
    left = int(scn_width/2.0) - 50
    top = int(scn_height/2.0) - 50
    right = int(scn_width/2.0) + 50
    bottom = int(scn_height/2.0) + 50
    ia_pars = (1, left, top, right, bottom, 'screen_center')
    el_tracker.sendMessage('!V IAREA RECTANGLE %d %d %d %d %d %s' % ia_pars)

    image_on = False
    fix_on = False
    while True:
        # draw the image
        if not image_on and (scan_clock.getTime() >= image_onset_time):
            win.fillColor = win.color
            img[pic].draw()
            win.flip()
            # send over a message to mark the onset of the image
            el_tracker.sendMessage('image_onset')

            # send over a message to specify where the image is stored
            # relative to the EDF data file, see Data Viewer User Manual,
            # "Protocol for EyeLink Data to Viewer Integration"
            el_tracker.sendMessage('!V CLEAR 128 128 128')
            bg_image = '../../images/' + pic
            imgload_pars = (bg_image, int(scn_width/2.0), int(scn_height/2.0),
                            int(scn_width), int(scn_height))
            imgload_msg = '!V IMGLOAD CENTER %s %d %d %d %d' % imgload_pars
            el_tracker.sendMessage(imgload_msg)

            image_on = True

        # draw the fixation cross
        if not fix_on and (scan_clock.getTime() >= fix_onset_time):
            win.fillColor = win.color
            fix.draw()
            win.flip()
            el_tracker.sendMessage('fixation_onset')

            # record a message to request Data Viewer to draw a cross when
            # visualizing the data; see Data Viewer User Manual, "Protocol
            # for EyeLink Data to Viewer Integration"
            h_center = int(scn_width/2.0)
            v_center = int(scn_height/2.0)
            hor = (h_center - 20, v_center, h_center + 20, v_center)
            ver = (h_center, v_center - 20, h_center, v_center + 20)
            el_tracker.sendMessage('!V CLEAR 128 128 128')
            el_tracker.sendMessage('!V DRAWLINE 0 0 0 %d %d %d %d' % hor)
            el_tracker.sendMessage('!V DRAWLINE 0 0 0 %d %d %d %d' % ver)

            fix_on = True

        # end trial after 6-sec
        if scan_clock.getTime() >= (image_onset_time + trial_duration):
            el_tracker.sendMessage('time_out')
            break

        # check for keyboard events
        for keycode, modifier in event.getKeys(modifiers=True):
            # Terminate the task if Ctrl-c
            if keycode == 'c' and (modifier['ctrl'] is True):
                el_tracker.sendMessage('terminated_by_user')
                terminate_task()

    # record trial variables in the EDF data file, see Data Viewer User
    # Manual, "Protocol for EyeLink Data to Viewer Integration"
    el_tracker.sendMessage('!V TRIAL_VAR cond %s' % cond)
    el_tracker.sendMessage('!V TRIAL_VAR image %s' % pic)

    # send a 'TRIAL_RESULT' message to mark the end of trial, see Data
    # Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
    el_tracker.sendMessage('TRIAL_RESULT %d' % pylink.TRIAL_OK)

# Real experiment starts from here
#
# Show the task instructions
if not dummy_mode:
    task_msg = 'Press ENTER to calibrate tracker'
    show_msg(win, task_msg)

# Set up the camera and calibrate the tracker, if not running in dummy mode
if not dummy_mode:
    try:
        el_tracker.doTrackerSetup()
    except RuntimeError as err:
        print('ERROR:', err)
        el_tracker.exitCalibration()

# Run two blocks of trials and perform a drift-check in-between
for block in range(1, 3):
    # construct a list of trials to test_list
    test_list = trials[:]*2
    block_len = len(test_list)
    # keep track of the number of trials completed
    trial_index = (block - 1) * block_len + 1

    # send a "TRIALID" message to mark the start of the first trial, so
    # the number of trials will be properly parsed by Data Viewer
    el_tracker.sendMessage('TRIALID %d' % trial_index)

    # OPTIONAL--record_status_message : show some info on the Host PC
    # for illustration purposes, here we show an "example_MSG"
    el_tracker.sendCommand("record_status_message 'Block %d'" % block)

    # For illustration purpose, we draw a rectangle on the Host screen
    # For a list of supported draw commands, see the "COMMANDS.INI" file on the
    # Host PC (under /elcl/exe)
    # Host PC (under /elcl/exe)
    left = int(scn_width/2.0) - 60
    top = int(scn_height/2.0) - 60
    right = int(scn_width/2.0) + 60
    bottom = int(scn_height/2.0) + 60
    draw_cmd = 'draw_filled_box %d %d %d %d 1' % (left, top, right, bottom)
    el_tracker.sendCommand(draw_cmd)

    # prepare the stimuli
    # fixation cross
    fix = visual.TextStim(win, text='+', height=64, color=foreground_color)
    # load all image and store it in a dictionary
    img = {}
    for trial in trials:
        cond, pic = trial
        img[pic] = visual.ImageStim(win, image=os.path.join('images', pic))

    # set up a global timer
    scan_clock = core.Clock()

    # we recommend drift-check at the beginning of each trial, in an MRI
    # setup, however, this is not possible and one can do online drift-
    # correction if needed
    # the doDriftCorrect() function requires target position in integers
    # the last two arguments:
    # draw_target (1-default, 0-draw the target then call doDriftCorrect)
    # allow_setup (1-press ESCAPE to recalibrate, 0-not allowed)
    #
    # Skip drift-check if running the script in Dummy Mode
    while not dummy_mode:
        # terminate the task if no longer connected to the tracker or
        # user pressed Ctrl-C to terminate the task
        if (not el_tracker.isConnected()) or el_tracker.breakPressed():
            terminate_task()

        # drift-check and re-do camera setup if ESCAPE is pressed
        try:
            error = el_tracker.doDriftCorrect(int(scn_width/2.0),
                                              int(scn_height/2.0), 1, 1)
            # break following a success drift-check
            if error is not pylink.ESC_KEY:
                break
        except:
            pass

    # put tracker in idle/offline mode before recording
    el_tracker.setOfflineMode()

    # Start recording, at the beginning of a new run
    # arguments: sample_to_file, events_to_file, sample_over_link,
    # event_over_link (1-yes, 0-no)
    try:
        el_tracker.startRecording(1, 1, 1, 1)
    except RuntimeError as error:
        print("ERROR:", error)
        terminate_task()

    # Allocate some time for the tracker to cache some samples
    pylink.pumpDelay(100)

    # wait for the MRI scanner to trigger the presentation of the stimuli
    # The trigger is usually converted into a keyboard event, i.e., a key press
    # frequently used trigger keys include "q", "t", "5", "escape" etc.
    prompt = 'Run # %d: Waiting for MRI signal...' % (block) + \
        '\n\nPress q, t, 5 or ESCAPE, if you are debugging the script'
    show_msg(win, prompt, wait_for_keypress=False)
    
    while not event.getKeys(['q', 't', '5', 'escape']):
    	# In case Ctrl-c is pressed terminate the task      
        for keycode, modifier in event.getKeys(modifiers=True):
            if keycode == 'c' and (modifier['ctrl'] is True):
                el_tracker.sendMessage('terminated_by_user')
                terminate_task()
        pass

    # record a message to mark the start of scanning
    el_tracker.sendMessage('Scan_start_Run_%d' % (block))

    # reset the global clock to compare stimulus timing
    # to time 0 to make sure each trial is 6-sec long
    # this is known as "non-slip timing"
    scan_clock.reset()

    for trial_pars in test_list:
        run_trial(trial_pars, trial_index, block, block_len, scan_clock)
        trial_index += 1

    # send a message to mark the end of a run
    el_tracker.sendMessage('Scan_end_Run_%d' % (block))

    # clear the screen
    clear_screen(win)

    # stop recording; add 100 msec to catch final events before stopping
    pylink.pumpDelay(100)
    el_tracker.stopRecording()

# Step 7: disconnect, download the EDF file, then terminate the task
terminate_task()
