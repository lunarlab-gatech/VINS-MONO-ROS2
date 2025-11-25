from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node

def generate_launch_description():

    config_path_arg = DeclareLaunchArgument(
        'config_path',
        default_value=PathJoinSubstitution([
            get_package_share_directory('config_pkg'),
            'config/euroc/euroc_config.yaml'
        ]),
        description='Full path to the config YAML file'
    )

    config_pkg_path = get_package_share_directory('config_pkg')

    config_path = PathJoinSubstitution([
        config_pkg_path,
        LaunchConfiguration('config_path')
    ])

    vins_path = PathJoinSubstitution([
        config_pkg_path,
        'config/../'
    ])

    support_path = PathJoinSubstitution([
        config_pkg_path,
        'support_files'
    ])

    # Sweepable parameters
    acc_n_arg = DeclareLaunchArgument('acc_n')
    gyr_n_arg = DeclareLaunchArgument('gyr_n')
    acc_w_arg = DeclareLaunchArgument('acc_w')
    gyr_w_arg = DeclareLaunchArgument('gyr_w')

    acc_n = LaunchConfiguration('acc_n')
    gyr_n = LaunchConfiguration('gyr_n')
    acc_w = LaunchConfiguration('acc_w')
    gyr_w = LaunchConfiguration('gyr_w')
    
    # Define the vins_estimator node
    vins_estimator_node = Node(
        package='vins_estimator',
        executable='vins_estimator',
        name='vins_estimator',
        namespace='vins_estimator',
        output='screen',
        parameters=[{
            'config_file': config_path,
            'vins_folder': vins_path,
            'acc_n': acc_n,
            'gyr_n': gyr_n,
            'acc_w': acc_w,
            'gyr_w': gyr_w
        }]
    )

    # Define the pose_graph node
    pose_graph_node = Node(
        package='pose_graph',
        executable='pose_graph',
        name='pose_graph',
        namespace='pose_graph',
        output='screen',
        parameters=[{
            'config_file': config_path,
            'support_file': support_path,
            'visualization_shift_x': 0,
            'visualization_shift_y': 0,
            'skip_cnt': 0,
            'skip_dis': 0.0
        }]
    )

    return LaunchDescription([
        config_path_arg,
        acc_n_arg,
        gyr_n_arg,
        acc_w_arg,
        gyr_w_arg,
        LogInfo(msg=['[vins estimator launch] config path: ', config_path]),
        LogInfo(msg=['[vins estimator launch] vins path: ', vins_path]),
        LogInfo(msg=['[vins estimator launch] support path: ', support_path]),
        vins_estimator_node,
        pose_graph_node
    ])