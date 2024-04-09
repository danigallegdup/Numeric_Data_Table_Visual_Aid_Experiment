"""

This Program takes in asc file as an argument when called
example: python Parse_to_task_log.py PilotMe.asc

for each task
- create a file named after the task name ei: anime-color-Filter-1_eye_tacking.csv
- add 3 lines of the asc file to the csv file starting at the first instance of the task name
- print out how many times the task name appears in the file 



for each task
- create a file named after the task name ei: anime-color-Filter-1_eye_tacking.csv
- find the first instance where the task name appears in the asc file
- add eveything from that line until the third time the file name appars 


"""

def get_task_dictionary():
    task_names = """
    anime-color-Filter-1  
    anime-color-Filter-2  
    anime-color-Filter-3  
    anime-color-Filter-4  
    cereal-zebra-Filter-1  
    cereal-zebra-Filter-2  
    cereal-zebra-Filter-3  
    cereal-zebra-Filter-4  
    candy-plain-Filter-1  
    candy-plain-Filter-2  
    candy-plain-Filter-3  
    candy-plain-Filter-4  
    movie-bar-Filter-1  
    movie-bar-Filter-2  
    movie-bar-Filter-3  
    movie-bar-Filter-4  
    anime-color-Correlation-1  
    anime-color-Correlation-2  
    anime-color-Correlation-3  
    anime-color-Correlation-4  
    cereal-zebra-Correlation-1  
    cereal-zebra-Correlation-2  
    cereal-zebra-Correlation-3  
    cereal-zebra-Correlation-4  
    candy-plain-Correlation-1  
    candy-plain-Correlation-2  
    candy-plain-Correlation-3  
    candy-plain-Correlation-4  
    movie-bar-Correlation-1  
    movie-bar-Correlation-2  
    movie-bar-Correlation-3  
    movie-bar-Correlation-4  
    anime-color-Sort-1  
    anime-color-Sort-2  
    anime-color-Sort-3  
    anime-color-Sort-4  
    cereal-zebra-Sort-1  
    cereal-zebra-Sort-2  
    cereal-zebra-Sort-3  
    cereal-zebra-Sort-4  
    candy-plain-Sort-1  
    candy-plain-Sort-2  
    candy-plain-Sort-3  
    candy-plain-Sort-4  
    movie-bar-Sort-1  
    movie-bar-Sort-2  
    movie-bar-Sort-3  
    movie-bar-Sort-4  
    anime-color-Estimate Average-1  
    anime-color-Estimate Average-2  
    anime-color-Estimate Average-3  
    anime-color-Estimate Average-4  
    cereal-zebra-Estimate Average-1  
    cereal-zebra-Estimate Average-2  
    cereal-zebra-Estimate Average-3  
    cereal-zebra-Estimate Average-4  
    candy-plain-Estimate Average-1  
    candy-plain-Estimate Average-2  
    candy-plain-Estimate Average-3  
    candy-plain-Estimate Average-4  
    movie-bar-Estimate Average-1  
    movie-bar-Estimate Average-2  
    movie-bar-Estimate Average-3  
    movie-bar-Estimate Average-4  
    anime-color-Retrieve Value-1  
    anime-color-Retrieve Value-2  
    anime-color-Retrieve Value-3  
    anime-color-Retrieve Value-4  
    cereal-zebra-Retrieve Value-1  
    cereal-zebra-Retrieve Value-2  
    cereal-zebra-Retrieve Value-3  
    cereal-zebra-Retrieve Value-4  
    candy-plain-Retrieve Value-1  
    candy-plain-Retrieve Value-2  
    candy-plain-Retrieve Value-3  
    candy-plain-Retrieve Value-4  
    movie-bar-Retrieve Value-1  
    movie-bar-Retrieve Value-2  
    movie-bar-Retrieve Value-3  
    movie-bar-Retrieve Value-4  
    """

    # Split the task names into a list
    task_names = task_names.split('\n')

    # Create a dictionary with task names as keys and True as values
    task_dictionary = {name.strip(): True for name in task_names}

    return task_dictionary

def main():
    task_dictionary = get_task_dictionary()

    # experiment_package\Results\EP1_PA\EP1_PA_Results\eyetracker_log
    file_path = "../eyetracker_log/"


    for task in task_dictionary:
        with open('PilotMe.asc', 'r') as file:
            lines = file.readlines()

        first_occurrence = None
        last_occurrence = None
        for i, line in enumerate(lines):
            if task in line:
                if first_occurrence is None:
                    first_occurrence = i + 1  # Line numbers start at 1
                last_occurrence = i + 1
        
        if first_occurrence is not None and last_occurrence is not None:
            with open(f'{file_path}{task}_eye_tracking.csv', 'w') as file:
                for line in lines[first_occurrence:last_occurrence+1]:
                    line = line.replace('\t', ', ')
                    file.write(line)

        if first_occurrence and last_occurrence:
            print(f'Task {task} first appears on line {first_occurrence} and last appears on line {last_occurrence}')

    


if __name__ == "__main__":
    main()