import sys
from tmuxp import config
from tmuxp.workspacebuilder import Server
from tmuxp.workspacebuilder import WorkspaceBuilder

def build_config(dataset_number: str, robot_name: str):
    """Generate a tmuxp config dict dynamically."""

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
                    {'shell_command': ['sleep 4', f'ros2 bag play $DATA_DIR/{robot_name} --topics /imu /cam0 /odom_gt /odom_gt/path']}
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
    if len(sys.argv) < 3:
        print("Usage: python3 tmuxp_launch.py <version_number> <robot_name>")
        sys.exit(1)

    launch_conf = config.trickle(config.expand(build_config(sys.argv[1], sys.argv[2])))
    server = Server()
    workspace = WorkspaceBuilder(launch_conf, server=server)
    workspace.build()
    server.attach_session(launch_conf['session_name'])

if __name__ == "__main__":
    main()
