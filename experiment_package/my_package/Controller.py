import csv
import threading
import pyautogui
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime
import os

from .Constants import *
from .eyetracker import *


class Controller:
    def __init__(self, eye_tracker):
        # INDEXES FOR BOTH GUI'S TO STAY IN SYNC
        self.current_index = -1
        self.experimentor_is_ready = False
        self.name_of_task = None

        # EYE TRACKER
        self.eye_tracker = eye_tracker
        
        # MOUSE
        self.mouse_log_enabled = False
        self.mouse_log = []
        self.mouse_log_thread = None
        
        # TIMERS
        self.start_task_milliseconds = None # When the Participants sees the prompt screen (when the task started)
        self.start_time_milliseconds = None # when paticipants sees the stimulous -- table
        self.end_time_milliseconds = None # when paticipants hits the space bar to exit the stimulous
        self.start_time_datetime = None # when paticipants sees the stimulous -- table
        self.end_time_datetime = None # when paticipants hits the space bar to exit the stimulous
        self.time_spend = None # end_time - start_time

        # EYE TRACKER DATA
        self.fixation_log = []
        self.saccade_log = []
        self.track_message= ""

# Eye Tracker
    def start_tracking_message(self, name_of_task):
        # Start recording samples and events
        el_tracker = self.eye_tracker.get_tracker()
        self.track_message = name_of_task
        el_tracker.sendMessage(self.track_message)
    
    def stop_tracking_message(self):
        el_tracker = self.eye_tracker.get_tracker()
        self.track_message = "_" + self.track_message
        el_tracker.sendMessage(self.track_message)





# timers

    def set_start_task_milliseconds(self, start):
        self.start_task_milliseconds = start

    def set_start_time_milliseconds(self, start):
        self.start_time_milliseconds = start
        self.set_start_time_date_time()

    def set_start_time_date_time(self):
        self.start_time_datetime = datetime.now()

    def set_end_time_milliseconds(self, end):
        self.end_time_milliseconds = end
        self.set_end_time_date_time()

    def set_end_time_date_time(self):
        self.end_time_datetime = datetime.now()
        self.time_spend = (self.end_time_datetime - self.start_time_datetime).total_seconds()*1000

    def get_all_times(self):
        return [self.start_time_datetime, self.end_time_datetime, 
                self.start_time_milliseconds, self.end_time_milliseconds, 
                self.time_spend, self.start_task_milliseconds]
    
# Counter 

    def update_counter(self):
        if(self.experimentor_is_ready):
            if self.current_index <80: # 80 tasks
                self.current_index = (self.current_index + 1)
            print( self.current_index)
            self.experimentor_is_ready = False
        else:
            print("Experimentor is not ready")
        
        return self.current_index
    
    def get_experimenter_status(self):
        return self.experimentor_is_ready
    
    def experimentor_ready(self):
        self.experimentor_is_ready = True

    def get_counter(self):
        return self.current_index
    
# mouse logs

    def start_mouse_logging(self, name_of_task):
        self.mouse_log_enabled = True
        self.mouse_log = []
        self.mouse_log_thread = threading.Thread(target=self.log_mouse_position)
        self.mouse_log_thread.start()
        self.name_of_task = name_of_task

    def stop_mouse_logging(self):
        self.mouse_log_enabled = False
        if self.mouse_log_thread is not None:
            self.mouse_log_thread.join()
        self.save_mouse_log()

    def log_mouse_position(self):
        while self.mouse_log_enabled:
            position = pyautogui.position()
            self.mouse_log.append((datetime.now(), position))
            time.sleep(0.1)  # Log every 100 milliseconds
            self.save_mouse_log() # Save log to file

    def save_mouse_log(self):
        # Ensure the directory exists
        filename = OutputFilePaths.mouse_log_path + self.name_of_task + f"-mouse_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        directory = os.path.dirname(filename)

        if not os.path.exists(directory):
            os.makedirs(directory)
        
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "X", "Y"])
            for log_entry in self.mouse_log:
                timestamp, position = log_entry
                writer.writerow([timestamp, position.x, position.y])
