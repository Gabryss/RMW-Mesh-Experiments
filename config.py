from enum import Enum


class Config(Enum):  
    # Leo02
    LEO02_NAME = "leo02"
    LEO02_HOST = "192.168.44.123"
    LEO02_USERNAME = "xavier"
    LEO02_PASSWORD = "xavier"
    LEO02_ROS_WS_PATH = "/home/xavier/ros2_ws"
    LEO02_ROS_DISTRO = "foxy"


    # Leo03
    LEO03_NAME = "leo03"
    LEO03_HOST = "192.168.44.133"
    LEO03_USERNAME = "xavier"
    LEO03_PASSWORD = "xavier"
    LEO03_ROS_WS_PATH = "/home/xavier/ros2_ws"
    LEO03_ROS_DISTRO = "foxy"

    # MASTER
    MASTER_ROS_WS_PATH = "/home/gabriel/ros2_ws"
    MASTER_ROS_DISTRO = "humble"

    # Zenoh
    ZENOH = False
    # DDS
    # ROS_DOMAIN_ID

    ROBOTS_NAME_LIST = [LEO02_NAME]
    ROBOTS_HOST_LIST = [LEO02_HOST]
    ROBOTS_USERNAME_LIST = [LEO02_USERNAME]
    ROBOTS_PASSWORD_LIST = [LEO02_PASSWORD]

    EXPERIMENT_NAME = "fast_zenoh_test"
    EXPERIMENT_TIME = 10            # In seconds
    EXPERIMENT_TIMESTEP = 0.1       # Step between each measurement (in seconds)
    PACKET_SIZE = "KILO512"            # Packet size (string)
                                    #KILO = 1024, KILO2 = 2048, KILO4 = 4096, KILO8 = 8192, KILO16 = 16384 KILO32 = 32768
                                    #KILO64 = 65536, KILO128 = 131072, KILO256 = 262144, KILO512 = 524288, MEGA = 1048576
                                    #MEGA2 = 2097152, MEGA4 = 4194304, MEGA8 = 8388608, MEGA16 = 16777216, MEGA32 = 33554432
                                    #MEGA64 = 67108864, MEGA128 = 134217728, MEGA256 = 268435456, MEGA512 = 536870912, GIGA = 1073741824


    # Paths
    REMOTE_MONITORING_DIR = "~/remote_monitoring"
    LOCAL_MONITORING_DIR = ""

    REMOTE_DATASET_PATH = "/home/xavier/dataset"
    LOCAL_DATASET_PATH = "~/dataset"


    # Activate/Deactivate local and remote monitoring
    USE_LOCAL = True
    USE_REMOTE = True

    # Download the entire database of every robot on the local database 
    GET_ENTIRE_DATABASE = False

    # Remote ssh timeout
    REMOTE_SSH_TIMEOUT = 5
