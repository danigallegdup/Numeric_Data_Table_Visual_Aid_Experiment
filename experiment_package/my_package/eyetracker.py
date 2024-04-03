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



class EyeTracker:
    def __init__(self):
        self.el_tracker = None
        self.dummy_mode = False
        self.edf_file_name = "pilot1.EDF"

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
        self.setup_data_file()
        self.start_tracking()
        

    def setup_data_file(self):
        self.el_tracker.openDataFile(self.edf_file_name)
        preamble_text = 'RECORDED BY %s' % os.path.basename(__file__)
        self.el_tracker.sendCommand("add_file_preamble_text '%s'" % preamble_text)

    def start_tracking(self):
        # Start recording samples and events
        self.el_tracker.openDataFile(self.edf_file_name)
        
        self.el_tracker.setOfflineMode()
        pylink.pumpDelay(100)
        
        error = self.el_tracker.startRecording(1, 1, 1, 1)
        if error:
            return error

        # Begin real-time mode
        pylink.beginRealTimeMode(100)
    
    def get_tracker(self):
        return self.el_tracker
    

        # ------- Eye Tracker File Transfer and clean up
    def close_eye_tracker(self):
        """Closes the EyeLink tracker."""
        # Step 7: File transfer and cleanup
        if self.el_tracker is not None:
            self.el_tracker.stopRecording()
            self.el_tracker.setOfflineMode()
            pylink.msecDelay(500)

            # Close the edf data file on the Host
            self.el_tracker.closeDataFile()

            results_folder = 'results'
           
            # transfer the edf file to the Display PC and rename it
            local_file_name = os.path.join(results_folder, self.edf_file_name)

            try:
                self.el_tracker.receiveDataFile(self.edf_file_name, local_file_name)
            except RuntimeError as error:
                print('ERROR:', error)

        # Step 8: close EyeLink connection and quit display-side graphics
        self.el_tracker.close()