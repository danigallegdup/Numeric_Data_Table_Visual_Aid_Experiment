import time
from tkinter import *
from PIL import Image, ImageTk
import csv
import tkinter.ttk as ttk
import os
import csv
from time import time,sleep

import pyautogui
import threading
from datetime import date
from threading import Timer

# Constants representing indices for various task properties
TASK_NAME = 0
TABLE_PIC = 1
TABLE = 2
TASK_ID = 3
TYPE = 4
REP = 5
CONDITION = 6
ORDER = 7
C_ANSWER = 8
p_id = 9
c_row = 10
c_col = 11
is_end = 12
show_text = 13
av = 14
mn = 15

# Global variables initialization
count = 1
image_number = 0
list_number = 0
tuple_number = 0
is_image = False
paused = True
answer_list = []
header = False
header_m = False
start_mouse = 1000
is_error = False

# Prompt for participant number and set as file path
file_path = input("Enter participants number: ")

# Function to resize the label (not fully implemented in provided code)
def resize(ev=None):
    label.config(text='')

# Function to display an image and accompanying table data on the panel
def show(panel, img):
    global image_number, count, list_number, tree, head_list, TableMargin
    global i, is_image, paused, oldtime, start_time, end_time
    global start_time_e, end_time_e, mouse_checker, start_mouse
    
    # Various global variables are updated and used here
    # Functionality includes displaying an image, setting up a table of data, handling button events, etc.

# Function to save participant's response to a CSV file
def save_file(file):
    global header, is_error
    # This function writes participant's responses along with other experiment data to a CSV file

# Function to handle the end of a task or a pause in the experiment
def white(p):
    global is_image, paused, end_time, end_time_e, mouse_checker
    # Updates the UI based on the task completion or pause
    #
# Function to continuously save mouse position data
def save_mouse():
    global header_m, start_mouse, t
    # Handles saving of mouse position data at regular intervals

# Function to wait for a set duration (function implementation not clear from provided code)
def wai_t():
    print("waiting")

# Function to change the current task in the experiment
def change_task(task):
    global test_l, count, list_number, tuple_number, oldtime2, start_time_t, t, header_m
    # Changes the task being displayed to the participant and resets relevant timers and counters

# Function to close the application
def close():
    top.destroy()
    root.destroy()

# Function to read a CSV file and return a list of tasks
def read_csv(filename):
    task_list = []
    with open(filename, newline='\n') as f:
        next(f)  # Skip header
        csv_reader = csv.reader(f)
        for row in csv_reader:
            task_list.append(tuple(row))
    return task_list

# Initialize the main application window
top = Tk()
top.attributes("-fullscreen", True)

# Read tasks from CSV file
test_l = read_csv(file_path + '/' + file_path + 'input.csv')

# Function to navigate back in the experiment sequence
def go_back():
    global list_number, image_number, is_error
    # Decrements the counters to go back to the previous state

# Set geometry and create main label for the top window
top.geometry('2000x2000')
label = Label(top, fg="red", text="Thank you for your participation...", font='Helvetica -55', justify=LEFT)
label.pack(fill=X, expand=1)
panel = Label(top)
panel.pack(side="bottom", fill="both", expand="yes")

# Function to run a timer for the experiment
def run_timer():
    global oldtime
    # Updates a label with the elapsed time since the start of the timer

# Function to run a secondary timer
def run_timer2():
    global oldtime2
    # Similar to run_timer but for a different label/display

# Function to handle item selection in a tree view
def selectItem(event):
    global col, ro, answer_list
    # Handles the logic when an item is selected from the tree view

# Function to read table headers from a file
def read_table(tablel):
    with open(tablel[list_number][TABLE], 'r') as file_handle:
        for line in file_handle:
            line = line.rstrip()
            list_of_words = line.split(',')
            return list_of_words

# Initialize the second window
root = Tk()
root.title("Python - Import CSV File To Tkinter Table")
root.geometry('2000x2000')

# Create frames and labels for displaying information
frame = Frame(root)
frame.pack(side="top", expand=True, fill="both")
frame2 = Frame(root)
frame2.pack(side="bottom", expand=True, fill="both")
display = Label(frame2, text='00:00', width=100)
display2 = Label(frame2)

display2 = Label(frame2, text='00:00', width=100)
display3 = Label(frame2, text='', width=100)
f_save = Label(frame2, text='', width=100)
f_save.pack(side="left")

# Set up screen dimensions for the root window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
oldtime2 = time()  # Initialize a timer for the root window
run_timer2()  # Start the timer

# Bind keyboard events for navigating through tasks and handling actions
top.bind("<space>", lambda x: white(test_l) if is_image else (show(panel, test_l) if (count % 2 == 0) else change_task(test_l)))
top.bind("<Tab>", lambda x: go_back())

# Set protocol for window close actions
top.protocol("WM_DELETE_WINDOW", close)  # Close both windows if one is closed
root.protocol("WM_DELETE_WINDOW", close)

# Start the main event loop of the application
mainloop()
