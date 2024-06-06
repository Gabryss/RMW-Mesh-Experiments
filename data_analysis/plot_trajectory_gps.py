"""
Takes GPS coordinates as an input and plot them on a graph
"""
import pandas as pd

import plotly.graph_objects as go

import random as rd

PATH = "/home/gabriel/Lab/python/data_science/fast_mesh_exp_2/fast_KILO8"
NB_TRAJECTORIES = 4


class Plot_GPS:
    def __init__(self, path_p, nb_trajectories_p) -> None:
        self.path = path_p
        self.nb_trajectories = nb_trajectories_p
        self.df_list = []
        for i in range(self.nb_trajectories):
            self.df_list.append(pd.read_csv(self.path+f'/fastrtps_KILO8_exp_{i+1}_leo02_global_monitoring.csv'))
        self.fig = go.Figure()
        

    def plot_ly(self):
        # Plot rover trajectory
        for i in range(self.nb_trajectories):
            self.fig.add_trace(go.Scattermapbox(
                lon = self.df_list[i]['LONG'],
                lat = self.df_list[i]['LAT'],
                mode = 'lines+markers',
                marker = dict(
                        size = 5,
                        color = f'rgb({rd.randint(0,255)}, {rd.randint(0,255)}, {rd.randint(0,255)})',
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
    plot = Plot_GPS(PATH, NB_TRAJECTORIES)
    plot.plot_ly()