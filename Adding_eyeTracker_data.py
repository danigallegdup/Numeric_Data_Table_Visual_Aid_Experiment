from __future__ import division
from __future__ import print_function

import csv
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import datetime
from datetime import datetime
import time
import pyautogui
import threading

import sys
import os
import pylink


'''
Take in a parameter for the eye tracker: el_tracker = initialize_tracker()
into the Class Controller I want it to take in the eye tracker as a parameter
- start_Tacking_fixation()
- start_Tracking_saccade()
- stop_and_record_fixation()
- stop_and_record_saccade()

in the participants interface

change update_screen(self, task_information):
- call controller.start_Tacking_fixation()
- call controller.start_Tracking_saccade()
- call controller.stop_and_record_fixation()
- call controller.stop_and_record_saccade()


'''
#eye tracker Stuff
# Dummy mode flag - set to True if no real tracker is connected
dummy_mode = False


# for the participant to read
Introduction = "Thank you for participating in this experiment.\nPlease be patient and wait for the experimenter."
Prompt = "\nPress the space bar as soon as you have found the answer and say the number out loud."
Progress = "\nPlease do not use the mouse or keyboard\nAfter the experientor has finished recording your answer,\nyou will be able to proceed to the next task by pressing the space bar"
Next_task = "You have finished all the conditions for this task!\nPlease take the survey that the experimentor will hand to you\n.You might want to take a short break before starting the next task."
Thank_You = "Thank you for participating in this experiment.\nPlease remain in your seat and for your wait experimenter's response."

# Experient Case
Experiment_Permutation = 1
Participant_ID = 'A'

# input file indexs: 
Task_Type_Index = 0 # values are from 1 to 5
Table_PNG_Index = 1 # path to the table image
Table_Rendering_Index = 2 # 1-64 table id
Dataset_Number_Index = 3 # 1-16 different datasets
Topic_Index = 4 # anime, cereal, candy, movie
Condition_Index = 5 # color, zebra, plain, bar
Repetition_Index = 6 # 1-4  repetitions for each condition
Task_Index = 7 # Filter, Correlation, Sort, Estimate Average, Retrieve Value
Task_Header_Index = 8 # Task Header ("Episodes")
Task_Column_Index = 9 # Excel column of Task Header C == column 1
Task_Par1_Index = 10 # Parameter 1 - Value in Prompt- only for task 1 and 5
Task_Prompt_Index = 11 # What a participant is asked to do
Task_Expected_Index = 12 # Expected answer
Task_Answer_Col_Row_Index = 13 # column = Letter and row = number
task_information = [Task_Type_Index, Table_PNG_Index, Table_Rendering_Index, 
                    Dataset_Number_Index, Topic_Index, Condition_Index, Repetition_Index, 
                    Task_Type_Index, Task_Header_Index, Task_Column_Index, Task_Par1_Index,
                    Task_Prompt_Index, Task_Expected_Index, Task_Answer_Col_Row_Index]

# Date and Time
Date_and_Time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


# input files paths
Input_File_Path = f'./Experiment_Results/ExperimentPermuation{Experiment_Permutation}_Participant{Participant_ID}/ExperimentPermuation{Experiment_Permutation}_Participant{Participant_ID}_Input.csv'
Task_CSV_Path = f'./Experiment_Data/Task_Answers_CSV/{task_information[Task_Type_Index]}/{task_information[Task_Type_Index]}.csv'
Table_PNG_Path = f'{task_information[Table_PNG_Index]}'

# output files paths
mainlog_file = F'./Experiment_Results/Experiment_permutation_{Experiment_Permutation}_participant_{Participant_ID}/EP{Experiment_Permutation}_P{Participant_ID}_Results/Mainlog_Experiment{Experiment_Permutation}_Participant{Participant_ID}_{Date_and_Time}.csv'
mouse_log_path = F'./Experiment_Results/Experiment_permutation_{Experiment_Permutation}_participant_{Participant_ID}/EP{Experiment_Permutation}_P{Participant_ID}_Results/mouse_logs_EP{Experiment_Permutation}_P{Participant_ID}_/'
gaze_log = "./gaze_log.csv"
fixation_log = "./fixation_log.csv"

# Mainlog Indexes
Experiment_permutation_Index = 0 # Experiment_permutation
participant_ID_Index = 1 # Participant_ID
Task_iteration_Index = 2 #  (out of 80)
name_of_task_Index = 3 # anime-color-Filter-1
Topic_Index = 4 # anime, cereal, candy, movie
Condition_Index = 5 # color, zebra, plain, bar
Task_Index = 6 # Filter, Correlation, Sort, Estimate Average, Retrieve Value
Repetition_Index = 7 # 1-4  repetitions for each condition
table_png_Index = 8 # path to the table image
table_rendering_Index = 9 # 1-64 table id
start_time_Index = 10 # example: 01:30
end_time_Index = 11 # example: 01:31
start_time_e_Index = 12 # example: 1710361678258.4583
end_time_e_Index = 13 # exammple: 1710361679163.9875
start_time_t_Index = 14 # example:1710361677257.3555
time_spent_Index = 15 # example:  0.905529296875
Recorded_Answer_Index = 16 # from the participant in experimentors GUI
Prompt_col_Index = 17 # Task_Column_Index = 9
Recorded_row_col_Index = 18 # hard coded into .cvs file --> if Task_Answer_Col_Row_Index = 13 is a number == row
Expected_Answer_Index = 19 # Task_Expected_Index = 12
Expected_Answer_row_col_Index = 20 # Task_Answer_Col_Row_Index = 13 is a number
error_Index = 21 # False or True: button to set false in experimentors GUI
Is_Perfect_Index = 22 # recored answer collected all data, can proceed to next task
Is_correct_Index = 23 # True or False: whether the recorded answer was correct
MainLog = [Experiment_permutation_Index ,participant_ID_Index, Task_iteration_Index,
            name_of_task_Index, Topic_Index, Condition_Index, Task_Index, Repetition_Index,
            table_png_Index, table_rendering_Index, start_time_Index, end_time_Index, start_time_e_Index,
              end_time_e_Index, start_time_t_Index, time_spent_Index, Recorded_Answer_Index, Prompt_col_Index,
                Recorded_row_col_Index, Expected_Answer_Index, Expected_Answer_row_col_Index, 
                error_Index, Is_Perfect_Index, Is_correct_Index]

# Results
# line 46: 
# record = [name_of_task ,task_information[Task_Type_Index], task_information[Task_Prompt_Index], task_information[Table_PNG_Index], expected, recorded, str(is_correct)]


# Participants constants
font_size = 32

class Controller:
    def __init__(self,el_tracker):
        # INDEXES FOR BOTH GUI'S TO STAY IN SYNC
        self.current_index = -1
        self.experimentor_is_ready = False
        
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
        self.el_tracker = el_tracker

#eye tracker
    def start_tracking(self):
        # Start recording samples and events
        error = self.el_tracker.startRecording(1, 1, 1, 1)
        if error:
            return error

        # Begin real-time mode
        pylink.beginRealTimeMode(100)
    
    def stop_and_store_tracking(self):
        # End real-time mode
        pylink.endRealTimeMode()

        # Stop recording
        self.el_tracker.stopRecording()

        # Set the tracker to offline mode
        self.el_tracker.setOfflineMode()

        # Wait a bit for the tracker to switch to offline mode
        pylink.msecDelay(500)

        # Define the name of the EDF file on the Host PC
        edf_file_name = "TEST.EDF"

        # Define the directory where you want to store the data
        local_file_path = "./results"
        
        # Construct the full local file name including the path
        local_file_name = os.path.join(local_file_path, edf_file_name)

        # Transfer the file from the Host PC to your local machine
        try:
            # Make sure to provide the full file name, not just the directory
            self.el_tracker.receiveDataFile(edf_file_name, local_file_name)
        except RuntimeError as error:
            print('ERROR:', error)


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

    def start_mouse_logging(self):
        self.mouse_log_enabled = True
        self.mouse_log = []
        self.mouse_log_thread = threading.Thread(target=self.log_mouse_position)
        self.mouse_log_thread.start()

    def stop_mouse_logging(self, task_name):
        self.mouse_log_enabled = False
        if self.mouse_log_thread is not None:
            self.mouse_log_thread.join()
        self.save_mouse_log(task_name)

    def log_mouse_position(self):
        while self.mouse_log_enabled:
            position = pyautogui.position()
            self.mouse_log.append((datetime.now(), position))
            time.sleep(0.1)  # Log every 100 milliseconds
            self.save_mouse_log() # Save log to file

    def save_mouse_log(self, task_name):
        # Ensure the directory exists
        filename = task_name + mouse_log_path + f"mouse_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "X", "Y"])
            for log_entry in self.mouse_log:
                timestamp, position = log_entry
                writer.writerow([timestamp, position.x, position.y])

class Experimenters_Interface:
    def __init__(self, root, data_dictionary, controller):
        self.root = root
        self.data_dictionary = data_dictionary
        self.keys_list = list(data_dictionary.keys())
        self.controller = controller
        self.saved_label = None
        
        self.left_frame = self.create_frame(self.root, 850, 600)
        self.right_frame = self.create_frame(self.root, 850, 400)
        self.bottom_frame = self.create_frame(self.root, 1700, 200)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        self.bottom_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.recorded_var = tk.StringVar()  # Define recorded_var
        self.is_error = False

        self.next_task_button = ttk.Button(self.bottom_frame, text="Next Task", command=self.next_task)
        self.next_task_button.grid(row=4, column=6, columnspan=2)

        self.next_task()  # Start the first task    


    def Set_Error_True(self):
        self.is_error= True

    def Set_Error_False(self):
        self.is_error= False 

    def clear_frame(self, frame):
        # Destroy all children of frame
        for widget in frame.winfo_children():
            widget.destroy()

    def next_task(self):
        self.controller.experimentor_ready()
        current_index = self.controller.update_counter()
        self.controller.set_start_task_milliseconds(time.time() * 1000)
        if current_index > 79:
            return
        name_of_task = self.keys_list[current_index]
        task_information = self.data_dictionary[name_of_task]

        if task_information[Task_Type_Index] == '3':
            self.task3_setup_gui(name_of_task,task_information)
        else:    
            self.setup_gui(name_of_task,task_information)

    def load_csv_content(self, csv_file_path):
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            return [row for row in reader]

    def create_frame(self, root, width, height):
        frame = tk.Frame(root, width=width, height=height)
        return frame

    def save_answer(self, expected, recorded, override, task_information, name_of_task):
        times_list =self.controller.get_all_times()
        is_correct = (expected == recorded) or (expected == override)
        is_perfect = is_correct and not self.is_error
        MainLog = [Experiment_Permutation, Participant_ID, self.controller.get_counter(), 
                   name_of_task, task_information[Topic_Index], task_information[Condition_Index],
                     task_information[Task_Index], task_information[Repetition_Index], 
                     task_information[Table_PNG_Index], task_information[Table_Rendering_Index], 
                     times_list[0], times_list[1], times_list[2], times_list[3], times_list[5], times_list[4], 
                     recorded, task_information[Task_Column_Index], task_information[Task_Answer_Col_Row_Index],
                     expected, task_information[Task_Answer_Col_Row_Index], str(self.is_error), is_perfect, str(is_correct)]
        with open(mainlog_file, 'a', newline='') as f:
            csv.writer(f).writerow(MainLog)
        self.saved_label.config(text=f"Saved: Expected: {expected}, Recorded: {recorded}, Correct: {is_correct}: Error: {self.is_error}")

    def load_csv_and_create_buttons(self, frame, file_path, recorded_var):
        csv_values = self.load_csv_content(file_path)
        for i, row in enumerate(csv_values):
            for j, value in enumerate(row):
                button = ttk.Button(frame, text=value, command=lambda v=value: recorded_var.set(v))
                button.grid(row=i, column=j)

    def create_label_and_picture(self, frame, task_information):
        prompt_label = tk.Label(frame, text=task_information[Task_Prompt_Index])
        prompt_label.pack()
        img = Image.open(task_information[1])
        img.thumbnail((1300, 1300), Image.LANCZOS)  # Resize image to fit
        photo = ImageTk.PhotoImage(img)
        picture_label = tk.Label(frame, image=photo)
        picture_label.image = photo  # Keep a reference
        picture_label.pack()


    def create_label(self, frame, text, row, column):
        label = tk.Label(frame, text=text)
        label.grid(row=row, column=column)
        return label

    def create_entry(self, frame, textvariable=None, state=None, width=None, row=None, column=None):
        entry = tk.Entry(frame, textvariable=textvariable, state=state, width=width)
        entry.grid(row=row, column=column)
        return entry, textvariable

    def create_button(self, frame, text, command, row, column, columnspan=None):
        button = ttk.Button(frame, text=text, command=command)
        button.grid(row=row, column=column, columnspan=columnspan)

    def task3_create_bottom_section(self, task_information, bottom_frame, recorded_var):
        self.create_label(bottom_frame, "Recorded Answers:", 0, 0)

        _, recorded_var1 = self.create_entry(bottom_frame, textvariable=tk.StringVar(), width=30, row=0, column=1)
        _, recorded_var2 = self.create_entry(bottom_frame, textvariable=tk.StringVar(), width=30, row=0, column=2)
        _, recorded_var3 = self.create_entry(bottom_frame, textvariable=tk.StringVar(), width=30, row=0, column=3)

        button_command = lambda: recorded_var.set('-'.join([recorded_var1.get(), recorded_var2.get(), recorded_var3.get()]))
        self.create_button(bottom_frame, "Concatenate", button_command, 1, 0)

        self.create_entry(bottom_frame, textvariable=recorded_var, width=100, row=1, column=1)

        self.create_label(bottom_frame, "Expected Answer:", 2, 0)
        _, expected_var = self.create_entry(bottom_frame, textvariable=tk.StringVar(value=task_information[Task_Expected_Index]), state='readonly', width=100, row=2, column=1)

        self.create_label(bottom_frame, "Override Answer:", 3, 0)
        override_entry, _ = self.create_entry(bottom_frame, width=100, row=3, column=1)

        error_button = ttk.Button(bottom_frame, text="Error", command=self.Set_Error_True)
        error_button.grid(row=4, column=2)
        print(self.is_error)

        name_of_task = self.keys_list[self.controller.get_counter()]
        save_button_command = lambda: self.save_answer(expected_var.get(), override_entry.get() or recorded_var.get(), override_entry.get(),task_information, name_of_task)
        self.create_button(bottom_frame, "Save", save_button_command, 4, 0, columnspan=2)
       
        self.saved_label = self.create_label(bottom_frame, "Shows what was saved:", 5, 0)

        self.Set_Error_False()
        self.create_button(bottom_frame, "Next Task", self.next_task, 4, 6, columnspan=2)
        

    def task3_setup_gui(self,name_of_task,task_information):
        self.clear_frame(self.left_frame)
        self.clear_frame(self.right_frame)
        self.clear_frame(self.bottom_frame)

        self.root.title(name_of_task)
        print(task_information[Table_PNG_Index], self.controller.get_counter())

        recorded_var = tk.StringVar()  # Define recorded_var
        file_path = f'./Experiment_Data/Task_Answers_CSV/{task_information[Task_Type_Index]}/{task_information[Topic_Index]}.csv'
        self.load_csv_and_create_buttons(self.left_frame, file_path, recorded_var)
        self.create_label_and_picture(self.right_frame, task_information)
        self.task3_create_bottom_section(task_information, self.bottom_frame, recorded_var)  # Pass recorded_var to create_bottom_section
    
     
    def create_expected_answer(self, bottom_frame, task_information):
        expected_label = tk.Label(bottom_frame, text="Expected Answer:")
        expected_label.grid(row=0, column=0)
        expected_var = tk.StringVar(value=task_information[Task_Expected_Index])
        expected_entry = tk.Entry(bottom_frame, textvariable=expected_var, state='readonly', width=100)
        expected_entry.grid(row=0, column=1)
        return expected_var

    def create_recorded_answer(self, bottom_frame, recorded_var):
        recorded_label = tk.Label(bottom_frame, text="Recorded Answer:")
        recorded_label.grid(row=1, column=0)
        recorded_entry = tk.Entry(bottom_frame, textvariable=recorded_var,width=100)
        recorded_entry.grid(row=1, column=1)

    def create_override_answer(self, bottom_frame):
        override_label = tk.Label(bottom_frame, text="Override Answer:")
        override_label.grid(row=2, column=0)
        override_entry = tk.Entry(bottom_frame, width=100)
        override_entry.grid(row=2, column=1)
        return override_entry

    def create_error_button(self, bottom_frame):
        error_button = ttk.Button(bottom_frame, text="Error", command=self.Set_Error_True)
        error_button.grid(row=2, column=2)
        print(self.is_error)

    def create_save_button(self, bottom_frame, expected_var, override_entry, recorded_var, task_information):
        name_of_task = self.keys_list[self.controller.get_counter()]
        save_button = ttk.Button(bottom_frame, text="Save", command=lambda: self.save_answer(expected_var.get(), override_entry.get() or recorded_var.get(), override_entry.get(),task_information, name_of_task))
        save_button.grid(row=3, column=0, columnspan=2)

    def create_saved_label(self, bottom_frame):
        self.saved_label = tk.Label(bottom_frame, text="Shows what was saved:")
        self.saved_label.grid(row=4, column=0, columnspan=2)

    def create_next_button(self, bottom_frame):
        next_button = ttk.Button(bottom_frame, text="Next Task", command=self.next_task)
        next_button.grid(row=4, column=6, columnspan=2)

    def create_bottom_section(self, task_information, bottom_frame, recorded_var):
        expected_var = self.create_expected_answer(bottom_frame, task_information)
        self.create_recorded_answer(bottom_frame, recorded_var)
        override_entry = self.create_override_answer(bottom_frame)
        self.create_error_button(bottom_frame)
        self.create_save_button(bottom_frame, expected_var, override_entry, recorded_var, task_information)
        self.create_saved_label(bottom_frame)
        self.create_next_button(bottom_frame)
        self.Set_Error_False()

    def setup_gui(self, name_of_task,task_information):

        self.clear_frame(self.left_frame)
        self.clear_frame(self.right_frame)
        self.clear_frame(self.bottom_frame)

        file_path = f'./Experiment_Data/Task_Answers_CSV/{task_information[Task_Type_Index]}/{task_information[Topic_Index]}.csv'
        print(task_information[Table_PNG_Index], self.controller.get_counter())
        self.root.title(name_of_task)
        
        self.load_csv_and_create_buttons(self.left_frame, file_path, self.recorded_var)
        self.create_label_and_picture(self.right_frame, task_information)
        self.create_bottom_section( task_information, self.bottom_frame, self.recorded_var)

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
        self.picture_label.config(text=Introduction, image='', font=("Helvetica", font_size), padx=10, pady=10)

    def display_thank_you(self):
        self.picture_label.config(text=Thank_You, image='', font=("Helvetica", font_size), padx=10, pady=10)

    def display_prompt(self, task_information):
        message = f"{task_information[Task_Prompt_Index]} \n{Prompt} "
        self.picture_label.config(text=message, image='', font=("Helvetica", font_size), padx=10, pady=10)

    def display_table(self, task_information):
        self.controller.set_start_time_milliseconds(time.time() * 1000)
        img = Image.open(task_information[Table_PNG_Index])
        img = img.resize((self.screen_width, self.screen_height), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)
        self.picture_label.config(image=self.photo, text='')

    def display_progress(self):
        self.controller.set_end_time_milliseconds(time.time() * 1000)
        progress_text = f"Completed {self.controller.get_counter()+1} out of 80 tasks" + "\n" + Progress
        if(self.controller.get_counter()+1 % 16==0 and self.controller.get_counter() >1):
            progress_text = progress_text + "\n\n" + Next_task
        self.picture_label.config(text=progress_text, image='', font=("Helvetica", font_size), padx=10, pady=10)

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
            self.controller.start_mouse_logging()
            self.display_table(task_information)
        elif self.state == 2:
            self.controller.stop_mouse_logging(self.keys_list(self.controller.get_counter()))
            self.controller.stop_and_store_tracking()
            self.display_progress()
            self.can_progress = False

        if self.can_progress:
            self.state = (self.state + 1) % 3

        self.previous_counter = self.controller.get_counter()
        if self.state == 0:
            self.controller.update_counter()
    
    
# Function to convert CSV file to a dictionary
def csv_to_row_dict(csv_file_path):
    """Converts a CSV file into a dictionary with custom keys."""
    row_dict = {}
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Get the header row

        for row in reader:
            key = f"{row[headers.index('Topic')]}-{row[headers.index('Condition')]}-{row[headers.index('Task')]}-{row[headers.index('Repetition')]}"
            row_dict[key] = row
    return row_dict       

def start_mainlog():
    variable_names = ("Experiment_permutation", "participant_ID", "Task_iteration",
                  "name_of_task", "Topic", "Condition", "Task", "Repetition",
                  "table_png", "table_rendering", "start_time", "end_time", "start_time_e",
                  "end_time_e", "start_time_t", "time_spent", "Recorded_Answer", "Prompt_col",
                  "Recorded_row_col", "Expected_Answer", "Expected_Answer_row_col", 
                  "error", "isPerfect", "Is_correct")

    with open(mainlog_file, 'w', newline='') as f:
        csv.writer(f).writerow(variable_names)

def both_screen(data_dictionary, el_tracker):
    start_mainlog()
    controller = Controller(el_tracker)

    root = tk.Tk()
    root.geometry("1700x900")
    Experimenters_Interface(root, data_dictionary, controller)

    top = tk.Tk()
    top = tk.Toplevel(root)
    top.attributes("-fullscreen", True)
    Participants_Interface(top, data_dictionary, controller)

    root.mainloop()

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

def main():
    el_tracker = initialize_tracker()
    Experiment_Permutation = int(input("Input the experiment permutation: "))
    Participant_ID = input("Input the participant ID: ")

    # Experiment_Results\E1_A\ExperimentPermuation1_ParticipantA_Input.csv

    Input_File_Path = f'./Experiment_Results/Experiment_permutation_{Experiment_Permutation}_participant_{Participant_ID}/ExperimentPermuation{Experiment_Permutation}_Participant{Participant_ID}_Input.csv'

    data_dictionary = csv_to_row_dict(Input_File_Path)  # Convert CSV to dictionary
    both_screen(data_dictionary, el_tracker)

     # Cleanup
    if el_tracker is not None:
        el_tracker.close()


if __name__ == "__main__":
    main()
    
    
   