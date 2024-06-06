import os
import pandas as pd
import numpy as np
import glob

class CSVFileMerger:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def find_matching_files(self, suffixes):
        # Create a dictionary to hold the groups of matching files
        matching_files = {}
        # List all files in the directory
        #files = os.listdir(self.folder_path)
        files = glob.glob(os.path.join(self.folder_path, '**/*.csv'), recursive=True)
        # Iterate over each file
        for file in files:
            # Check if the file ends with any of the specified suffixes
            for suffix in suffixes:
                if file.endswith(suffix):
                    # Extract the prefix (common part of the filename)
                    prefix = file.split(suffix)[0]
                    # Add the file to the corresponding group in the dictionary
                    if prefix not in matching_files:
                        matching_files[prefix] = {s: '' for s in suffixes}
                    matching_files[prefix][suffix] = file
                    break
        return matching_files

    def merge_files(self):
        # Define the suffixes for the files to be merged
        suffixes = ['_leo02_global_monitoring.csv', '_local_delay.csv', '_local_global_monitoring.csv']
        # Find all matching files
        matching_files = self.find_matching_files(suffixes)

        robot_names = {
        '_leo02_global_monitoring.csv': '_leo02',
        '_local_delay.csv': '_local',
        '_local_global_monitoring.csv': '_local'
        }
        
            # Iterate over each group of matching files
        for prefix, files_dict in matching_files.items():
            # Check if there are exactly three files in the group
            if all(files_dict.values()):
                # Read the first file
                merged_df = pd.read_csv(os.path.join(self.folder_path, files_dict[suffixes[0]]))
                # Rename columns with the robot name suffix
                merged_df.columns = [col if col == 'Timestamp' else col + robot_names[suffixes[0]] for col in merged_df.columns]
                
                # Merge the remaining files
                for suffix in suffixes[1:]:
                    df = pd.read_csv(os.path.join(self.folder_path, files_dict[suffix]))
                    # Rename columns with the robot name suffix
                    df.columns = [col if col == 'Timestamp' else col + robot_names[suffix] for col in df.columns]
                    # Merge with the main dataframe
                    merged_df = merged_df.merge(df, on='Timestamp', how='outer')
                
                # Save the merged dataframe to a new CSV file
                merged_filename = f"{prefix}_merged.csv"
                merged_df.to_csv(os.path.join(self.folder_path, merged_filename), index=False)
                print(f"Merged file saved as {merged_filename}")
                # Resample the data by second and calculate the mean for each second
                resampled_filename = f"{prefix}_resampled.csv"
                self.resampling_to_sec(merged_df, resampled_filename)

            else:
                # If there are not exactly three files, print a message
                print(f"Could not find a complete set of files for prefix '{prefix}'")

    def resampling_to_sec(self, data, output_file_path):
        # Convert the 'Timestamp' column to datetime format
        data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='ms')

        # Resample the data by second and calculate the mean for each second
        data.set_index('Timestamp', inplace=True)
        resampled_data = data.resample('s').mean()

        # Preserve NaNs in seconds where no data is available
        resampled_data = resampled_data.replace({0: np.nan})

        # Before saving, replace all the NaN of Ping_target_local with 0
        resampled_data['Ping_target_local'] = resampled_data['Ping_target_local'].fillna(0)

        # Convert the index to integer seconds since epoch
        resampled_data.index = (resampled_data.index - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

        resampled_data.to_csv(output_file_path)

   