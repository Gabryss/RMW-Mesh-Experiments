from enum import Enum


class Config(Enum):


    # Target
    TARGET = "leo02"


    #LeoA
    LEOA_NAME = "leo02"
    LEOA_HOST = "192.168.44.122"
    LEOA_USERNAME = "pi"
    LEOA_PASSWORD = "raspberry"
    LEOA_ROS_WS_PATH = "/home/pi/mesh_exp/remote_monitoring/exp_ws"
    LEOA_ROS_DISTRO = "iron"

    #LeoB
    LEOB_NAME = "leo03"
    LEOB_HOST = "192.168.44.132"
    LEOB_USERNAME = "pi"
    LEOB_PASSWORD = "raspberry"
    LEOB_ROS_WS_PATH = "/home/pi/mesh_exp/remote_monitoring/exp_ws"
    LEOB_ROS_DISTRO = "iron"


    # Leo02
    # LEO02_NAME = "leo02"
    # LEO02_HOST = ""
    # LEO02_USERNAME = ""
    # LEO02_PASSWORD = ""
    # LEO02_ROS_WS_PATH = "/home/pi/mesh_exp/remote_monitoring/exp_ws"
    # LEO02_ROS_DISTRO = "iron"


    # Leo03
    # LEO03_NAME = "leo03"
    # LEO03_HOST = ""
    # LEO03_USERNAME = ""
    # LEO03_PASSWORD = ""
    # LEO03_ROS_WS_PATH = "/home/pi/mesh_exp/remote_monitoring/exp_ws"
    # LEO03_ROS_DISTRO = "iron"

    # MASTER
    MASTER_ROS_WS_PATH = "/home/lchovet/mesh_exp/remote_monitoring/exp_ws"
    MASTER_ROS_DISTRO = "iron"

    # Zenoh
    ZENOH = False
    # DDS
    #DDS = "fastrtps"
    DDS = "cyclonedds"
    # DDS = "zenoh"

    RMW_IMPLEMENTATION = f"rmw_{DDS}_cpp"
    # ROS_DOMAIN_ID

    ROBOTS_NAME_LIST = [LEOA_NAME, LEOB_NAME]
    ROBOTS_HOST_LIST = [LEOA_HOST, LEOB_HOST]
    ROBOTS_USERNAME_LIST = [LEOA_USERNAME, LEOB_USERNAME]
    ROBOTS_PASSWORD_LIST = [LEOA_PASSWORD, LEOB_PASSWORD]
    ROBOTS_ROS_WS_PATH_LIST = [LEOA_ROS_WS_PATH, LEOB_ROS_WS_PATH]
    ROBOTS_ROS_DISTRO_LIST = [LEOA_ROS_DISTRO, LEOB_ROS_DISTRO]
    # ROBOTS_NAME_LIST = [LEOA_NAME]
    # ROBOTS_HOST_LIST = [LEOA_HOST]
    # ROBOTS_USERNAME_LIST = [LEOA_USERNAME]
    # ROBOTS_PASSWORD_LIST = [LEOA_PASSWORD]
    # ROBOTS_ROS_WS_PATH_LIST = [LEOA_ROS_WS_PATH]
    # ROBOTS_ROS_DISTRO_LIST = [LEOA_ROS_DISTRO]


    EXPERIMENT_NAME = f"{DDS}_test_7"
    EXPERIMENT_TIME = 60            # In seconds
    EXPERIMENT_TIMESTEP = 0.1       # Step between each measurement (in seconds)
    PACKET_SIZE = "KILO32"            # Packet size (string)
                                    #KILO = 1024, KILO2 = 2048, KILO4 = 4096, KILO8 = 8192, KILO16 = 16384 KILO32 = 32768
                                    #KILO64 = 65536, KILO128 = 131072, KILO256 = 262144, KILO512 = 524288, MEGA = 1048576
                                    #MEGA2 = 2097152, MEGA4 = 4194304, MEGA8 = 8388608, MEGA16 = 16777216, MEGA32 = 33554432
                                    #MEGA64 = 67108864, MEGA128 = 134217728, MEGA256 = 268435456, MEGA512 = 536870912, GIGA = 1073741824


    # Paths
    REMOTE_MONITORING_DIR = "~/mesh_exp/remote_monitoring"
    LOCAL_MONITORING_DIR = ""

    REMOTE_DATASET_PATH = "/home/pi/mesh_exp/dataset"
    LOCAL_DATASET_PATH = "~/mesh_exp/dataset"


    # Activate/Deactivate local and remote monitoring
    USE_LOCAL = True
    USE_REMOTE = True

    # Download the entire database of every robot on the local database 
    GET_ENTIRE_DATABASE = False

    # Remote ssh timeout
    REMOTE_SSH_TIMEOUT = 5