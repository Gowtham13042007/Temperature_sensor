from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='temp_monitor_system',
            executable='temperature_sensor',
            name='temp_sensor',
            output='screen',
            parameters=[
                {
                    'publish_rate':2.0,
                    'base_temp':25.0,
                    'temp_variation':5.0
                }
            ]
        ),

        Node(
            package='temp_monitor_system',
            executable='monitor',
            name='monitor',
            output='screen',
            parameters=[
                {
                    'temp_threshold':28.0
                }
            ]
        ),

        Node(
            package='temp_monitor_system',
            executable='alert_logger',
            name='logger',
            output='screen'
        )
    ])