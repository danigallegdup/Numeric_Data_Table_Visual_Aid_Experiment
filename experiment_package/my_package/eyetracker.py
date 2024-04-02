from __future__ import division
from __future__ import print_function

import csv
import threading
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime

import sys
import os
import pylink

from .Controller import *
from .Constants import *
from .Experimenters_Interface import *

# Dummy mode flag - set to True if no real tracker is connected
dummy_mode = False

class EyeTracker:
    SCN_WIDTH = 1920
    SCN_HEIGHT = 1080

    def __init__(self):
        self.dummy_mode = dummy_mode
        self.el_tracker = None

    def on_escape(self, event=None):
        pylink.closeGraphics()

    def initialize_tracker(self):
        if self.dummy_mode:
            self.el_tracker = pylink.EyeLink(None)
            print('Dummy mode activated. No real-time eye tracking data will be available.')
        else:
            try:
                self.el_tracker = pylink.EyeLink("100.1.1.1")
            except RuntimeError as error:
                print('ERROR:', error)
                sys.exit()

    def setup_display(self):
        pylink.openGraphics((self.SCN_WIDTH, self.SCN_HEIGHT), 32)

    def setup_data_file(self):
        edf_file_name = "TEST.EDF"
        self.el_tracker.openDataFile(edf_file_name)
        preamble_text = 'RECORDED BY %s' % os.path.basename(__file__)
        self.el_tracker.sendCommand("add_file_preamble_text '%s'" % preamble_text)

    def setup_tracker_options(self):
        self.el_tracker.setOfflineMode()
        pix_msg = "screen_pixel_coords 0 0 %d %d" % (self.SCN_WIDTH - 1, self.SCN_HEIGHT - 1)
        self.el_tracker.sendCommand(pix_msg)
        self.el_tracker.sendCommand("calibration_type = HV9")
        self.el_tracker.sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT")
        self.el_tracker.sendCommand("file_sample_data = GAZE,GAZERES,HREF,AREA,STATUS,INPUT")

    def calibrate_tracker(self):
        self.el_tracker.doTrackerSetup()

    def setup(self):
        self.initialize_tracker()
        self.setup_display()
        self.setup_data_file()
        self.setup_tracker_options()
        self.calibrate_tracker()

    def close(self):
        if self.el_tracker is not None:
            self.el_tracker.setOfflineMode()
            pylink.msecDelay(500)
            self.el_tracker.closeDataFile()

            results_folder = 'results'
            edf_file_name = "TEST.EDF"
            local_file_name = os.path.join(results_folder, edf_file_name)

            try:
                self.el_tracker.receiveDataFile(edf_file_name, local_file_name)
            except RuntimeError as error:
                print('ERROR:', error)

            self.el_tracker.close()