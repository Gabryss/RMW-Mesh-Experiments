import pandas as pd
import matplotlib.pyplot as plt
import argparse
import sys
import numpy as np
import os

class DataPlotter:
    def __init__(self, base_path='/mesh_exp/dataset/', use_run=False, run_size="KILO8", run_numbers=(3, 3, 3), plot_variances=True):
        self.display_columns = ['LAT_leo02','LONG_leo02','Ping_target_local', 'Delay_local']
        self.base_path = os.path.expanduser("~") + base_path
        self.plot_variances = plot_variances
        self.use_run = use_run
        self.run_size = run_size
        self.run_numbers = run_numbers
        self.fast_data_original = None
        self.fast_data_variance = None
        self.cyclone_data_original = None
        self.cyclone_data_variance = None
        self.zenoh_data_original = None
        self.zenoh_data_variance = None
        self.timestamps = None

    def load_data(self):
        if not self.use_run:
            file_path = f'{self.base_path}fast_clean/fast_clean_average.csv'
            self.fast_data_original = pd.read_csv(file_path)

            file_path_variance = f'{self.base_path}fast_clean/fast_clean_variance.csv'
            self.fast_data_variance = pd.read_csv(file_path_variance)

            file_path = f'{self.base_path}cyclone_clean/cyclone_clean_average.csv'
            self.cyclone_data_original = pd.read_csv(file_path)

            file_path_variance = f'{self.base_path}cyclone_clean/cyclone_clean_variance.csv'
            self.cyclone_data_variance = pd.read_csv(file_path_variance)

            file_path = f'{self.base_path}zenoh_clean/zenoh_clean_average.csv'
            self.zenoh_data_original = pd.read_csv(file_path)

            file_path_variance = f'{self.base_path}zenoh_clean/zenoh_clean_variance.csv'
            self.zenoh_data_variance = pd.read_csv(file_path_variance)
        else:
            fast_run_number, cyclone_run_number, zenoh_run_number = self.run_numbers

            file_path = f'{self.base_path}fast_clean/fast_{self.run_size}/fastrtps_{self.run_size}_exp_{fast_run_number}_resampled.csv'
            self.fast_data_original = pd.read_csv(file_path)

            file_path = f'{self.base_path}cyclone_clean/cyclone_{self.run_size}/cyclonedds_{self.run_size}_exp_{cyclone_run_number}_resampled.csv'
            self.cyclone_data_original = pd.read_csv(file_path)

            file_path = f'{self.base_path}zenoh_clean/zenoh_{self.run_size}/zenoh_{self.run_size}_exp_{zenoh_run_number}_resampled.csv'
            self.zenoh_data_original = pd.read_csv(file_path)

    #TO BE IMPROVED
    def extract_timestamp(self):
        self.timestamps_fast = self.fast_data_original['Timestamp']
        self.timestamps_cyclone = self.cyclone_data_original['Timestamp']
        self.timestamps_zenoh = self.zenoh_data_original['Timestamp']

    def plot_data(self):
        # Convert timestamps to numpy array
        timestamps_np_fast = self.timestamps_fast.to_numpy()
        timestamps_np_cyclone = self.timestamps_cyclone.to_numpy()
        timestamps_np_zenoh = self.timestamps_zenoh.to_numpy()

        # Initialize subplots
        num_plots = len(self.display_columns)-1
        fig, axs = plt.subplots(num_plots, 1, figsize=(12, 6 * num_plots))

        if not isinstance(axs, np.ndarray):
            axs = [axs]

        data_lat = self.fast_data_original['LAT_leo02'].to_numpy()
        data_long = self.fast_data_original['LONG_leo02'].to_numpy()
        data_lat = data_lat - data_lat[0]
        data_long = data_long - data_long[0]
        if self.plot_variances:
            variance_lat = self.fast_data_variance['LAT_leo02'].to_numpy()
            variance_long = self.fast_data_variance['LONG_leo02'].to_numpy()
            axs[0].fill_between(timestamps_np_fast, data_lat - variance_lat, data_lat + variance_lat, alpha=0.2)
            axs[0].fill_between(timestamps_np_fast, data_long - variance_long, data_long + variance_long, alpha=0.2)
        axs[0].plot(timestamps_np_fast, data_lat, label='lat leo02')
        axs[0].plot(timestamps_np_fast, data_long, label='long leo02')

        axs[0].set_ylabel("Pose")
        axs[0].legend()

        #Ping
        data_ping_fast = self.fast_data_original['Ping_target_local'].to_numpy()
        data_ping_cyclone = self.cyclone_data_original['Ping_target_local'].to_numpy()
        data_ping_zenoh = self.zenoh_data_original['Ping_target_local'].to_numpy()

        if self.plot_variances:
            variance_ping_fast = self.fast_data_variance['Ping_target_local'].to_numpy()
            variance_ping_cyclone = self.cyclone_data_variance['Ping_target_local'].to_numpy()
            variance_ping_zenoh = self.zenoh_data_variance['Ping_target_local'].to_numpy()

            axs[1].fill_between(timestamps_np_fast, data_ping_fast - variance_ping_fast, data_ping_fast + variance_ping_fast, alpha=0.2)
            axs[1].fill_between(timestamps_np_cyclone, data_ping_cyclone - variance_ping_cyclone, data_ping_cyclone + variance_ping_cyclone, alpha=0.2)
            axs[1].fill_between(timestamps_np_zenoh, data_ping_zenoh - variance_ping_zenoh, data_ping_zenoh + variance_ping_zenoh, alpha=0.2)
        axs[1].plot(timestamps_np_fast, data_ping_fast, 'b', label="Fast")
        axs[1].plot(timestamps_np_cyclone, data_ping_cyclone, 'r', label="Cyclone")
        axs[1].plot(timestamps_np_zenoh, data_ping_zenoh, 'g', label="Zenoh")

        axs[1].set_ylabel("Reachability")
        axs[1].legend()

        #Delay
        data_delay_fast = self.fast_data_original['Delay_local'].to_numpy()
        data_delay_cyclone = self.cyclone_data_original['Delay_local'].to_numpy()
        data_delay_zenoh = self.zenoh_data_original['Delay_local'].to_numpy()

        if self.plot_variances:
            variance_delay_fast = self.fast_data_variance['Delay_local'].to_numpy()
            variance_delay_cyclone = self.cyclone_data_variance['Delay_local'].to_numpy()
            variance_delay_zenoh = self.zenoh_data_variance['Delay_local'].to_numpy()

            axs[2].fill_between(timestamps_np_fast, data_delay_fast - variance_delay_fast, data_delay_fast + variance_delay_fast, alpha=0.2)
            axs[2].fill_between(timestamps_np_cyclone, data_delay_cyclone - variance_delay_cyclone, data_delay_cyclone + variance_delay_cyclone, alpha=0.2)
            axs[2].fill_between(timestamps_np_zenoh, data_delay_zenoh - variance_delay_zenoh, data_delay_zenoh + variance_delay_zenoh, alpha=0.2)
        axs[2].plot(timestamps_np_fast, data_delay_fast, 'b', label="Fast")
        axs[2].plot(timestamps_np_cyclone, data_delay_cyclone, 'r', label="Cyclone")
        axs[2].plot(timestamps_np_zenoh, data_delay_zenoh, 'g', label="Zenoh")

        axs[2].set_ylabel("Delay")
        axs[2].legend()

        plt.xlabel('Timestamp')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot data with variance from CSV files.')

    parser.add_argument('--use_run', action='store_true', help='Use run data instead of averaged data')
    parser.add_argument('--run_size', type=str, default="KILO8", help='Size of the run')
    parser.add_argument('--run_numbers', type=int, nargs=3, default=[3, 3, 3], help='Run numbers for Fast, Cyclone, and Zenoh')
    parser.add_argument('--plot_variances', action='store_true', help='Plot variances')

    args = parser.parse_args()

    plotter = DataPlotter(use_run=args.use_run, run_size=args.run_size, run_numbers=tuple(args.run_numbers), plot_variances=args.plot_variances)
    plotter.load_data()
    plotter.extract_timestamp()
    plotter.plot_data()
