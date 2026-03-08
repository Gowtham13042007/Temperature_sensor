from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument,LogInfo
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration

def generate_launch_description():

    user_logger_arg=DeclareLaunchArgument(
        'use_logger',
        default_value='true',
        description='Whether to start the alert logger node'
    )

    rate_arg=DeclareLaunchArgument(
        'rate',
        default_value='2.0',
        description='Temperature sensor publish rate (Hz)'
    )

    threshold_arg=DeclareLaunchArgument(
        'threshold',
        default_value='28.0',
        description='Temperature threshold for alerts(°C)'
    )

    use_logger=LaunchConfiguration('use_logger')
    rate=LaunchConfiguration('rate')
    threshold=LaunchConfiguration('threshold')

    return LaunchDescription([
        user_logger_arg,
        rate_arg,
        threshold_arg,

        LogInfo(msg=['Launching temperature monitoring system...']),
        LogInfo(msg=['Sensor rate: ', rate, ' Hz']),
        LogInfo(msg=['Alert threshold: ', threshold, ' °C']),

        Node(
            package='temp_monitor_system',
            executable='temperature_sensor',
            name='temp_sensor',
            output='screen',
            parameters=[
                {
                    'publish_rate':rate,
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
                    'temp_threshold':threshold
                }
            ]
            
        ),

        Node(
            package='temp_monitor_system',
            executable='alert_logger',
            name='logger',
            output='screen',
            condition=IfCondition(use_logger)
        )
        
    ])
