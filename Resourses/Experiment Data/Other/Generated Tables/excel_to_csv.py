import pandas as pd

# Assuming the Excel file is named 'candy_data.xlsx'
excel_file_path = 'anime.xlsx'
csv_file_path = 'anime_new.csv'

# Read the Excel file from a specific sheet named 's2_plain'
df = pd.read_excel(excel_file_path, sheet_name='s2_plain')

# Define the column names in the desired order
column_names = [
    'Row', 'Candy Name', 'Chocolate', 'Fruity', 'Caramel', 'Almond', 'Nougat',
    'Hard', 'Bar', 'Pluribus', 'SugarPercent', 'Rating', 'Price'
]

# Ensure the dataframe has the correct column names in case they're different in the Excel file
# If the data already includes 'Row' as the first column, you can comment out the next line that generates it
# df['Row'] = range(len(df))

# Write the DataFrame to a CSV file
df.to_csv(csv_file_path, index=False, columns=column_names)

print(f'CSV file has been created at {csv_file_path}')
