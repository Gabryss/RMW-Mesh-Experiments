"""
Zoom on the rover's trajectories.
Takes GPS coordinates as an input and plot them on a graph.
"""
import pandas as pd
import plotly.graph_objects as go
import pathlib

PATH = str(pathlib.Path(__file__).parent.resolve()) + '/data/Cleaned'
MESSAGE_SIZE = 16
FILTER = True

class Plot_GPS:
    def __init__(self, path_p, message_size_p) -> None:
        self.path = path_p
        self.message_size = message_size_p
        self.df_fast = pd.read_csv(self.path+f'/fast/fast_KILO{self.message_size}/fastrtps_KILO{self.message_size}_exp_5_resampled.csv')
        self.df_cyclone = pd.read_csv(self.path+f'/cyclone/cyclone_KILO{self.message_size}/cyclonedds_KILO{self.message_size}_exp_1_resampled.csv')
        self.df_zenoh = pd.read_csv(self.path+f'/zenoh/zenoh_KILO{self.message_size}/zenoh_KILO{self.message_size}_exp_3_resampled.csv')

        if FILTER:
            self.df_fast_filtered = self.filter(self.df_fast)
            self.df_cyclone_filtered = self.filter(self.df_cyclone)
            self.df_zenoh_filtered = self.filter(self.df_zenoh)
        else:
            self.df_fast_filtered = [self.df_fast]
            self.df_cyclone_filtered = [self.df_cyclone]
            self.df_zenoh_filtered = [self.df_zenoh]


        self.fig = go.Figure()
        

    def plot_ly(self):
        """
        Plot rover trajectories
        """

        # Fast
        for i in range(len(self.df_fast_filtered)):
            self.fig.add_trace(go.Scattermapbox(
                lon = self.df_fast_filtered[i]['LONG_leo02'],
                lat = self.df_fast_filtered[i]['LAT_leo02'],
                mode = 'lines+markers',
                marker = dict(
                        size = 5,
                        color = 'rgb(0, 0, 255)',
                    ),
                name = f'FastRTPS'
                ))

        # Cyclone
        for i in range(len(self.df_cyclone_filtered)):
            self.fig.add_trace(go.Scattermapbox(
                lon = self.df_cyclone_filtered[i]['LONG_leo02'],
                lat = self.df_cyclone_filtered[i]['LAT_leo02'],
                mode = 'lines+markers',
                marker = dict(
                        size = 5,
                        color = 'rgb(255, 0, 0)',
                    ),
                name = f'CycloneDDS'
                ))
        
        # Zenoh
        for i in range(len(self.df_zenoh_filtered)):
            self.fig.add_trace(go.Scattermapbox(
                lon = self.df_zenoh_filtered[i]['LONG_leo02'],
                lat = self.df_zenoh_filtered[i]['LAT_leo02'],
                mode = 'lines+markers',
                marker = dict(
                        size = 5,
                        color = 'rgb(0, 255, 0)',
                    ),
                name = f'ZenohRMW'
                ))

        # Layout settings
        self.fig.update_layout(
            # template='plotly_dark',
            title = "Mesh experiment overview zoomed",
            mapbox_style="open-street-map",
            mapbox_center_lat=49.6275,
            mapbox_center_lon=6.159,
            mapbox_zoom=18.4,
        )

        self.fig.show()


    def filter(self, df_p):
        """
        Remove the row where the leo can not be reached
        This method create a list of dataframes for each middleware. Create a new Dataframe every time the connection between the lander and the Leo Rover is lost then retrieved.
        The objective is to plot the trajectories only when the lander and the rover can communicate.
        example:
        fast_list = [traj_chunk_1, traj_chunk_2, traj_chunk_3, ...]
        cyclone_list = [traj_chunk_1, traj_chunk_2, traj_chunk_3, ...]
        zenoh_list = [traj_chunk_1, traj_chunk_2, traj_chunk_3, ...]
        """
        df = df_p
        start_index_traj = 0
        df_list = []
        new_traj = True

        for index, row in df.iterrows():

            # If signal lost and has not been reaquired in the meantime, add trajectory to the list
            if row['Ping_target_local'] == 0.0:
                if new_traj == True:
                    trajectory = df.iloc[start_index_traj : index] # Slice the trajectory
                    df_list.append(trajectory) # Add the created trajectory into the list

                new_traj = False # Signal lost

            else:
                # Get the new starting position of trajectory while ping acquired
                if new_traj == False:
                    start_index_traj = index
                    new_traj = True

                new_traj = True # Signal reaquired, ready for a new plot

        # Add last segment trajectory
        if df.iloc[-1]['Ping_target_local'] != 0.0:
            trajectory = df.iloc[start_index_traj : index] # Slice the trajectory
            df_list.append(trajectory) # Add the created trajectory into the list

        return df_list


if __name__ == "__main__":
    plot = Plot_GPS(PATH, MESSAGE_SIZE)
    plot.plot_ly()