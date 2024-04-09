"""

This Program takes in asc file as an argument when called
example: python Parse_to_task_log.py PilotMe.asc

1) find all the task starting messages: anime-color-Filter-1

2) find all ending messages:_anime-color-Filter-1

3) create a file adding everything that inbetween those lines: anime-color-Filter-1_eye_tacking.csv 

Here is the list of all the task names:
1) anime-color-Filter-1
2) anime-color-Filter-2
3) anime-color-Filter-3
4) anime-color-Filter-4


"""


with open('PilotMe.asc', 'r') as file:
    for line in file:
        # Split the line into parts
        parts = line.split()

        # Check if the line has the correct number of parts
        if len(parts) == 5:
            # Parse the parts
            timestamp = int(parts[0])
            x = float(parts[1])
            y = float(parts[2])
            z = float(parts[3])
            value = float(parts[4])

            # Do something with the parsed values
            print(timestamp, x, y, z, value)

        elif len(parts) > 1 and parts[0] == 'MSG':
            # This is a message line
            timestamp = int(parts[1])
            message = ' '.join(parts[2:])

            # Do something with the timestamp and message
            print(timestamp, message)