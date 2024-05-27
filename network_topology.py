import networkx as nx
import matplotlib.pyplot as plt
import time
from datetime import datetime
import routeros_api

def execute_command(ip, username, password, command):
    try:
        connection = routeros_api.RouterOsApiPool(ip, username=username, password='', plaintext_login=True)
        connection.set_timeout(2)
        api = connection.get_api()
        response = api.get_binary_resource('/').call(command)
        connection.disconnect()
        return response
    except Exception as e:
        print(f"Could not connect to {ip}: {e}")
        return None

# Hardcoded list pairing each antenna with its IP, username, and password
antenna_info = {
    #"MTA-I": {"ip": "192.168.44.160", "MAC": "DC:2C:6E:F4:E0:2E", "username": "admin", "password": ""},
    #"MTA-F": {"ip": "192.168.44.150", "MAC": "48:8F:5A:B5:E4:24", "username": "admin", "password": ""},
    #"MTA-A": {"ip": "192.168.44.110", "MAC": "DC:2C:6E:F4:E4:C2","username": "admin", "password": ""},
    #"MTA-J": {"ip": "192.168.44.170", "MAC": "DC:2C:6E:F4:DF:FA","username": "admin", "password": ""},
    #"MTA-K": {"ip": "192.168.44.180", "MAC": "DC:2C:6E:F4:E0:1C","username": "admin", "password": ""},
    #"MTA-B": {"ip": "192.168.44.120", "MAC": "48:8F:5A:B5:E4:CD","username": "admin", "password": ""},
    #"MTA-C": {"ip": "192.168.44.130", "MAC": "48:8F:5A:B7:D5:36","username": "admin", "password": ""},
    "Static": {"ip": "192.168.44.150", "MAC": "48:8F:5A:B5:E4:CD","username": "admin", "password": ""}, #MTA_B
    "LEO02": {"ip": "192.168.44.120", "MAC": "DC:2C:6E:F4:E0:2E","username": "admin", "password": ""}, #MTA_I
    "LEO03": {"ip": "192.168.44.130", "MAC": "DC:2C:6E:F4:DF:FA","username": "admin", "password": ""}, #MTA_J
    "Lander": {"ip": "192.168.44.100", "MAC": "48:8F:5A:B7:D5:36","username": "admin", "password": ""} #MTA_C
    # Add more antennas and their information here
}

label_offset = 0.01     # Offset to position edge labels
command = "interface/mesh/fdb/print"

initial_layout = {}
previous_edges = set()

while True:  # Infinite loop to keep updating the graph
    G = nx.DiGraph()  # Initialize an empty graph
    edge_labels = {}  # Dictionary to hold edge labels
    
    for antenna_name, info in antenna_info.items():
        ip = info["ip"]
        username = info["username"]
        password = info["password"]

        result = execute_command(ip, username, password, command)

        if result is not None:
            for entry in result:
                neighbor_mac = entry.get('mac-address').decode('utf-8')  # Convert bytes to string
                entry_type = entry.get('type').decode('utf-8')  # Convert bytes to string
                metric = entry.get('metric').decode('utf-8')  # Assuming metric is also in the entry
                
                if entry_type == 'neighbor':
                    # Find the antenna name corresponding to the MAC address
                    neighbor_name = [name for name, inf in antenna_info.items() if inf['MAC'] == neighbor_mac]
                    
                    if neighbor_name:
                        neighbor_name = neighbor_name[0]
                        G.add_edge(antenna_name, neighbor_name, metric=metric)
                        #edge_labels[(antenna_name, neighbor_name, key)] = metric  # Include the key
                        print(f"Added edge between {antenna_name} and {neighbor_name}, metric {metric}")
                    else:
                        print(f"Could not find neighbor name for MAC address {neighbor_mac}")




    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    plt.gcf().canvas.set_window_title(f"Mesh Topology Graph : {current_time}")

    # Draw the graph
    current_edges = set(G.edges())
    
    if current_edges != previous_edges:
        # Update the layout if the edges have changed
        print("Edges have changed, updating layout.")
        if G.nodes() and initial_layout:
            initial_layout = nx.spring_layout(G, pos=initial_layout)
        else:
            initial_layout = nx.spring_layout(G)
        # Update the previous_edges set
        previous_edges = current_edges
        plt.clf()
        nx.draw(G, initial_layout, with_labels=True, font_weight='bold', node_color='white', edgecolors="black", font_size=18, node_size=5000, font_color='black', width=5.0, linewidths=5)

    edge_labels=dict([((u,v,),d['metric'])
                for u,v,d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, initial_layout, edge_labels=edge_labels, label_pos=0.3, font_size=7)


    plt.pause(1)  # Pause to display the plot
    time.sleep(10)  # Sleep for 60 seconds before the next update
