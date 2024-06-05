import pandas as pd
import matplotlib.pyplot as plt
import argparse
import sys
import numpy as np

class DataPlotter:
    """
    Class very close from the plot_one_file_with_variance.py script, but showing exactly the graphs as we want
    """
    def __init__(self, rmw, prefix, base_path='/home/lchovet/mesh_exp/dataset/'):
        self.rmw = rmw
        self.prefix = prefix
        self.display_columns = ['LAT_leo02','LONG_leo02','Delay_local', 'Bytes_Send_leo02']
        self.base_path = base_path
        self.plot_variances = False
        self.data_original = None
        self.data_variance = None
        self.timestamps = None

    def load_data(self):
        file_path = f'{self.base_path}{self.rmw}_clean/{self.prefix}_average.csv'
        self.data_original = pd.read_csv(file_path)

        file_path_variance = f'{self.base_path}{self.rmw}_clean/{self.prefix}_variance.csv'
        self.data_variance = pd.read_csv(file_path_variance)

    def extract_and_interpolate(self):
        self.timestamps = self.data_original['Timestamp']

        for column in self.display_columns:
            self.data_original[column] = self.data_original[column].interpolate()
            self.data_variance[column] = self.data_variance[column].interpolate()

    def plot_data(self):
        # Convert timestamps to numpy array
        timestamps_np = self.timestamps.to_numpy()

        # Initialize subplots
        num_plots = len(self.display_columns)
        fig, axs = plt.subplots(num_plots, 1, figsize=(12, 6 * num_plots))

        if not isinstance(axs, np.ndarray):
            axs = [axs]

        # Plot each selected column manually
            
        # Latitude and Longitude
        data_lat = self.data_original['LAT_leo02'].to_numpy()
        data_long = self.data_original['LONG_leo02'].to_numpy()
        variance_lat = self.data_variance['LAT_leo02'].to_numpy()
        variance_long = self.data_variance['LONG_leo02'].to_numpy()
        axs[0].plot(timestamps_np, data_lat, label='lat leo02')
        axs[1].plot(timestamps_np, data_long, label='long leo02')
        axs[0].fill_between(timestamps_np, data_lat - variance_lat, data_lat + variance_lat, alpha=0.2)
        axs[1].fill_between(timestamps_np, data_long - variance_long, data_long + variance_long, alpha=0.2)
        axs[0].set_ylabel("Pose")
        axs[0].legend()

        # Delay
            
        # Bytes Sent
            
        
        # for i, column in enumerate(self.display_columns):
        #     data_np = self.data_original[column].to_numpy()
        #     variance_np = self.data_variance[column].to_numpy()

        #     axs[i].plot(timestamps_np, data_np, label=column)
        #     if self.plot_variances:
        #         axs[i].fill_between(timestamps_np, data_np - variance_np, data_np + variance_np, alpha=0.2)
        #     axs[i].set_ylabel(column)
        #     axs[i].legend()

        plt.xlabel('Timestamp')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot data with variance from CSV files.')
    parser.add_argument('rmw', type=str, help='RMW value')
    parser.add_argument('prefix', type=str, help='Prefix for the CSV files')


    args = parser.parse_args()

    if not args.rmw or not args.prefix:
        print("Usage: python your_script_name.py <RMW> <Prefix>")
        print("Example: python3 plot_one_file_with_variance.py zenoh zenoh_clean")
        sys.exit(1)

    plotter = DataPlotter(args.rmw, args.prefix)
    plotter.load_data()
    plotter.extract_and_interpolate()
    plotter.plot_data()
