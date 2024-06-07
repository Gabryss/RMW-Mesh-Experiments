import pandas as pd
import matplotlib.pyplot as plt
import argparse
import sys
import numpy as np
import os

class DataPlotter:
    def __init__(self,rmw, base_path='/mesh_exp/dataset/', use_run=False, run_size="KILO8", run_number=3, plot_variances=True):
        self.rmw = rmw
        if self.rmw == "fast":
            self.prefix = "fastrtps"
        elif self.rmw == "cyclone":
            self.prefix = "cyclonedds"
        elif self.rmw == "zenoh":
            self.prefix = "zenoh"
        self.display_columns = ['LAT_leo02','LONG_leo02','Ping_target_local', 'Delay_local']
        self.base_path = os.path.expanduser("~") + base_path
        self.plot_variances = plot_variances
        self.use_run = use_run
        self.run_size = run_size
        self.run_numbers = run_number
        self.data_original = None
        self.data_variance = None
        self.cyclone_data_original = None
        self.cyclone_data_variance = None
        self.zenoh_data_original = None
        self.zenoh_data_variance = None
        self.timestamps = None

    def load_data(self):
        if not self.use_run:
            file_path = f'./data/Cleaned/{self.rmw}/{self.prefix}_average.csv'
            self.data_original = pd.read_csv(file_path)

            file_path_variance = f'./data/Cleaned/{self.rmw}/{self.prefix}_variance.csv'
            self.data_variance = pd.read_csv(file_path_variance)

        else:
            file_path = f'{self.base_path}{self.rmw}_clean/{self.rmw}_{self.run_size}/{self.prefix}_{self.run_size}_exp_{self.run_numbers}_resampled.csv'
            self.data_original = pd.read_csv(file_path)

    #TO BE IMPROVED
    def extract_timestamp(self):
        self.timestamps = self.data_original['Timestamp']

    def plot_data(self):
        # Convert timestamps to numpy array
        timestamps_np = self.timestamps.to_numpy()

        # Initialize subplots
        num_plots = len(self.display_columns)-1
        fig, axs = plt.subplots(num_plots, 1, figsize=(12, 6 * num_plots))

        if not isinstance(axs, np.ndarray):
            axs = [axs]

        data_lat = self.data_original['LAT_leo02'].to_numpy()
        data_long = self.data_original['LONG_leo02'].to_numpy()
        data_lat = data_lat - data_lat[0]
        data_long = data_long - data_long[0]
        if self.plot_variances:
            variance_lat = self.data_variance['LAT_leo02'].to_numpy()
            variance_long = self.data_variance['LONG_leo02'].to_numpy()
            axs[0].fill_between(timestamps_np, data_lat - variance_lat, data_lat + variance_lat, alpha=0.2)
            axs[0].fill_between(timestamps_np, data_long - variance_long, data_long + variance_long, alpha=0.2)
        axs[0].plot(timestamps_np, data_lat, label='lat leo02')
        axs[0].plot(timestamps_np, data_long, label='long leo02')

        axs[0].set_ylabel("Pose")
        axs[0].legend()

        #Ping
        data_ping = self.data_original['Ping_target_local'].to_numpy()

        if self.plot_variances:
            variance_ping = self.data_variance['Ping_target_local'].to_numpy()

            axs[1].fill_between(timestamps_np, data_ping - variance_ping, data_ping + variance_ping, alpha=0.2)
           
        axs[1].plot(timestamps_np, data_ping, 'b', label="Reachability")


        axs[1].set_ylabel("Reachability")
        axs[1].legend()

        #Delay
        data_delay = self.data_original['Delay_local'].to_numpy()

        if self.plot_variances:
            variance_delay = self.data_variance['Delay_local'].to_numpy()

            axs[2].fill_between(timestamps_np, data_delay - variance_delay, data_delay + variance_delay, alpha=0.2)
            
        axs[2].plot(timestamps_np, data_delay, 'b', label="Delay")


        axs[2].set_ylabel("Delay")
        axs[2].legend()

        plt.xlabel('Timestamp')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot data with variance from CSV files.')
    parser.add_argument('rmw', type=str, help='RMW to plot')
    parser.add_argument('--use_run', action='store_true', help='Use run data instead of averaged data')
    parser.add_argument('--run_size', type=str, default="KILO8", help='Size of the run')
    parser.add_argument('--run_number', type=int, default=3, help='Run numbers for the RMW')
    parser.add_argument('--plot_variances', action='store_true', help='Plot variances')

    args = parser.parse_args()

    plotter = DataPlotter(args.rmw,use_run=args.use_run, run_size=args.run_size, run_number=args.run_number, plot_variances=args.plot_variances)
    plotter.load_data()
    plotter.extract_timestamp()
    plotter.plot_data()
