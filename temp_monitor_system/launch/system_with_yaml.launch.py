import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_dir=get_package_share_directory('temp_monitor_system')
    sensor_params_file=os.path.join(pkg_dir,'config','sensor_params.yaml')
    monitor_params_file=os.path.join(pkg_dir,'config','monitor_params.yaml')

    return LaunchDescription([
        Node(
            package='temp_monitor_system',
            executable='temperature_sensor',
            name='temp_sensor',
            output='screen',
            parameters=[sensor_params_file]
        ),

        Node(
            package='temp_monitor_system',
            executable='monitor',
            name='monitor',
            output='screen',
            parameters=[monitor_params_file]
        ),

        Node(
            package='temp_monitor_system',
            executable='alert_logger',
            name='logger',
            output='screen'
        )
    ])