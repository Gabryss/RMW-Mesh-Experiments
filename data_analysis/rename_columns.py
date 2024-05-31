import os
import sys
import pandas as pd
import glob

def rename_columns(folder_path, column_name_p):
    """
    Rename the first line (header) of each CSV file in the specified folder and its subfolders.
    """
    delay_files = glob.glob(os.path.join(folder_path, '**/*_delay.csv'), recursive=True)
    new_columns = column_name_p.strip().split(',')

    for fil in delay_files:
        df = pd.read_csv(fil)
        if len(df.columns) != len(new_columns):
            print(f"Skipping file {fil}: number of columns does not match.")
            continue
        df.columns = new_columns
        df.to_csv(fil, index=False)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <folder_path> <column_names>")
        sys.exit(1)

    folder_path = sys.argv[1]
    column_names = sys.argv[2]

    rename_columns(folder_path, column_names)
    print(f"Renamed columns in CSV files in folder: {folder_path}")
