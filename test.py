"""
Decription / What it does:
This script is a Python-based graphical user interface (GUI) application designed
for conducting experiments. It displays tasks ( from CSV files)
to participants, records their responses, and manages the flow of tasks. The application
supports user interactions through a Tkinter-based GUI.

Authors: Written YongFeng J, Refactored by Daniela Gallegos Dupuis

Dependencies / How to Run:
python -m venv myenv   
myenv\Scripts\Activate.ps1
python test.py

 pip install pillow
 pip install pyautogui

prompted for the participants ID number
id # 1



- Python: Python 3.x is required.
- Libraries: Tkinter for the GUI, PIL for image handling, and pyautogui for automating GUI interactions.
- Running: Execute the script in a Python environment. Ensure all dependent libraries are installed.

How it works:  break this program down into 4 different parts 

Expandabilty:
1. To Add/Modify a Task:
Update the 1input.csv or modify the read_csv function to alter how tasks are read and presented.

2. Change Interface for Participant:
Modify the functions responsible for GUI rendering, such as show or update_image_on_panel, to change how information is presented to participants.

3. Change Interface for Experimenter:
Enhance or alter the secondary GUI window (root) to display different controls or information pertinent to the experimenter.

4. Where Results are Stored:
Results and data are stored in CSV files. The locations and formats are determined by functions like save_file and save_mouse.

Questions: 
    1. Where are the results stored?
    2. Experimentor and participants screen where are they, how are they configured

References for Debugging:


"""

"""
------------------------------------------------------------------------------------------
   Section 0:
   Everything related to GUI and mouse data
   Functions to display an image and accompanying table data on the panel   
------------------------------------------------------------------------------------------
"""


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



# Function to resize the label (not fully implemented in provided code)
def resize(ev=None)->None:
    """
    Resize the label. This function is currently not fully implemented.

    Args:
    ev (Event, optional): The event that triggers this function.
    """
    label.config(text='')

 
"""
------------------------------------------------------------------------------------------
   Section 1:
   Everything realated to what the trinkets Show
   Functions to display an image and accompanying table data on the panel   
------------------------------------------------------------------------------------------
"""
def update_image_on_panel(panel: Label, int: list_number, image_number, img: list) -> None:
    """
    Insert table data into the tree view.

    Args:
    table_path (str): The file path of the table data.
    headings (list): The list of headings for the table data.
    """
    photo = ImageTk.PhotoImage(Image.open(img[list_number][TABLE_PIC]).resize((top.winfo_width(), top.winfo_height())))
    label.config(text='')
    label.configure(image=photo)
    label.image =photo
    print(img[list_number][TABLE])

    if (image_number !=0):
            for widgets in frame.winfo_children():
              widgets.destroy()

    button2 = Button(frame,text ='save',width = 10,height = 5, command=lambda: save_file(img[list_number-1]))
    button2.pack(side= 'left')

def setup_tree_view(frame: Frame, headings: list) -> None:
    """
    Insert table data into the tree view.

    Args:
    table_path (str): The file path of the table data.
    headings (list): The list of headings for the table data.
    """
    global tree

    scrollbarx = Scrollbar(frame, orient=HORIZONTAL)
    scrollbary = Scrollbar(frame, orient=VERTICAL)
    tree = ttk.Treeview(frame, columns=(head_list[0] ,head_list[1],head_list[2],head_list[3] ,head_list[4],head_list[5],
        head_list[6] ,head_list[7],head_list[8],head_list[9] ,head_list[10],head_list[11]), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading(head_list[0], text=head_list[0], anchor=W)
    tree.heading(head_list[1], text=head_list[1], anchor=W)
    tree.heading(head_list[2], text=head_list[2], anchor=W)
    tree.heading(head_list[3], text=head_list[3], anchor=W)
    tree.heading(head_list[4], text=head_list[4], anchor=W)
    tree.heading(head_list[5], text=head_list[5], anchor=W)
    tree.heading(head_list[6], text=head_list[6], anchor=W)
    tree.heading(head_list[7], text=head_list[7], anchor=W)
    tree.heading(head_list[8], text=head_list[8], anchor=W)
    tree.heading(head_list[9], text=head_list[9], anchor=W)
    tree.heading(head_list[10], text=head_list[10], anchor=W)
    tree.heading(head_list[11], text=head_list[11], anchor=W)
    tree.bind('<ButtonRelease-1>', selectItem)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.pack()
    print(tree)

def insert_table_data_into_tree_view(table_path: str, head_list: list) -> None:
    """
    Insert table data into the tree view.

    Args:
    table_path (str): The file path of the table data.
    headings (list): The list of headings for the table data.
    """
    global tree
    global i
    i= 0

    with open(table_path) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            colum1 = row[head_list[0]]
            colum2 = row[head_list[1]]
            colum3 = row[head_list[2]]
            colum4 = row[head_list[3]]
            colum5 = row[head_list[4]]
            colum6 = row[head_list[5]]
            colum7 = row[head_list[6]]
            colum8 = row[head_list[7]]
            colum9 = row[head_list[8]]
            colum10 = row[head_list[9]]
            colum11 = row[head_list[10]]
            colum12 = row[head_list[11]]

            tree.insert("", i, iid=i+1, values=(colum1,colum2,colum3,colum4,colum5,colum6,colum7,colum8,colum9,colum10,colum11,colum12))
            i = i+1
        print(count)
    print(head_list)

def update_application_state() -> None:
    """
    Update the application state after displaying new data.
    """
    global image_number, count, list_number, is_image, paused, oldtime, start_time, i

    image_number += 1  # Increment the image_number
    count += 1         # Increment the count
    list_number += 1   # Move to the next item in the list
    i=i+1
    is_image = True    # Set the state to indicate an image is currently displayed
    paused = False     # Resume any paused process or timer
    oldtime = time()  # Reset the timer to current time
    run_timer()        # Start or restart the timer
    save_mouse()       # Call function to save mouse data or perform related actions
   
    print(start_time)

def show(panel: Label, img: list) -> None:
    """
    Updating Image and GUI Elements: 
    The function updates a label with a new image and possibly removes 
    old widgets from a frame.

    Setting Up a Tree View: It sets up a tree view to display table data. 
    This involves creating scrollbars, configuring columns, and binding a select event.

    Reading and Inserting Table Data: The function reads data from a CSV file
      and inserts it into the tree view.

    Managing State and Timing: It updates several global variables
      related to the state of the application and starts timers 
      for event handling.
  
    """
    global list_number,image_number, count, is_image, paused, oldtime, i, head_list 
    global tree, start_time, start_time_e, mouse_checker, start_mouse 
    
    start_mouse = 3813 #60 secs: 3813
    pyautogui.moveTo(33, 24)
    update_image_on_panel(panel, list_number, image_number, img)
   
    head_list = read_table(img)
    start_time = display2.cget('text')
    print(len(head_list))
    setup_tree_view(frame, head_list)

    start_time_e = (time())*1000
    mouse_checker = True
    table_path = img[list_number][TABLE]
    insert_table_data_into_tree_view( table_path , head_list)
    
    # increment: count, list_number, image_number, i
    update_application_state()
   
 
"""
------------------------------------------------------------------------------------------
    Section 2:
    handles file operations, UI updates, and task management.
------------------------------------------------------------------------------------------
""" 

def save_file(file: dict) -> None:
    """
    Save the participant's response and related data to a CSV file.

    Args:
    file (dict): A dictionary containing information about the current task.
    """
    global header, is_error
    print(str(True))
    file_handle = open("Results/1/result.csv", 'a')
    if(header == False):
        file_handle.write('participant ID'+','+'P_answer'+','+'start time'+','+'end time'+','+'start time_e'+','+'end time_e'+','+'start time_t'+','+'time spent'+','+'Task ID'+','+'trial'+','+'Repetition'+','+'Condition'+','+'Order of table'+','+'Correct Answer'+','+'col'+','+'row'+','+'Answer row'+','+'Answer column'+','+'error'+','+'isPerfect'+','+'ans_value'+'\n')
  
    for p in answer_list:
        file_handle.write(str(file[p_id])+','+str(p[0]) + ',' + str(start_time)+','+str(end_time)+','+str(start_time_e)+','+str(end_time_e)+','+str(start_time_t)+','+ str((end_time_e-start_time_e)/1000) + ','+ str(file[TASK_ID])+',' +str(file[mn]) +',' 
        + str(file[REP]) +','+ str(file[CONDITION]) +','+ str(file[ORDER]) +','+str(file[C_ANSWER])+','+str(col)+','+str(ro)+','+str(file[c_row])+','+str(file[c_col])+','+str(is_error)+','+str(str(p[0])==str(file[C_ANSWER]))+','+str(file[av])+'\n')
    
    file_handle.close()
    is_error = False
    header = True

def white(p: list) -> None:
    """
    Update the user interface based on the task's end condition.

    Args:
    p (list): List of task-related parameters.
    """
    global is_image, paused, end_time, end_time_e, mouse_checker

    mouse_checker = False
    if p[list_number-1][is_end]:
        label.config(image='')
        label.config(fg="blue",text=str(p[list_number-1][show_text]),font='Helvetica -35')
    else:
        label.config(image='')    
        label.config(fg="red",text="Please don't click or press on anything and wait for experimenter's response.",font='Helvetica -55')
      
    is_image = False
    paused = True
    end_time = display2.cget('text')
    end_time_e = (time())*1000

def save_mouse()-> None:
    """
    Save mouse position data at regular intervals.
    """
    global header_m
    global start_mouse 
    if mouse_checker == False:
        header_m = True
        return 

    else:
        global t
        if test_l[list_number-1][TYPE] == "Describing" and start_mouse <0:
            pyautogui.press("space")
                
        start_mouse -=1
        file_handle = open('Results/1/mouse/'+test_l[list_number-1][mn]+'-'+str(date.today())+'-'+str(start_time_e)+'.csv','a')
        if header_m == False:
            file_handle.write('trial'+','+'timestamp'+','+'x'+','+'y'+'\n')
        file_handle.write(str(test_l[list_number-1][mn])+','+str((time())*1000)+','+str(pyautogui.position().x)+','+str(pyautogui.position().y)+'\n')
        ##print(str(pyautogui.position()))
    
        t= threading.Timer(0.001, save_mouse)
        t.start()
        header_m = True
          
def wai_t()-> None:
    """
    Placeholder function to demonstrate a waiting period.
    """
    print("waiting")

def change_task(task)-> None:
    """
    Change the current task displayed to the user.

    Args:
    task (list): A list of tasks.
    """
    global test_l
    global count
    global list_number
    global tuple_number
    global oldtime2
    global start_time_t
    global t
    global header_m
    header_m = False
    #print(type(task[list_number][TASK_NAME]))

    start_time_t = (time())*1000
    display.config(text='00:00')
    label.config(image='')
    label.config(fg="black",text='\n'*10+str(task[list_number][TASK_NAME])+'\n'*20+test_l[list_number][TASK_ID],font='Helvetica -35')
    print(task[list_number][TASK_NAME])

    count = count +1
    print('aa')

def close()-> None:
    """
    Close the application window.
    """
    top.destroy()
    root.destroy()

def read_csv(filename: str) -> list:
    """
    Read data from a CSV file and return it as a list of tuples.

    Args:
    filename (str): The path to the CSV file.

    Returns:
    list: A list of tuples containing the data from the CSV file.
    """
    task_list =[]
    my_list = []
    with open(filename, newline='\n') as f:
        next(f)
        csv_reader = csv.reader(f)
        for row in csv_reader:
            print (str(row[TASK_NAME]))
            TN = row[TASK_NAME]
            TP = row[TABLE_PIC]
            T = row[TABLE]
            ID = row[TASK_ID]
            TYP = row[TYPE]
            REPE = row[REP]
            CON = row[CONDITION]
            ORD = row[ORDER]
            CANS = row[C_ANSWER]
            pid = row[p_id]
            crow = row[c_row]
            ccol = row[c_col]
            end = row[is_end]
            st = row[show_text]
            ans_value = row[av]
            mouse_name = row[mn]

            task_list.append((TN,TP,T,ID,TYP,REPE,CON,ORD,CANS,pid,crow,ccol,end,st,ans_value,mouse_name))

        #file_handle.close()

        print(my_list)
        
        return task_list

def go_back() -> None:
    """
    Navigate to the previous item in the sequence, adjusting the counters accordingly.
    This function is used to handle the case where the user needs to go back one step in the application flow.
    """
    global list_number
    global image_number
    global is_error
    list_number = list_number -1
    image_number = image_number -1
    is_error = True
    
def run_timer() -> None:
    """
    Continuously update a display element with the elapsed time since a starting point.
    This function uses recursion to update the timer every second.
    """

def run_timer2() -> None:
    """
    A secondary timer function similar to 'run_timer', but updates a different display element.
    This can be used for tracking a separate time interval or for displaying time in a different part of the UI.
    """
    delta = int(time() - oldtime2)
    #print('1')
    timestr = '{:02}:{:02}'.format(*divmod(delta, 60))
    display2.config(text=timestr)
    display2.after(1000, run_timer2)

def selectItem(event) -> None:
    """
    Handle the selection of an item in a tree view and update the application state based on the selection.

    Args:
    event: The event object containing details about the tree view item selection.
    """
    global col
    global ro
    curItem = tree.item(tree.focus())
    col = tree.identify_column(event.x)
    ro = tree.identify_row(event.y)
    print ('curItem = ', curItem)
    print ('col = ', col)
    print ('row = ', ro)
    global answer_list

    if col == '#0':
        cell_value = curItem['text']
    elif col == '#1':
        cell_value = curItem['values'][0]

    elif col == '#2':
        cell_value = curItem['values'][1]

    elif col == '#3':
        cell_value = curItem['values'][2]
    elif col == '#4':
        cell_value = curItem['values'][3]
    elif col == '#5':
        cell_value = curItem['values'][4]
    elif col == '#6':
        cell_value = curItem['values'][5]
    elif col == '#7':
        cell_value = curItem['values'][6]
    elif col == '#8':
        cell_value = curItem['values'][7]
    elif col == '#9':
        cell_value = curItem['values'][8]
    elif col == '#10':
        cell_value = curItem['values'][9]
    elif col == '#11':
        cell_value = curItem['values'][10]
    elif col == '#12':
        cell_value = curItem['values'][11]
        
    print('row:', curItem['values'])
    print ('cell_value = ', cell_value)
        
    answer_list = [(cell_value,display.cget('text'))]
        
def read_table(tablel: str) -> list:
    """
    Read the first line of a table from a file and return it as a list of words.

    Args:
    tablel (str): The file path of the table.

    Returns:
    list: A list of words (headers) from the first line of the table.
    """
    file_handle = open(tablel[list_number][TABLE],'r')
    for line in file_handle:
        line = line.rstrip()
        list_of_words = line.split(',')
        print(list_of_words)
        break

    return list_of_words


"""
Prompt the user to enter a participant's number.
This number is used to construct the file path for reading task data.
"""
file_path = input("Enter participant's ID number: ")

"""
Read task data from a CSV file named after the participant's number.
Initialize the main window (top) of the application and set it to fullscreen.
"""  
test_l = read_csv("Results/1/1input.csv")
top = Tk()
print(test_l)
top.attributes("-fullscreen", True)

"""
Setting Up Secondary GUI Window:
After some operations (not detailed in the script), adjust the geometry of the main window.
Create and configure a label to display a message to the participant.
"""    
top.geometry('2000x2000')
label=Label(top,fg="red",
        text="Thank you for your participation, please be patient and wait for experimenter's response.",
        wraplength=1000, font='Helvetica -55',justify=LEFT)
label.pack()
label.pack(fill=X, expand=1)
panel = Label(top)
panel.pack(side = "bottom", fill = "both", expand = "yes")

"""
Creating Additional GUI Elements:
Initialize a secondary window (root) for additional interface components.
Set up frames and labels for displaying information like time and saving status.
"""    
root = Tk()
root.title("Python - Import CSV File To Tkinter Table")
width = 100
height = 100
frame = Frame(root)
frame.pack(side="top", expand=True, fill="both")
frame2 = Frame(root)
frame2.pack(side="bottom", expand=True, fill="both")
display = Label(frame2, text='00:00', width=100)
display2 = Label(frame2, text='00:00', width=100)
display3 = Label(frame2, text='', width=100)
#display.pack(side="bottom")
f_save = Label(frame2, text='', width = 100)
f_save.pack(side="left")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
oldtime2 = time()
run_timer2()

root.geometry('2000x2000')
second=StringVar()
"""
Event Bindings and Window Protocols:
Bind keyboard events (Space and Tab) to specific functions for navigating through tasks.
Set protocols for handling window close events.
"""   
top.bind("<space>", lambda x:white(test_l) if(is_image) else (show(panel,test_l) if(count%2==0) else change_task(test_l)))
top.bind("<Tab>", lambda x :go_back())
top.protocol("WM_DELETE_WINDOW", close)
root.protocol("WM_DELETE_WINDOW", close)

"""
Start the Application's Event Loop:
The mainloop method is called to run the application. 
This method listens for events, such as button clicks or keypresses, 
and processes them as long as the application runs.
"""   
mainloop()



