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
# This example shows how to implement a gaze-based trigger.
# We show a fixation cross at the center of the screen. A trial would move
# on only when the eyes are looking at the fixation cross.
# We then show a picture and wait for the participant to issue a keypress
# response or until 5 secs have elapsed.
#
# Last updated: 3/29/2021

from __future__ import division
from __future__ import print_function

import pylink
import os
import platform
import sys
import pygame
import random
import time
from pygame.locals import *
from CalibrationGraphicsPygame import CalibrationGraphics
from math import fabs
from string import ascii_letters, digits

# Switch to the script folder
script_path = os.path.dirname(sys.argv[0])
if len(script_path) != 0:
    os.chdir(script_path)

# initialize pygame
pygame.init()

# Set this variable to True to run the script in "Dummy Mode"
dummy_mode = False

#Workaround for pygame 2.0 shows black screen when running in full 
#screen mode in linux
full_screen=True

if 'Linux' in platform.platform():
    if int(pygame.version.ver[0])>1:
        full_screen=False

# get the screen resolution natively supported by the monitor
scn_width, scn_height = 0,0

# Store the parameters of all trials in a list, [cond, image]
trials = [
    ['cond_1', 'img_1.jpg'],
    ['cond_2', 'img_2.jpg'],
    ]

# Set up EDF data file name and local data folder
#
# The EDF data filename should not exceed eight alphanumeric characters
# use ONLY number 0-9, letters, and _ (underscore) in the filename
edf_fname = 'TEST'

# Prompt user to specify an EDF data filename
# before we open a fullscreen window
while True:
    # use "raw_input" to get user input if running with Python 2.x
    try:
        input = raw_input
    except NameError:
        pass
    prompt = '\nSpecify an EDF filename\n' + \
        'Filename must not exceed eight alphanumeric characters.\n' + \
        'ONLY letters, numbers and underscore are allowed.\n\n--> '
    edf_fname = input(prompt)
    # strip trailing characters, ignore the '.edf' extension
    edf_fname = edf_fname.rstrip().split('.')[0]

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
        pygame.quit()
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
    pygame.quit()
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
# open a Pygame window
win=None
if full_screen:
    win = pygame.display.set_mode((0, 0), FULLSCREEN | DOUBLEBUF)
else:
    win = pygame.display.set_mode((0, 0), 0)
    
scn_width, scn_height = win.get_size()
pygame.mouse.set_visible(False)  # hide mouse cursor

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
genv = CalibrationGraphics(el_tracker, win)

# Set background and foreground colors
# parameters: foreground_color, background_color
foreground_color = (0, 0, 0)
background_color = (128, 128, 128)
genv.setCalibrationColors(foreground_color, background_color)

# Set up the calibration target
#
# The target could be a "circle" (default) or a "picture",
# To configure the type of calibration target, set
# genv.setTargetType to "circle", "picture", e.g.,
# genv.setTargetType('picture')
#
# Use gen.setPictureTarget() to set a "picture" target, e.g.,
# genv.setPictureTarget(os.path.join('images', 'fixTarget.bmp'))

# Use the default calibration target
genv.setTargetType('circle')

# Configure the size of the calibration target (in pixels)
genv.setTargetSize(24)

# Beeps to play during calibration, validation and drift correction
# parameters: target, good, error
#     target -- sound to play when target moves
#     good -- sound to play on successful operation
#     error -- sound to play on failure or interruption
# Each parameter could be ''--default sound, 'off'--no sound, or a wav file
# e.g., genv.setCalibrationSounds('type.wav', 'qbeep.wav', 'error.wav')
genv.setCalibrationSounds('', '', '')

# Request Pylink to use the Pygame window we opened above for calibration
pylink.openGraphicsEx(genv)

# Step 5: Run the experimental trials
# define a few helper functions for trial handling


def show_message(message, fg_color, bg_color):
    """ show messages on the screen

    message: The message you would like to show on the screen
    fg_color/bg_color: color for the texts and the background screen
    """

    # clear the screen and blit the texts
    win_surf = pygame.display.get_surface()
    win_surf.fill(bg_color)

    scn_w, scn_h = win_surf.get_size()
    message_fnt = pygame.font.SysFont('Arial', 32)
    msgs = message.split('\n')
    for i in range(len(msgs)):
        message_surf = message_fnt.render(msgs[i], True, fg_color)
        w, h = message_surf.get_size()
        msg_y = scn_h / 2 + h / 2 * 2.5 * (i - len(msgs) / 2.0)
        win_surf.blit(message_surf, (int(scn_w / 2 - w / 2), int(msg_y)))

    pygame.display.flip()


def wait_key(key_list, duration=sys.maxsize):
    """ detect and return a keypress, terminate the task if ESCAPE is pressed

    parameters:
    key_list: allowable keys (pygame key constants, e.g., [K_a, K_ESCAPE]
    duration: the maximum time allowed to issue a response (in ms)
              wait for response 'indefinitely' (with sys.maxsize)
    """

    got_key = False
    # clear all cached events if there are any
    pygame.event.clear()
    t_start = pygame.time.get_ticks()
    resp = [None, t_start, -1]

    while not got_key:
        # check for time out
        if (pygame.time.get_ticks() - t_start) > duration:
            break

        # check key presses
        for ev in pygame.event.get():
            if ev.type == KEYDOWN:
                if ev.key in key_list:
                    resp = [pygame.key.name(ev.key),
                            t_start,
                            pygame.time.get_ticks()]
                    got_key = True

            if (ev.type == KEYDOWN) and (ev.key == K_c):
                if ev.mod in [KMOD_LCTRL, KMOD_RCTRL, 4160, 4224]:
                    terminate_task()

    # clear the screen following each keyboard response
    win_surf = pygame.display.get_surface()
    win_surf.fill(genv.getBackgroundColor())
    pygame.display.flip()

    return resp


def terminate_task():
    """ Terminate the task gracefully and retrieve the EDF data file

    file_to_retrieve: The EDF on the Host that we would like to download
    win: the current window used by the experimental script
    """

    # disconnect from the tracker if there is an active connection
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
        show_message(msg, (0, 0, 0), (128, 128, 128))

        # Download the EDF data file from the Host PC to a local data folder
        # parameters: source_file_on_the_host, destination_file_on_local_drive
        local_edf = os.path.join(session_folder, session_identifier + '.EDF')
        try:
            el_tracker.receiveDataFile(edf_file, local_edf)
        except RuntimeError as error:
            print('ERROR:', error)

        # Close the link to the tracker.
        el_tracker.close()

    # quit pygame and python
    pygame.quit()
    sys.exit()


def abort_trial():
    """Ends recording

    We add 100 msec to catch final events
    """

    # get the currently active tracker object (connection)
    el_tracker = pylink.getEYELINK()

    # Stop recording
    if el_tracker.isRecording():
        # add 100 ms to catch final trial events
        pylink.pumpDelay(100)
        el_tracker.stopRecording()

    # clear the screen
    surf = pygame.display.get_surface()
    surf.fill((128, 128, 128))
    pygame.display.flip()
    # Send a message to clear the Data Viewer screen
    el_tracker.sendMessage('!V CLEAR 128 128 128')

    # send a message to mark trial end
    el_tracker.sendMessage('TRIAL_RESULT %d' % pylink.TRIAL_ERROR)


def run_trial(trial_pars, trial_index, should_recal):
    """ Helper function specifying the events that will occur in a single trial

    trial_pars - a list containing trial parameters, e.g.,
                ['cond_1', 'img_1.jpg']
    trial_index - record the order of trial presentation in the task
    should_recal - we recalibrate the tracker? 'yes' vs. 'no'
    """

    # unpacking the trial parameters
    cond, pic = trial_pars

    # load the image to display, here we stretch the image to fill full screen
    img = pygame.image.load('./images/' + pic)
    img = pygame.transform.scale(img, (scn_width, scn_height))

    # get the currently active window
    surf = pygame.display.get_surface()

    # get a reference to the currently active EyeLink connection
    el_tracker = pylink.getEYELINK()

    if should_recal == 'yes':
        recal_msg = 'Please press ENTER to recalibrate the tracker'
        show_message(recal_msg, (0, 0, 0), (128, 128, 128))
        wait_key([K_RETURN])
        try:
            el_tracker.doTrackerSetup()
        except RuntimeError as err:
            print('ERROR:', err)
            el_tracker.exitCalibration()
        should_recal = 'no'

    # put the tracker in the offline mode first
    el_tracker.setOfflineMode()

    # clear the host screen before we draw the backdrop
    el_tracker.sendCommand('clear_screen 0')

    # show a backdrop image on the Host screen, imageBackdrop() the recommended
    # function, if you do not need to scale the image on the Host
    # parameters: image_file, crop_x, crop_y, crop_width, crop_height,
    #             x, y on the Host, drawing options
##    el_tracker.imageBackdrop(os.path.join('images', pic),
##                             0, 0, scn_width, scn_height, 0, 0,
##                             pylink.BX_MAXCONTRAST)

    # If you need to scale the backdrop image on the Host, use the old Pylink
    # bitmapBackdrop(), which requires an additional step of converting the
    # image pixels into a recognizable format by the Host PC.
    # pixels = [line1, ...lineH], line = [pix1,...pixW], pix=(R,G,B)
    #
    # the bitmapBackdrop() command takes time to return, not recommended
    # for tasks where the ITI matters, e.g., in an event-related fMRI task
    # parameters: width, height, pixel, crop_x, crop_y,
    #             crop_width, crop_height, x, y on the Host, drawing options
    #
    # Use the code commented below to convert the image and send the backdrop
    #
    pixels = [[img.get_at((i, j))[0:3] for i in range(scn_width)]
              for j in range(scn_height)]
    el_tracker.bitmapBackdrop(scn_width, scn_height, pixels,
                              0, 0, scn_width, scn_height,
                              0, 0, pylink.BX_MAXCONTRAST)

    # OPTIONAL: draw landmarks on the Host screen
    # In addition to backdrop image, You may draw simples on the Host PC to use
    # as landmarks. For illustration purpose, here we draw some texts and a box
    # For a list of supported draw commands, see the "COMMANDS.INI" file on the
    # Host PC (under /elcl/exe)
    left = int(scn_width/2.0) - 60
    top = int(scn_height/2.0) - 60
    right = int(scn_width/2.0) + 60
    bottom = int(scn_height/2.0) + 60
    draw_cmd = 'draw_filled_box %d %d %d %d 1' % (left, top, right, bottom)
    el_tracker.sendCommand(draw_cmd)

    # send a "TRIALID" message to mark the start of a trial, see Data
    # Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
    el_tracker.sendMessage('TRIALID %d' % trial_index)

    # record_status_message : show some info on the Host PC
    # here we show how many trial has been tested
    status_msg = 'TRIAL number %d' % trial_index
    el_tracker.sendCommand("record_status_message '%s'" % status_msg)

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

    # determine which eye(s) is/are available
    # 0- left, 1-right, 2-binocular
    eye_used = el_tracker.eyeAvailable()
    if eye_used == 1:
        el_tracker.sendMessage("EYE_USED 1 RIGHT")
    elif eye_used == 0 or eye_used == 2:
        el_tracker.sendMessage("EYE_USED 0 LEFT")
        eye_used = 0
    else:
        print("Error in getting the eye information!")
        return pylink.TRIAL_ERROR

    # put the central fixation cross on screen for 1000 ms
    surf.fill((128, 128, 128))  # clear the screen
    pygame.draw.line(win, (0, 255, 0),
                     (int(scn_width/2.0-20), int(scn_height/2.0)),
                     (int(scn_width/2.0+20), int(scn_height/2.0)), 3)
    pygame.draw.line(win, (0, 255, 0),
                     (int(scn_width/2.0), int(scn_height/2.0-20)),
                     (int(scn_width/2.0), int(scn_height/2.0+20)), 3)
    pygame.display.flip()

    # send over a message to log the onset of the fixation cross
    el_tracker.sendMessage('fix_onset')

    # OPTIONAL - send over messages to request Data Viewer to draw
    # a cross when visualizing the data; see Data Viewer User Manual,
    # Protocol for EyeLink Data to Viewer Integration
    line_hor = (scn_width/2 - 20, scn_height/2, scn_width/2 + 20, scn_height/2)
    line_ver = (scn_width/2, scn_height/2 - 20, scn_width/2, scn_height/2 + 20)
    el_tracker.sendMessage('!V CLEAR 128 128 128')  # clear the screen
    el_tracker.sendMessage('!V DRAWLINE 0 255 0 %d %d %d %d' % line_hor)
    el_tracker.sendMessage('!V DRAWLINE 0 255 0 %d %d %d %d' % line_ver)

    # Here we implement a gaze trigger, so the target only comes up when
    # the subject direct gaze to the fixation cross
    new_sample = None
    old_sample = None
    trigger_fired = False
    in_hit_region = False
    trigger_start_time = pygame.time.get_ticks()
    # fire the trigger following a 300-ms gaze
    minimum_duration = 300
    gaze_start = -1
    while not trigger_fired:
        # abort the current trial if the tracker is no longer recording
        error = el_tracker.isRecording()
        if error is not pylink.TRIAL_OK:
            el_tracker.sendMessage('tracker_disconnected')
            abort_trial()
            return error

        # if the trigger did not fire in 10 seconds, abort trial
        if pygame.time.get_ticks() - trigger_start_time >= 10000:
            el_tracker.sendMessage('trigger_timeout_recal')
            # re-calibrate in the following trial
            should_recal = 'yes'
            # abort trial
            abort_trial()
            return should_recal

        # check for keyboard events, skip a trial if ESCAPE is pressed
        # terminate the task is Ctrl-C is pressed
        for ev in pygame.event.get():
            if (ev.type == KEYDOWN) and (ev.key == K_ESCAPE):
                el_tracker.sendMessage('abort_and_recal')
                # re-calibrate in the following trial
                should_recal = 'yes'
                # abort trial
                abort_trial()
                return should_recal

            if (ev.type == KEYDOWN) and (ev.key == K_c):
                if ev.mod in [KMOD_LCTRL, KMOD_RCTRL, 4160, 4224]:
                    el_tracker.sendMessage('terminated_by_user')
                    terminate_task()
                    return pylink.ABORT_EXPT

        # Do we have a sample in the sample buffer?
        # and does it differ from the one we've seen before?
        new_sample = el_tracker.getNewestSample()
        if new_sample is not None:
            if old_sample is not None:
                if new_sample.getTime() != old_sample.getTime():
                    # check if the new sample has data for the eye
                    # currently being tracked; if so, we retrieve the current
                    # gaze position and PPD (how many pixels correspond to 1
                    # deg of visual angle, at the current gaze position)
                    if eye_used == 1 and new_sample.isRightSample():
                        g_x, g_y = new_sample.getRightEye().getGaze()
                    if eye_used == 0 and new_sample.isLeftSample():
                        g_x, g_y = new_sample.getLeftEye().getGaze()

                    # break the while loop if the current gaze position is
                    # in a 120 x 120 pixels region around the screen centered
                    fix_x, fix_y = (scn_width/2.0, scn_height/2.0)
                    if fabs(g_x - fix_x) < 60 and fabs(g_y - fix_y) < 60:
                        # record gaze start time
                        if not in_hit_region:
                            if gaze_start == -1:
                                gaze_start = pygame.time.get_ticks()
                                in_hit_region = True
                        # check the gaze duration and fire
                        if in_hit_region:
                            gaze_dur = pygame.time.get_ticks() - gaze_start
                            if gaze_dur > minimum_duration:
                                trigger_fired = True
                    else:  # gaze outside the hit region, reset variables
                        in_hit_region = False
                        gaze_start = -1

            # update the "old_sample"
            old_sample = new_sample

    # show the image
    surf.fill((128, 128, 128))  # clear the screen
    surf.blit(img, (0, 0))
    pygame.display.flip()
    onset_time = pygame.time.get_ticks()  # image onset time

    # send over a message to mark the onset of the image
    el_tracker.sendMessage('image_onset')

    # Send a message to clear the Data Viewer screen, get it ready for
    # drawing the pictures during visualization
    el_tracker.sendMessage('!V CLEAR 128 128 128')

    # send over a message to specify where the image is stored relative
    # to the EDF data file, see Data Viewer User Manual, "Protocol for
    # EyeLink Data to Viewer Integration"
    bg_image = '../../images/' + pic
    imgload_msg = '!V IMGLOAD CENTER %s %d %d %d %d' % (bg_image,
                                                        int(scn_width/2.0),
                                                        int(scn_height/2.0),
                                                        int(scn_width),
                                                        int(scn_height))
    el_tracker.sendMessage(imgload_msg)

    # send interest area messages to record in the EDF data file
    # here we draw a rectangular IA, for illustration purposes
    # format: !V IAREA RECTANGLE <id> <left> <top> <right> <bottom> [label]
    # for all supported interest area commands, see the Data Viewer Manual,
    # "Protocol for EyeLink Data to Viewer Integration"
    ia_pars = (1, left, top, right, bottom, 'screen_center')
    el_tracker.sendMessage('!V IAREA RECTANGLE %d %d %d %d %d %s' % ia_pars)

    # show the image for 5 secs; break if the SPACEBAR is pressed
    pygame.event.clear()  # clear all cached events if there were any
    get_keypress = False
    RT = -1
    while not get_keypress:
        # present the picture for a maximum of 5 seconds
        if pygame.time.get_ticks() - onset_time >= 5000:
            el_tracker.sendMessage('time_out')
            break

        # abort the current trial if the tracker is no longer recording
        error = el_tracker.isRecording()
        if error is not pylink.TRIAL_OK:
            el_tracker.sendMessage('tracker_disconnected')
            abort_trial()
            return error

        # check for keyboard events
        for ev in pygame.event.get():
            # Stop stimulus presentation when the spacebar is pressed
            if (ev.type == KEYDOWN) and (ev.key == K_SPACE):
                # send over a message to log the key press
                el_tracker.sendMessage('key_pressed')

                # get response time in ms, PsychoPy report time in sec
                RT = pygame.time.get_ticks() - onset_time
                get_keypress = True

            # Abort a trial if "ESCAPE" is pressed
            if (ev.type == KEYDOWN) and (ev.key == K_ESCAPE):
                el_tracker.sendMessage('trial_skipped_by_user')
                # abort trial
                abort_trial()
                return pylink.SKIP_TRIAL

            # Terminate the task if Ctrl-c
            if (ev.type == KEYDOWN) and (ev.key == K_c):
                if ev.mod in [KMOD_LCTRL, KMOD_RCTRL, 4160, 4224]:
                    el_tracker.sendMessage('terminated_by_user')
                    terminate_task()
                    return pylink.ABORT_EXPT

    # clear the screen
    surf.fill((128, 128, 128))
    pygame.display.flip()
    el_tracker.sendMessage('blank_screen')
    # send a message to clear the Data Viewer screen as well
    el_tracker.sendMessage('!V CLEAR 128 128 128')

    # stop recording; add 100 msec to catch final events before stopping
    pylink.pumpDelay(100)
    el_tracker.stopRecording()

    # record trial variables to the EDF data file, for details, see Data
    # Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
    el_tracker.sendMessage('!V TRIAL_VAR condition %s' % cond)
    el_tracker.sendMessage('!V TRIAL_VAR image %s' % pic)
    el_tracker.sendMessage('!V TRIAL_VAR RT %d' % RT)

    # send a 'TRIAL_RESULT' message to mark the end of trial, see Data
    # Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
    el_tracker.sendMessage('TRIAL_RESULT %d' % pylink.TRIAL_OK)

    return should_recal

# Step 5: Set up the camera and calibrate the tracker

# Show the task instructions
if dummy_mode:
    task_msg = 'Cannot run the script in Dummy mode,\n' + \
        'Press ENTER to quit the script'
else:
    task_msg = 'On each trial, look at the cross to start,\n' + \
        'then press SPACEBAR to end a trial\n' + \
        '\nPress Ctrl-C if you need to quit the task early\n' + \
        '\nNow, press ENTER to calibrate tracker'

# Pygame bug warning
pygame_warning = '\n\nDue to a bug in Pygame 2, the window may have lost' + \
                 '\nfocus and stopped accepting keyboard inputs.' + \
                 '\nClicking the mouse helps get around this issue.'
if pygame.__version__.split('.')[0] == '2':
    task_msg = task_msg + pygame_warning

show_message(task_msg, (0, 0, 0), (128, 128, 128))
wait_key([K_RETURN])

# Terminate the task if running in Dummy Mode
if dummy_mode:
    print('ERROR: This task requires real-time gaze data.\n' +
          'It cannot run in Dummy mode (with no tracker connection).')
    terminate_task()
else:
    try:
        el_tracker.doTrackerSetup()
    except RuntimeError as err:
        print('ERROR:', err)
        el_tracker.exitCalibration()

# Step 6: Run the experimental trials, index all the trials

# construct a list of 4 trials
test_list = trials[:]*2

# randomize the trial list
random.shuffle(test_list)

trial_index = 1
should_recal = 'no'
for trial_pars in test_list:
    should_recal = run_trial(trial_pars, trial_index, should_recal)
    trial_index += 1

# Step 7: disconnect, download the EDF file, then terminate the task
terminate_task()
