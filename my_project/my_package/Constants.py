import csv
import threading
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime

"""


"""

class ExperimentConstants:
    Introduction = "Thank you for participating in this experiment.\nPlease be patient and wait for the experimenter."
    Prompt = "\nPress the space bar as soon as you have found the answer and say the number out loud."
    Progress = "\nPlease do not use the mouse or keyboard\nAfter the experientor has finished recording your answer,\nyou will be able to proceed to the next task by pressing the space bar"
    Next_task = "You have finished all the conditions for this task!\nPlease take the survey that the experimentor will hand to you\n.You might want to take a short break before starting the next task."
    Thank_You = "Thank you for participating in this experiment.\nPlease remain in your seat and for your wait experimenter's response."

class ExperientCase:
    Experiment_Permutation = 1
    Participant_ID = 'A'

class InputFileIndexes:
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
  
task_information = [InputFileIndexes.Task_Type_Index, InputFileIndexes.Table_PNG_Index, InputFileIndexes.Table_Rendering_Index, 
                    InputFileIndexes.Dataset_Number_Index, InputFileIndexes.Topic_Index, InputFileIndexes.Condition_Index, InputFileIndexes.Repetition_Index, 
                    InputFileIndexes.Task_Type_Index, InputFileIndexes.Task_Header_Index, InputFileIndexes.Task_Column_Index, InputFileIndexes.Task_Par1_Index,
                    InputFileIndexes.Task_Prompt_Index, InputFileIndexes.Task_Expected_Index, InputFileIndexes.Task_Answer_Col_Row_Index]

class InputFilePaths:
    Task_CSV_Path = f'./Experiment_Data/Task_Answers_CSV/{task_information[InputFileIndexes.Task_Type_Index]}/{task_information[InputFileIndexes.Task_Type_Index]}.csv'
    Table_PNG_Path = f'{task_information[InputFileIndexes.Table_PNG_Index]}'

# Experient Case
Experiment_Permutation = 1
Participant_ID = 'A'

# Date and Time
Date_and_Time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

class OutputFilePaths:
    mainlog_file = F'./Experiment_Results/Experiment_permutation_{Experiment_Permutation}_participant_{Participant_ID}/EP{Experiment_Permutation}_P{Participant_ID}_Results/Mainlog_Experiment{Experiment_Permutation}_Participant{Participant_ID}_{Date_and_Time}.csv'
    mouse_log_path = F'./Experiment_Results/Experiment_permutation_{Experiment_Permutation}_participant_{Participant_ID}/EP{Experiment_Permutation}_P{Participant_ID}_Results/mouse_logs_EP{Experiment_Permutation}_P{Participant_ID}_/'
    gaze_log = "./gaze_log.csv"
    fixation_log = "./fixation_log.csv"

class MainlogIndexes:
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
    Recorded_row_col_Index = 18 # hard coded into.cvs file --> if Task_Answer_Col_Row_Index = 13 is a number == row
    Expected_Answer_Index = 19 # Task_Expected_Index = 12
    Expected_Answer_row_col_Index = 20 # Task_Answer_Col_Row_Index = 13 is anumber
    error_Index = 21 # False or True: button to set false in experimentors GUI
    Is_Perfect_Index = 22 # recored answer collected all data, can proceed to next task
    Is_correct_Index = 23 # True or False: whether the recorded answer was correct

class ParticipantConstants:
    font_size = 32
