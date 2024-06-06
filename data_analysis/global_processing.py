import sys
import os
from Concatenate_data import CSVFileMerger
from size_average_variance import SizeAverageVar
from rmw_average_variance import RMWAverageVar
from rename_columns import rename_columns

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 global_processing.py <folder_path> ")
        sys.exit(1)

    folder_path = sys.argv[1]
    subfolders = [f.path for f in os.scandir(folder_path) if f.is_dir()]
    
    rename_columns(folder_path, "Timestamp,Delay,Size")
    print(f"Renamed columns in CSV files in folder: {folder_path}")

    
    for subfolder in subfolders:
        

        #Merging each run in one file
        merger = CSVFileMerger(subfolder)
        merger.merge_files()
        print(f"Merged files in folder: {subfolder}")
        #Getting the average per message size
        size_processor = SizeAverageVar(subfolder)
        size_processor.create_simple_average_and_variance_csv()
        print(f"Created average and variance files in folder: {subfolder}")


    #Getting the average per RMW
    rmw_processor = RMWAverageVar(folder_path)
    rmw_processor.create_simple_average_and_variance_csv()
    print(f"Created average and variance files in folder: {folder_path}")
