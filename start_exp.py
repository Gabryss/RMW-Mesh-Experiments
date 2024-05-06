import os
import re

# Function to update EXPERIMENT_NAME in config.py
def update_config_file(new_number):
    with open('config.py', 'r') as file:
        lines = file.readlines()

    with open('config.py', 'w') as file:
        for line in lines:
            if 'EXPERIMENT_NAME = "cyclone_' in line:
                file.write(f'    EXPERIMENT_NAME = "cyclone_"+PACKET_SIZE+"_{new_number}" \n')
            else:
                file.write(line)

# Run the master_monitoring.py script and update config.py 10 times
for i in range(1, 11):
    # Uncomment the following line if you actually want to run the Python script
    os.system('python3 master_monitoring.py')

    # Read the config file and get the current EXPERIMENT_NAME
    with open('config.py', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if 'EXPERIMENT_NAME = "cyclone_' in line:
                current_number = int(re.search(r'_(\d+)"', line).group(1))

    # Increment the experiment number
    next_number = current_number + 1

    # Update config.py
    update_config_file(next_number)

# After all loops, reset the EXPERIMENT_NAME to 1
update_config_file(1)