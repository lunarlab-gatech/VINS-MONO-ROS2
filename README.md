# VINS-MONO-ROS2
## ROS2 version of VINS-MONO
# 1. Introduction
This repository implements the ROS2 version of VINS-MONO, mainly including the following packages:
* **camera_model**
* **feature_tracker**
* **vins_estimator**
* **pose_graph**
* **benchmark_pubilsher**
* **ar_demo**
* **config_pkg**

**NOTE**: Since the **_get_package_share_directory_** command in ROS2 launch files can only locate packages in the _install_ directory instead of the _src_ directory like ROS1, we create a package called **_config_pkg_** to store the _config/_ and _support_files/_ folders from VINS-MONO.
 
![mh01](https://github.com/dongbo19/VINS-MONO-ROS2/blob/main/config_pkg/config/gif/vins_ros2_mh01.gif)
![mh02](https://github.com/dongbo19/VINS-MONO-ROS2/blob/main/config_pkg/config/gif/vins_ros2_mh02.gif)
# 2. Prerequisites
* System  
  * Ubuntu 20.04  
  * ROS2 foxy
* Libraries
  * OpenCV 4.2.0
  * [Ceres Solver](http://ceres-solver.org/installation.html) 1.14.0
  * Eigen 3.3.7
# 3. Build VINS-MONO-ROS2

## Docker Setup
Make sure to install:
- [Docker](https://docs.docker.com/engine/install/ubuntu/)

Then, clone this repository in a ROS2 workspace at a desired location on your computer.

After that, navigate to the `docker` directory. Log in to the user that you want the docker file to create in the container. Then, edit the `DOCKERFILE` to update these lines:
- `ARG USERNAME=`: Your username
- `ARG USER_UID=`: Output of `echo $UID`
- `ARG USER_GID=`: Output of `id -g`

Edit the `enter_container.sh` script with the following paths:
- `DATA_DIR=`: The directory where the any datasets are located
- `ROS_WS_DIR=`: The directory of the ros workspace this repository is a part of

Now, run the following commands:
```
build_container.sh
run_container.sh
```

The rest of this README **assumes that you are inside the Docker container**. For easier debugging and use, its highly recommended to install the [VSCode Docker extension](https://code.visualstudio.com/docs/containers/overview), which allows you to start/stop the container and additionally attach VSCode to the container by right-clicking on the container and selecting `Attach Visual Studio Code`.


# Build
Next navigate to the root of your ROS workspace, and run the following commands:
```
colcon build
```

# Support Files install
Run the following command in the root of your ROS workspace to install support files from the original VINS-Mono:
```
git clone git@github.com:HKUST-Aerial-Robotics/VINS-Mono.git
```

# 4. VINS-MONO-ROS2 on EuRoC datasets
## 4.1. ROS1 bag to ROS2 bag
Download [EuRoC datasets](https://projects.asl.ethz.ch/datasets/doku.php?id=kmavvisualinertialdatasets). However, the datasets are in ROS1 format. To run the code in ROS2, we need to first convert these datasets to ROS2 format. We can use [rosbags](https://pypi.org/project/rosbags/) for this purpose, which can convert ROS built-in messages between ROS1 and ROS2.  
## 4.2. Visual-inertial odometry and loop closure
All configuration files are in the package, **_config_pkg_**, so in launch files, the path to the EuRoC configuration files is found using **_get_package_share_directory('config_pkg')_**.  

Then, navigate to this repositories folder and run the following command:
```
tmuxp load tmux/euroc.yaml
```
![mh05](https://github.com/dongbo19/VINS-MONO-ROS2/blob/main/config_pkg/config/gif/vins_ros2_mh05.gif)
![v101](https://github.com/dongbo19/VINS-MONO-ROS2/blob/main/config_pkg/config/gif/vins_ros2_v101.gif)

## 4.3. Visualize ground truch
First, take the MH01 for example, modifying the **'sequence_name'** in the launch file: 
**_benchmark_publisher/launch/benchmark_publisher.launch.py_**
```
sequence_name_arg = DeclareLaunchArgument(
    'sequence_name',
    default_value='MH_01_easy',
    description='Sequence name for the benchmark'
)
sequence_name = LaunchConfiguration('sequence_name')
```
**PS: After modifying the launch file, don't forget to run **_colcon build_** for this package again.**  
Then, run the following command:
```
tmuxp load tmux/euroc_w_benchmark.yaml
```
![mh01_benchmark](https://github.com/dongbo19/VINS-MONO-ROS2/blob/main/config_pkg/config/gif/vins_ros2_benchmark_mh01.gif)
![mh02_benchmark](https://github.com/dongbo19/VINS-MONO-ROS2/blob/main/config_pkg/config/gif/vins_ros2_benchmark_mh02.gif)

## 4.4. AR Demo
Download the [bag file](https://www.dropbox.com/scl/fi/q18lot4bfs1fqrctclz7b/ar_box.bag?rlkey=16yrxnwnt2fcutwwzwhlevd1n&e=1&dl=0).  
Then open two terminals  
```
ros2 launch ar_demo 3dm_bag.launch.py               # for featuer tracking, backend optimization, ar demo and rviz2.
ros2 bag play $(PATH_TO_YOUR_DATASET)/ar_box        # for ros2 bag
```
![ar_demo](https://github.com/dongbo19/VINS-MONO-ROS2/blob/main/config_pkg/config/gif/vins_ros2_ar_demo.gif)

# 5. VINS-MONO-ROS2 on HERCULES dataset

Run the following command to run V1.2 of the HERCULES dataset:

```
tmuxp load ./src/VINS-MONO-ROS2/tmux/hercules_husky_V1.2.yaml
```
