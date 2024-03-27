Python / PyLink examples

SR Research Ltd. provides these examples to illustrate how to use the PyLink library to interface with the EyeLink trackers in Python. 

## Install and Usage

To use these example scripts, please first install the EyeLink Developers Kit, available from the SR Support Forum (http://sr-support.com/thread-13.html). To properly install the PyLink library, please see Section 3.3 of the "Getting Started with Python and PyLink.pdf" in the parent folder. If the PyLink library is properly, no error message should come up when enter the following command in the Python shell:

   import pylink

### Scripts that does not require PsychoPy and Pygame 

The EyeLink Developers Kit comes with some SDL graphics routines for tracker calibration, etc. It is possible to run some of the scripts without installing additional Python libraries (e.g., Pygame). The "link_event" and "link_sample" folder contain the following scripts.

link_event -- This script shows the frequently used commands for connecting to the tracker, configuring tracker parameters, starting / ending recording, and messaging for event logging. Most importantly, this script shows how to retrieve eye events (Fixation Start / End, Saccade Start / End, etc.) during data recording from the stimulus presentation PC.

link_sample -- This script shows the frequently used commands for connecting to the tracker, configuring tracker parameters, starting / ending recording, and messaging for event logging. Most importantly, this script shows how to retrieve samples (time stamped gaze position, pupil size, etc.) in real-time during data recording.


### Scripts that require PsychoPy or Pygame

In a typical experimental task, one may use a dedicated library for graphics generation, keyboard response collection, etc. There are lots of free (or open source) Python libraries that one can use for this purpose. Here we provide examples for PsychoPy and Pygame to illustrate the eye tracker integration with a Python-based programming tool through the PyLink library. 

Note that for both the PsychoPy and Pygame examples, there is an accompanying library in the same folder as the example script-- EyeLinkCoreGraphicsPsychoPy.py. There are also three .wav files that this .py library depends on. The EyeLinkCoreGraphicsPsychoPy.py library and the .wav files are needed for tracker calibration. You don’t need to change these files in any way, but please include them in your experimental scripts folder.

Please see below for descriptions of the examples in the "PsychoPy_examples" and "Pygame_examples" folders.

fixationWindow_fastSamples -- This is a basic example, which shows how to implement a gaze-based trigger. We first show a fixation cross at the center of the screen. A trial will move on only when the gaze has been directed to the fixation cross. We then show a picture and wait for the participant to issue a keypress response, or until 5 seconds have elapsed.

GC_window -- This example script shows how to manipulate the visual stimuli based on real-time gaze data. A mask is shown at the current gaze position in the "mask" condition; in the "window" condition, the image is masked, and a window at the current gaze position will reveal the image hidden behind.

MRI_demo -- This is a basic example illustrating how to do continuous eye tracker recording through a block of trials (e.g., in an MRI setup), and how to synchronize the presentation of trials with a sync signal from the MRI. With a long recording, we start and stop recording at the beginning and end of a testing session (run), rather than at the beginning and end of each experimental trial. We still send the TRIALID and TRIAL_RESULT messages to the tracker, and Data Viewer will still be able to segment the long recording into small segments (trials).

picture -- This is a basic example, which shows how to connect to and disconnect from the tracker, how to open and close data files, how to start / stop recording, and the standard messages for integration with the Data Viewer software. We show four pictures one-by-one on each trial, and a trial terminates upon a keypress response or until 3 secs have elapsed.

pursuit -- This example script shows how to record the target position in a smooth pursuit task. This script also shows how to record dynamic Interest Area and target position information to the EDF data file so Data Viewer can recreate the interest area and playback the target movement.

saccade -- This example script shows how to retrieve eye events (saccades) during testing. A visual target appears on the left side, or right side of the screen and the participant is required to quickly shift gaze to look at the target (pro-saccade) or a mirror location on the opposite side of the central fixation (anti-saccade).

The "PsychoPy_examples" folder also includes an example on video playback.

video -- This example script shows how to present video stimuli and how to log frame information in the EDF data file so the gaze data can be correctly laid over the video in Data Viewer

### Scripts and Plugins for OpenSesame

For users that are using OpenSesame (http://osdoc.cogsci.nl/) as their experimental software, please refer to the "OpenSesame EyeLink Plugin User Manual.pdf" in the "OpenSesame" folder for specific on how to install the PyLink library and the EyeLink Plugins into OpenSesame. 

### Folder structure

|--linkEvent
|   |--link_event.py
|
|--linkSample
|   |--link_sample.py
|
|--OpenSesame
|   |--OpenSesame_eyelink_plugin
|   |--OpenSesame_examples
|   |--OpenSesame EyeLink Plugin User Manual.pdf
|
|---Psychopy
|   |--fixationWidnow_fast
|   |    |--images
|   |    |--EyeLinkCoreGraphicsPsychoPy.py
|   |    |--fixationWidnow_fast.py
|   |
|   |--GC_window
|   |    |--images
|   |    |--EyeLinkCoreGraphicsPsychoPy.py
|   |    |--GC_window.py
|   |
|   |--MRI_demo
|   |    |--images
|   |    |--EyeLinkCoreGraphicsPsychoPy.py
|   |    |--MRI_demo.py
|   |
|   |--picture
|   |    |--images
|   |    |--EyeLinkCoreGraphicsPsychoPy.py
|   |    |--picture.py
|   |
|   |--pursuit
|   |    |--EyeLinkCoreGraphicsPsychoPy.py
|   |    |--pursuit.py
|   |
|   |--pursuit
|   |    |--EyeLinkCoreGraphicsPsychoPy.py
|   |    |--pursuit.py
|   |
|   |--video
|        |--videos
|        |--EyeLinkCoreGraphicsPsychoPy.py
|        |--video.py
|
|---Pygame
|   |--fixationWidnow_fast
|   |    |--fixationWidnow_fast.py
|   |    |--images
|   |    |--CalibrationGraphicsPygame.py
|   |    |--qbeep.wav
|   |    |--type.wav
|   |    |--error.wav
|   |
|   |--GC_window
|   |    |--GC_window.py
|   |    |--images
|   |    |--CalibrationGraphicsPygame.py.py
|   |    |--qbeep.wav
|   |    |--type.wav
|   |    |--error.wav
|   |
|   |--MRI_demo
|   |    |--MRI_demo.py
|   |    |--images
|   |    |--CalibrationGraphicsPygame.py.py
|   |    |--qbeep.wav
|   |    |--type.wav
|   |    |--error.wav
|   |
|   |--picture
|   |    |--picture.py
|   |    |--images
|   |    |--CalibrationGraphicsPygame.py.py
|   |    |--qbeep.wav
|   |    |--type.wav
|   |    |--error.wav
|   |
|   |--pursuit
|   |    |--pursuit.py
|   |    |--CalibrationGraphicsPygame.py.py
|   |    |--qbeep.wav
|   |    |--type.wav
|   |    |--error.wav
|   |
|   |--saccade
|        |--saccade.py
|        |--CalibrationGraphicsPygame.py.py
|        |--qbeep.wav
|        |--type.wav
|        |--error.wav
|
|--README.md
