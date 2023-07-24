from enum import Enum


class Config(Enum):
    # TEST
    TEST_NAME = ''
    TEST_HOST = ''
    TEST_USERNAME = ''
    TEST_PASSWORD = ''

    # Leo02
    LEO02_NAME = ""
    LEO02_HOST = ""
    LEO02_USERNAME = ""
    LEO02_PASSWORD = ""


    # Leo03
    LEO03_NAME = ""
    LEO03_HOST = ""
    LEO03_USERNAME = ""
    LEO03_PASSWORD = ""


    # Global
    # ROBOTS_NAME_LIST = [LEO02_NAME, LEO03_NAME]
    # ROBOTS_HOST_LIST = [LEO02_HOST, LEO03_HOST]
    # ROBOTS_USERNAME_LIST = [LEO02_USERNAME, LEO03_USERNAME]
    # ROBOTS_PASSWORD_LIST = [LEO02_PASSWORD, LEO03_PASSWORD]

    ROBOTS_NAME_LIST = [TEST_NAME, TEST_NAME]
    ROBOTS_HOST_LIST = [TEST_HOST, TEST_HOST]
    ROBOTS_USERNAME_LIST = [TEST_USERNAME, TEST_USERNAME]
    ROBOTS_PASSWORD_LIST = [TEST_PASSWORD, TEST_PASSWORD]

    EXPERIMENT_NAME = "The great wall"
    EXPERIMENT_TIME = 1
    EXPERIMENT_TIMESTEP = 0.1
    REMOTE_ROBOT_NUMBER = 2
    PROCESS_PER_ROBOTS = 1 # If this value is greated than the actual number of monitoring script, the script will be frozen

    LOCAL_MONITORING_DIR = ""
    REMOTE_MONITORING_DIR = ""


    REMOTE_DATASET_PATH = "~/dataset"
    LOCAL_DATASET_PATH = ""

    # Activate/Deactivate local and remote monitoring
    USE_LOCAL = True
    USE_REMOTE = False

    # Download the entire database of every robot on the local database 
    GET_ENTIRE_DATABASE = False

    # Remote ssh timeout
    REMOTE_SSH_TIMEOUT = 5
