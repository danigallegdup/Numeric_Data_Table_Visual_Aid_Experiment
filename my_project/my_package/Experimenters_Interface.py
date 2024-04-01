import csv
import threading
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime

from .Constants import *
from .Controller import *
from .Participants_Interface import *

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

        if task_information[InputFileIndexes.Task_Type_Index] == '3':
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
                   name_of_task, task_information[InputFileIndexes.Topic_Index], task_information[InputFileIndexes.Condition_Index],
                     task_information[InputFileIndexes.Task_Index], task_information[InputFileIndexes.Repetition_Index], 
                     task_information[InputFileIndexes.Table_PNG_Index], task_information[InputFileIndexes.Table_Rendering_Index], 
                     times_list[0], times_list[1], times_list[2], times_list[3], times_list[5], times_list[4], 
                     recorded, task_information[InputFileIndexes.Task_Column_Index], task_information[InputFileIndexes.Task_Answer_Col_Row_Index],
                     expected, task_information[InputFileIndexes.Task_Answer_Col_Row_Index], str(self.is_error), is_perfect, str(is_correct)]
        with open(OutputFilePaths.mainlog_file, 'a', newline='') as f:
            csv.writer(f).writerow(MainLog)
        self.saved_label.config(text=f"Saved: Expected: {expected}, Recorded: {recorded}, Correct: {is_correct}: Error: {self.is_error}")

    def load_csv_and_create_buttons(self, frame, file_path, recorded_var):
        csv_values = self.load_csv_content(file_path)
        for i, row in enumerate(csv_values):
            for j, value in enumerate(row):
                button = ttk.Button(frame, text=value, command=lambda v=value: recorded_var.set(v))
                button.grid(row=i, column=j)

    def create_label_and_picture(self, frame, task_information):
        prompt_label = tk.Label(frame, text=task_information[InputFileIndexes.Task_Prompt_Index])
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
        _, expected_var = self.create_entry(bottom_frame, textvariable=tk.StringVar(value=task_information[InputFileIndexes.Task_Expected_Index]), state='readonly', width=100, row=2, column=1)

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
        print(task_information[InputFileIndexes.Table_PNG_Index], self.controller.get_counter())

        recorded_var = tk.StringVar()  # Define recorded_var
        file_path = f'./Experiment_Data/Task_Answers_CSV/{task_information[InputFileIndexes.Task_Type_Index]}/{task_information[InputFileIndexes.Topic_Index]}.csv'
        self.load_csv_and_create_buttons(self.left_frame, file_path, recorded_var)
        self.create_label_and_picture(self.right_frame, task_information)
        self.task3_create_bottom_section(task_information, self.bottom_frame, recorded_var)  # Pass recorded_var to create_bottom_section
    
     
    def create_expected_answer(self, bottom_frame, task_information):
        expected_label = tk.Label(bottom_frame, text="Expected Answer:")
        expected_label.grid(row=0, column=0)
        expected_var = tk.StringVar(value=task_information[InputFileIndexes.Task_Expected_Index])
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

        file_path = f'./Experiment_Data/Task_Answers_CSV/{task_information[InputFileIndexes.Task_Type_Index]}/{task_information[InputFileIndexes.Topic_Index]}.csv'
        print(task_information[InputFileIndexes.Table_PNG_Index], self.controller.get_counter())
        self.root.title(name_of_task)
        
        self.load_csv_and_create_buttons(self.left_frame, file_path, self.recorded_var)
        self.create_label_and_picture(self.right_frame, task_information)
        self.create_bottom_section( task_information, self.bottom_frame, self.recorded_var)
