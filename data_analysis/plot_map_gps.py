"""
Plot the map overview of the experiments.
Takes GPS coordinates as an input and plot them on a graph.
"""
import pandas as pd
import plotly.graph_objects as go
import random as rd
import pathlib

PATH = str(pathlib.Path(__file__).parent.resolve()) + '/data/Cleaned'
MESSAGE_SIZE = 16


class Plot_GPS:
    def __init__(self, path_p, message_size_p) -> None:
        self.path = path_p
        self.df_list = []
        self.message_size = message_size_p
        self.colors = ['rgb(0,0,255)','rgb(255,0,0)','rgb(0,255,0)']
        self.df_list.append(pd.read_csv(self.path+f'/fast/fast_KILO{self.message_size}/fastrtps_KILO{self.message_size}_exp_5_resampled.csv'))
        self.df_list.append(pd.read_csv(self.path+f'/cyclone/cyclone_KILO{self.message_size}/cyclonedds_KILO{self.message_size}_exp_1_resampled.csv'))
        self.df_list.append(pd.read_csv(self.path+f'/zenoh/zenoh_KILO{self.message_size}/zenoh_KILO{self.message_size}_exp_3_resampled.csv'))
        self.fig = go.Figure()
        

    def plot_ly(self):
        # Plot rover trajectory
        for i in range(3):
            print(self.df_list[i])
            self.fig.add_trace(go.Scattermapbox(
                lon = self.df_list[i]['LONG_leo02'],
                lat = self.df_list[i]['LAT_leo02'],
                mode = 'lines+markers',
                marker = dict(
                        size = 5,
                        color =self.colors[i],
                    )
                ))
        
        # Lander
        self.fig.add_trace(go.Scattermapbox(
            lon = [6.1588639999999995]*len(self.df_list[0]),
            lat = [49.62566233333333]*len(self.df_list[0]),
            mode = 'markers',
            marker = dict(
                    size = 15,
                    color = 'rgb(0, 0, 0)',
                    # name = "test"
                )
            ))    

        # Static point
        self.fig.add_trace(go.Scattermapbox(
            lon = [6.157641]*len(self.df_list[0]),
            lat = [49.626623]*len(self.df_list[0]),
            mode = 'markers',
            marker = dict(
                    size = 15,
                    color = 'rgb(0, 0, 0)',
                )
            ))

        # Leo03 (Relay)
        self.fig.add_trace(go.Scattermapbox(
            lon = [6.159770]*len(self.df_list[0]),
            lat = [49.626670]*len(self.df_list[0]),
            mode = 'markers',
            marker = dict(
                    size = 15,
                    color = 'rgb(0, 0, 0)',
                )
            ))

        # Layout settings
        self.fig.update_layout(
            # template='plotly_dark',
            title = "Mesh experiment overview",
            mapbox_style="open-street-map",
            mapbox_center_lat=49.6265,
            mapbox_center_lon=6.159,
            mapbox_zoom=17,
            )

        self.fig.show()





if __name__ == "__main__":
    plot = Plot_GPS(PATH, MESSAGE_SIZE)
    plot.plot_ly()