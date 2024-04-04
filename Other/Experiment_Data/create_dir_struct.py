import os

# Define the base directory structure as nested dictionaries
experiment_structure = {
    'Experiment': {
        f'Experiment_permutation_{i:02}_participant_{chr(65+j)}': {
            'EP01_PA_ReadMe.md': None,
            'EP01_PA_input_file.csv': None,
            'EP01_PA_Results': {
                f'mainlog_EP01_PA_DATE_AND_TIME.csv': None,
                f'mouse_logs': {
                    f'uselog_TaskID_DATE_AND_TIME.csv': None
                },
                f'eye_movement_logs': {
                    f'movement_logs_TaskID_DATE_AND_TIME.csv': None
                },
                f'fixation_logs': {
                    f'fixation_log_TaskID_DATE_AND_TIME.csv': None
                }
            }
        } for i in range(1, 25) for j in range(0, (i % 24) + 1)
    },
    'start_experiment.py': None,
    'experiment_script.csv': None,
    'Tables_PNG': None,
    'Table_csv': None
}

# Define the path for the root of the structure to be created
# root_path = 'C:/Users/danig/OneDrive/Desktop/Actual_Experiment/'

# Function to recursively create directories and files
def create_structure(base_path, structure):
    for name, substructure in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(substructure, dict):  # It's a directory
            os.makedirs(path, exist_ok=True)
            create_structure(path, substructure)  # Recurse into the directory
        else:  # It's a file
            open(path, 'a').close()  # Create the file

# Create the entire directory structure
create_structure(root_path, experiment_structure)

# Return the path to the root of the structure as a confirmation
root_path
