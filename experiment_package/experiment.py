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

"""
Writen by: Daniela Gallegos Dupuis

"""

from my_package.Constants import *
from my_package.Participants_Interface import *
from my_package.Experimenters_Interface import *
from my_package.Controller import *
from my_package.eyetracker import *


# Function to convert CSV file to a dictionary
def csv_to_row_dict(csv_file_path: str) -> dict:
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
    variable_names = ("Experiment_permutation", "participant_ID", "Task_Trial",
                  "Name_of_Task", "Task_Type", "Table_PNG", "Table_Rendering", "Dataset_Number",
                  "Topic", "Condition", "Repetition", "Task" ,  "Task_Header", "Task_Column", "Task_Par1",
                  "Task_Prompt", "Task_Expected_Answer", "Task_Answer_Col_Row", 
                  "Start_time", "End_time", "Start_time_e", "End_time_e", "Start_time_Prompt", "Time_Spent",
                 "Recorded_Answer", "IsError", "IsPerfect", "IsCorrect")

    with open(OutputFilePaths.mainlog_file, 'w', newline='') as f:
        csv.writer(f).writerow(variable_names)

def both_screen(data_dictionary, eye_tracker):
    start_mainlog()
    controller = Controller(eye_tracker)

    root = tk.Tk()
    root.geometry("1700x900")
    Experimenters_Interface(root, data_dictionary, controller)

    top = tk.Toplevel(root)
    top.attributes("-fullscreen", True)
    Participants_Interface(top, data_dictionary, controller)

    root.mainloop()

if __name__ == "__main__":
    eye_tracker = EyeTracker()
    eye_tracker.initialize_tracker()
    
    Experiment_Permutation = int(input("Input the experiment permutation: "))
    Participant_ID = input("Input the participant ID: ")
   
    # Experiment_Results\E1_A\ExperimentPermuation1_ParticipantA_Input.csv

    Input_File_Path = f'./Results/EP{Experiment_Permutation}_P{Participant_ID}/ExperimentPermuation{Experiment_Permutation}_Participant{Participant_ID}_Input.csv'
    data_dictionary = csv_to_row_dict(Input_File_Path)  # Convert CSV to dictionary
    
    both_screen(data_dictionary, eye_tracker)
    
    
    eye_tracker.close_eye_tracker()
    sys.exit()
   