# Remote Monitoring

### Purpose
This repository was originaly created to monitor multiple robots all at once using different scripts for an experiment. Once the "master" file called `master_monitoring.py` is launched, a specific number of other files will alwo be triggered, starting the experiment. The master file use a config file as an input to monitor itself and a various number of robots. The connection between the monitoring station and the robot is provided by SSH protocol, allowing execution of command lines or downloading back the created database (at the end of the experiment). During the experiment, a database (`csv` format) is created by the monitoring script (create automaticaly a folder) at the specified path in the config file. Otherwise the script will try to create it in the package folder.

The overall architecture of the script follows like this:
![Overall Architecture](docs/diagrams/out/architecture_overview.png)

Each robot has a "sub-master" node called `meta_monitoring.py` responsible for launching all the monitoring script within a device (robot or monitoring station). This architecture is up to down only with a partial or complete download of the database at the end of the experiment.


### Installation
The installation was tested on `Python 3.10.6` with the default libraries:
- `os`
- `subprocess`
- `threading`
- `sys`
- `paramiko`
- `colorama`
- `multiprocessing`
- `argparse`
- `psutil`
- `csv`
- `time`

For more information about the installed libraries, please check the `requirements.txt` file.

Installed libraries:
- `psutil` (Give measurement related to your computer)
- `paramiko` (SSH connection)
- `colorama` (Nice looking terminal output)

Strictly speaking, the monitoring station should have the whole package whereas the other rovers only the `monitoring.py` and `meta_monitoring.py` files. However, installing the package on the robot has no effect. 

### Usage
Before launching the `master_monitoring.py` make sure to enter every needed informations in the config file such has host, username and password for the SSH connection.

Once everything is configured, run the command:

```shell
$ python3 master_monitor.py
```

Note that you can have further documentation on each script by running:

```shell
$ python3 <name_of_the_script.py> -h
```


### Limitations
Currently it is not possible to change dynamicaly or remotely the monitoring scripts during runtime. The name of the script should be hard coded within the `meta_monitoring.py` file.

This package is experiment oriented, meaning the first purpose is to collect efficiently data, not do live monitoring. Live monitoring would probably change deeply the architecture of the package.
