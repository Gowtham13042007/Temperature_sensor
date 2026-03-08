from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import TimerAction

def generate_launch_description():
    """
    Launch system with namespace and topic remapping.
    This demonstrates how to run multiple instances without conflicts.
    """
    
    return LaunchDescription([
        Node(
            package='temp_monitor_system',
            executable='temperature_sensor',
            name='temp_sensor',
            namespace='robot1',  
            output='screen',
            parameters=[
                {'publish_rate': 2.0}
            ],
            arguments=['--ros-args', '--log-level', 'DEBUG']
        ),                                                                                                                    
        
        Node(
            package='temp_monitor_system',
            executable='monitor',
            name='monitor',
            namespace='robot1',
            output='screen',
            remappings=[
                ('temperature', '/robot1/temperature')   
            ]
        ),
        
      
        Node(
            package='temp_monitor_system',
            executable='temperature_sensor',
            name='temp_sensor',
            namespace='robot2',
            output='screen',
            parameters=[{'publish_rate': 3.0, 'base_temp': 30.0}]
        ),
        
        Node(
            package='temp_monitor_system',
            executable='monitor',
            name='monitor',
            namespace='robot2',
            output='screen',
            remappings=[
                ('temperature', '/robot2/temperature'),
            ]
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen'
        ),

        TimerAction(
            period=2.0,
            actions=[
                Node(
                    package='temp_monitor_system',
                    executable='alert_logger',
                    name='logger',
                    namespace="robot1",
                    output='screen',
                )
            ]
        )
        
    ])