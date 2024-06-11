import os
import glob
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

class DataVisualizer:
    def __init__(self) -> None:
        """
        Initialize the DataVisualizer class.
        """
        self.message_sizes = ['KILO', 'KILO2', 'KILO4', 'KILO8', 'KILO16', 'KILO32', 'KILO64']
        self.path = './data/Cleaned/'
        self.fast_data = self.get_all_dataframe(self.path + 'fast/', 'fast')
        self.cyclone_data = self.get_all_dataframe(self.path + 'cyclone/', 'cyclone')
        self.zenoh_data = self.get_all_dataframe(self.path + 'zenoh/', 'zenoh')

        # Combine all data into a single DataFrame
        self.all_data = pd.concat([self.fast_data, self.cyclone_data, self.zenoh_data], ignore_index=True)

    def get_all_dataframe(self, folder_path, rmw_type):
        # For a given RMW, span over each size
        data = []
        for size in self.message_sizes:
            df = self.get_dataframe_size(size, folder_path)
            if df is not None:
                df['Message_Size'] = size
                df['RMW'] = rmw_type
                data.append(df)
        if data:
            concatenated_data = pd.concat(data, ignore_index=True)  # Ignore index to avoid duplicate labels
            return concatenated_data
        else:
            return pd.DataFrame()

    def get_dataframe_size(self, size, folder_path):
        # For a given size, get the dataframe containing each run
        pattern = os.path.join(folder_path, f'**/*_{size}_*_resampled.csv')
        csv_files = glob.glob(pattern, recursive=True)
        if not csv_files:
            return None
        dataframes = [pd.read_csv(file) for file in csv_files]
        return pd.concat(dataframes, ignore_index=True)  # Ignore index to avoid duplicate labels

    def plot_boxplot(self, metric):
        if self.all_data.empty:
            print("No data available to plot.")
            return
        if metric not in self.all_data.columns:
            print(f"Metric '{metric}' not found in data.")
            return
        
        # Define a color palette
        palette = {"fast": "blue", "cyclone": "red", "zenoh": "green"}
        
        plt.figure(figsize=(7, 5))
        sns.boxplot(data=self.all_data, x='Message_Size', y=metric, hue='RMW', palette=palette, showfliers=False,linewidth=2.5)
        plt.title(f'Boxplot of {metric} for Different RMWs and Message Sizes')
        plt.xlabel('Message Size')
        plt.ylabel(metric)
        plt.legend(title='RMW')
        plt.grid(True, linestyle='--', alpha=0.7)
        folder = 'CPU and RAM'
        path = f'../docs/plots/{folder}/box_{metric}.png'
        plt.savefig(path,bbox_inches='tight')
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot data with variance from CSV files.')
    parser.add_argument('column', type=str, help='Column to plot')
    # parser.add_argument('--use_run', action='store_true', help='Use run data instead of averaged data')
    # parser.add_argument('--run_size', type=str, default="KILO8", help='Size of the run')
    # parser.add_argument('--run_number', type=int, default=3, help='Run numbers for the RMW')
    # parser.add_argument('--plot_variances', action='store_true', help='Plot variances')
    # parser.add_argument('--save_path', type=str, default='plot.png', help='Path to save the plot image')

    args = parser.parse_args()

    # Example usage:
    visualizer = DataVisualizer()

    # Debug: print the structure of the combined DataFrame
    # print("Combined DataFrame head:")
    # print(visualizer.all_data.head())
    # print("\nCombined DataFrame columns:")
    # print(visualizer.all_data.columns)

    # Plot the boxplot
    visualizer.plot_boxplot(args.column)
