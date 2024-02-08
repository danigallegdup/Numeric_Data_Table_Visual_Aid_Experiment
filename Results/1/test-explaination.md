 # GUI-Based Experiment/Survey Application

## Introduction
This Python-based GUI application is designed for conducting experiments or surveys. It displays tasks (from CSV files) to participants, records their responses, and manages the flow of tasks. The application features a Tkinter-based GUI, PIL for image handling, and pyautogui for automating GUI interactions.

## Key Features
- Displays images and accompanying table data on a panel.
- Supports user interactions through a Tkinter-based GUI.
- Records participant responses and related data to CSV files.
- Manages the flow of tasks and updates the application state accordingly.

## Step-by-Step Explanation
### 1. Importing Necessary Libraries
```python
import tkinter as tk
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
```

### 2. Global Variables and Constants
```python
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
```

### 3. GUI and Mouse Data Functions
#### 3.1 Resize Function (Not Fully Implemented)
```python
def resize(ev=None):
    """
    Resize the label. This function is currently not fully implemented.

    Args:
    ev (Event, optional): The event that triggers this function.
    """
    label.config(text='')
```

#### 3.2 Update Image on Panel Function
```python
def update_image_on_panel(panel: Label, int: list_number, image_number, img: list) -> None:
    """
    Insert table data into the tree view.

    Args:
    table_path (str): The file path of the table data.
    headings (list): The list of headings for the table data.
    """
    photo = ImageTk.PhotoImage(Image.open(img[list_number][TABLE_PIC]).resize((top.winfo_width(), top.winfo_height())))
    label.

