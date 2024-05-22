from enum import Enum
from pathlib import Path

class Config(Enum):
    # Paths
    PROJECT_NAME = "RMW-Mesh-Experiments"
    PROJECT_PATH = str(Path(__file__).parent.resolve())
    PARENT_PROJECT_PATH = str(Path(PROJECT_PATH).parent.resolve())
    REMOTE_PATH = "/home/pi/mesh_exp"
    REMOTE_WS_PATH = REMOTE_PATH + PROJECT_NAME
    REMOTE_DATASET_PATH = REMOTE_PATH + "/dataset"
    DATASET_PATH = PARENT_PROJECT_PATH + "/dataset"

    REMOTE_USERNAME = "pi"
    REMOTE_PASSWORD = "raspberry"

    # Target
    TARGET = "leo02"
    TARGET_IP = "1.1.1.1"

    #LeoA
    LEOA_NAME = "leo02"
    LEOA_HOST = "192.168.44.122"

    #LeoB
    LEOB_NAME = "leo03"
    LEOB_HOST = "192.168.44.132"


    # DDS
    #DDS = "fastrtps"
    DDS = "cyclonedds"
    # DDS = "zenoh"

    RMW_IMPLEMENTATION = f"rmw_{DDS}_cpp"

    ROBOTS_NAME_LIST = [LEOA_NAME, LEOB_NAME]
    ROBOTS_HOST_LIST = [LEOA_HOST, LEOB_HOST]
    # ROBOTS_NAME_LIST = [LEOA_NAME]
    # ROBOTS_HOST_LIST = [LEOA_HOST]


    EXPERIMENT_NAME = f"{DDS}_test_9"
    EXPERIMENT_TIME = 10            # In seconds
    EXPERIMENT_TIMESTEP = 0.1       # Step between each measurement (in seconds)
    PACKET_SIZE = "KILO32"            # Packet size (string)
                                    #KILO = 1024, KILO2 = 2048, KILO4 = 4096, KILO8 = 8192, KILO16 = 16384 KILO32 = 32768
                                    #KILO64 = 65536, KILO128 = 131072, KILO256 = 262144, KILO512 = 524288, MEGA = 1048576
                                    #MEGA2 = 2097152, MEGA4 = 4194304, MEGA8 = 8388608, MEGA16 = 16777216, MEGA32 = 33554432
                                    #MEGA64 = 67108864, MEGA128 = 134217728, MEGA256 = 268435456, MEGA512 = 536870912, GIGA = 1073741824


    # Activate/Deactivate local and remote monitoring
    USE_LOCAL = True
    USE_REMOTE = True

    # Download the entire database of every robot on the local database 
    GET_ENTIRE_DATABASE = False

    # Remote ssh timeout
    REMOTE_SSH_TIMEOUT = 5