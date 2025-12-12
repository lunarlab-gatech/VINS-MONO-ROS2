import sys
from tmuxp import config
from tmuxp.workspacebuilder import Server
from tmuxp.workspacebuilder import WorkspaceBuilder

def build_config(dataset_number: str, robot_name: str, use_rosbag_play: str):
    """Generate a tmuxp config dict dynamically.
    
    Args:
        dataset_number (str): The Hercules dataset version number (e.g., V1.6).
        robot_name (str): The name of the robot (e.g., Drone1).
        use_rosbag_play (str): Whether to use ros2 bag play (this assumes you've made a rosbag file) 
            or custom publisher script.
    """

    if use_rosbag_play.lower() in ['true', '1', 'yes', 'y']:
        use_rosbag = True
    else:
        use_rosbag = False

    if use_rosbag:
        play_cmds = [f'ros2 bag play $DATA_DIR/{robot_name} --topics /imu /cam0 /odom_gt /odom_gt/path']
    else:
        play_cmds = ['unset PYTHONPATH',
                     'source /opt/miniconda3/bin/activate robotdataprocess',
                     'source $ROS_DIR/setup.bash',
                     f'python3 $ROS_WS/src/VINS-MONO-ROS2/dependencies/robotdataprocess/examples/Hercules/publish_data_VINS-Mono.py --dataset_num {dataset_number} --robot_name {robot_name}']

    config = {
        'session_name': 'vins_mono', 
        'environment': {
            'ROS_DIR': '/opt/ros/foxy', 
            'DATA_DIR': f'/home/dbutterfield3/data/Hercules_datasets/{dataset_number}/extract/bags_for_vins_mono', 
            'ROS_WS': '/home/dbutterfield3/vins_mono_ws'
        }, 
        'options': {
            'default-command': '/bin/bash'
        }, 
        'windows': [
            {
                'window_name': 'main', 
                'layout': 'tiled', 
                'focus': True, 
                'shell_command_before': ['source $ROS_DIR/setup.bash', 'source $ROS_WS/install/setup.bash'], 
                'panes': [
                    {'shell_command': []},
                    {'shell_command': ['sleep 2', f'ros2 launch feature_tracker vins_feature_tracker.launch.py config_path:=config/hercules/{dataset_number}/{robot_name}.yaml']}, 
                    {'shell_command': ['export RCL_LOG_LEVEL=DEBUG', 'sleep 2', f'ros2 launch vins_estimator euroc.launch.py config_path:=config/hercules/{dataset_number}/{robot_name}.yaml']}, 
                    {'shell_command': ['sleep 4', *play_cmds]}
                ]
            }, 
            {
                'window_name': 'kill', 
                'layout': 'tiled', 
                'panes': ['tmux kill-session -t vins_mono_']
            }
        ]
    }

    return config

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 tmuxp_launch.py <version_number> <robot_name> <use_rosbag_play>")
        sys.exit(1)

    launch_conf = config.trickle(config.expand(build_config(sys.argv[1], sys.argv[2], sys.argv[3])))
    server = Server()
    workspace = WorkspaceBuilder(launch_conf, server=server)
    workspace.build()
    server.attach_session(launch_conf['session_name'])

if __name__ == "__main__":
    main()
