# Numeric Data Table Visual Aid Experiment

## Overview
This research experiemnt explores the effectiveness of using visual aids to understand  numeric data tables.

## Generated Data Tables: 
![color](./Experiment%20Data/Other/Generated%20Tables/anime.csv_color.png)

![bar](./Experiment%20Data/Other/Generated%20Tables/anime.csv_bar.png)

![zebra](./Experiment%20Data/Other/Generated%20Tables/anime.csv_zebra.png)

![plain](./Experiment%20Data/Other/Generated%20Tables/anime.csv_plain.png)


## Shortlisted Data Table Tasks:

From the list of tasks that were shortlisted and the table generating process that was covered last week. Here is a demo to figure all the tasks to help narrow down and finalize the experiment.

- Full document can be found here: 
[Click here to view the PDF](./ShortListed_Tasks.md)

### Task 1: Filter
- **Count the number of entries in the Y Column that exceed a value of X.**

### Task 2: Correlate
- **Determine which column amongst X, Y, and Z is positively correlated with Column A.**

### Task 3: Sort
- **Name the rows that are in the top 5 values in Column X in ascending order.**

### Task 4: Calculate
- **Calculate an estimation of the average value of entries in Column X.**

### Task 5: Retrieve Value
- **Find the anime with a value equal to X in the Y column.**

## Running the Experiment

### Important Files and Folders
- [test.py](./test.py): Main file for Running the experiment
- [EyeTrackerHandler.py](./EyeTrackerHandler.py): supporting class incharge of eye Tracker
- [Results](./Results/): input file and results of each participant 
- [Exeriment_Data](./Experiment%20Data/):Find Tables used int the experiment


### Dependencies\How to Run:
- Python: Python 3.x is required.
- Libraries: Tkinter for the GUI, PIL for image handling, and pyautogui for automating GUI interactions.
- Running: Execute the script in a Python environment. Ensure all dependent libraries are installed.

```bash
python -m venv myenv   
myenv\Scripts\Activate.ps1

pip install pillow
pip install pyautogui

python test.py
Enter participant's ID number: 1