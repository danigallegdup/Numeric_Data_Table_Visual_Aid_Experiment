import csv
import threading
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime

from .Controller import *
from .Constants import *
from .Experimenters_Interface import *
class Participants_Interface:
    def __init__(self, root, data_dictionary, controller):

        self.controller = controller
        self.root = root
        self.keys_list = list(data_dictionary.keys())
        self.data_dictionary = data_dictionary
        self.state = -1  # 0: prompt, 1: table, 2: progress
        self.can_progress = True
        self.previous_counter = controller.get_counter()

        self.initialize_gui()
        self.bind_events()
        self.update_screen()

    def initialize_gui(self):
        # GUI setup
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.photo = ImageTk.PhotoImage(Image.new('RGB', (self.screen_width, self.screen_height)))
        self.picture_label = tk.Label(self.root, image=self.photo)
        self.picture_label.pack(fill="both", expand=True)

    def bind_events(self):
        self.root.bind('<space>', self.update_screen)

    def display_intro_text(self):
        self.picture_label.config(text=ExperimentConstants.Introduction, image='', font=("Helvetica", ExperimentConstants.font_size), padx=10, pady=10)

    def display_thank_you(self):
        self.picture_label.config(text=ExperimentConstants.Thank_You, image='', font=("Helvetica", ExperimentConstants.font_size), padx=10, pady=10)

    def display_prompt(self, task_information):
        message = f"{task_information[InputFileIndexes.Task_Prompt_Index]} \n{ExperimentConstants.Prompt} "
        self.picture_label.config(text=message, image='', font=("Helvetica", ExperimentConstants.font_size), padx=10, pady=10)

    def display_table(self, task_information):
        self.controller.set_start_time_milliseconds(time.time() * 1000)
        img = Image.open(task_information[InputFileIndexes.Table_PNG_Index])
        img = img.resize((self.screen_width, self.screen_height), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)
        self.picture_label.config(image=self.photo, text='')

    def display_progress(self):
        self.controller.set_end_time_milliseconds(time.time() * 1000)
        progress_text = f"Completed {self.controller.get_counter()+1} out of 80 tasks" + "\n" + ExperimentConstants.Progress
        if self.controller.get_counter()== 15 or self.controller.get_counter()== 31 or self.controller.get_counter()== 47 or self.controller.get_counter()== 63:
            progress_text = progress_text + "\n\n" + ExperimentConstants.Next_task
        self.picture_label.config(text=progress_text, image='', font=("Helvetica", ExperimentConstants.font_size), padx=10, pady=10)

    def update_screen(self, event=None):
        if self.previous_counter < self.controller.get_counter():
            self.can_progress = True
            self.state = 0
            print("Counter updated, proccress and resume", self.state)
        
        if self.controller.get_counter() == 80:
            self.display_thank_you()
            return

        name_of_task = self.keys_list[self.controller.get_counter()]
        task_information = self.data_dictionary[name_of_task]

        if self.state == -1:
            self.display_intro_text()
        elif self.state == 0:
            self.display_prompt(task_information)
        elif self.state == 1:
            self.controller.start_tracking()
            self.controller.start_mouse_logging( name_of_task)
            self.display_table(task_information)
        elif self.state == 2:
            self.controller.stop_and_store_tracking()
            self.controller.stop_mouse_logging()
            self.display_progress()
            self.can_progress = False

        if self.can_progress:
            self.state = (self.state + 1) % 3

        self.previous_counter = self.controller.get_counter()
        if self.state == 0:
            self.controller.update_counter()
    