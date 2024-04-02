import csv
import threading
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime

from my_package.Constants import *
from my_package.Participants_Interface import *
from my_package.Experimenters_Interface import *
from my_package.Controller import *


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

    with open(OutputFilePaths.mainlog_file, 'w', newline='') as f:
        csv.writer(f).writerow(variable_names)

def both_screen(data_dictionary):
    start_mainlog()
    controller = Controller()

    root = tk.Tk()
    root.geometry("1700x900")
    Experimenters_Interface(root, data_dictionary, controller)

    top = tk.Tk()
    top = tk.Toplevel(root)
    top.attributes("-fullscreen", True)
    Participants_Interface(top, data_dictionary, controller)

    root.mainloop()

if __name__ == "__main__":
    Experiment_Permutation = int(input("Input the experiment permutation: "))
    Participant_ID = input("Input the participant ID: ")

    # Experiment_Results\E1_A\ExperimentPermuation1_ParticipantA_Input.csv

    Input_File_Path = f'./Experiment_Results/Experiment_permutation_{Experiment_Permutation}_participant_{Participant_ID}/ExperimentPermuation{Experiment_Permutation}_Participant{Participant_ID}_Input.csv'

    data_dictionary = csv_to_row_dict(Input_File_Path)  # Convert CSV to dictionary
    both_screen(data_dictionary)
   