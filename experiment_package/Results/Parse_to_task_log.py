"""

This Program takes in asc file as an argument when called
example: python Parse_to_task_log.py PilotMe.asc

1) find all the task starting messages: anime-color-Filter-1

2) find all ending messages:_anime-color-Filter-1

3) create a file adding everything that inbetween those lines: anime-color-Filter-1_eye_tacking.csv 

Here is the list of all the task names start message:
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
    task_names = task_names.split()

    # Create a dictionary with task names as keys and True as values
    task_dictionary = {name: True for name in task_names}

    return task_dictionary

def main():
    task_dictionary = get_task_dictionary()
    if 'anime-color-Filter-1' in task_dictionary:
        print('Task name exists in the dictionary')

    # with open('PilotMe.asc', 'r') as file:
    #     for line in file:
    #         # Split the line into parts
    #         parts = line.split()

    #         # Check if the line has the correct number of parts
    #         if len(parts) == 5:
    #             # Parse the parts
    #             timestamp = int(parts[0])
    #             x = float(parts[1])
    #             y = float(parts[2])
    #             z = float(parts[3])
    #             value = float(parts[4])

    #             # Do something with the parsed values
    #             print(timestamp, x, y, z, value)

if __name__ == "__main__":
    main()