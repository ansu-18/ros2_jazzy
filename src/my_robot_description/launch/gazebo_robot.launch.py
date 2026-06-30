from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue

from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():

    pkg_share = get_package_share_directory(
        "my_robot_description"
    )

    xacro_file = os.path.join(
        pkg_share,
        "urdf",
        "robot_model.xacro"
    )

    world_file = os.path.join(
        pkg_share,
        "worlds",
        "robot_model_world.sdf"
    )

    robot_description = {
        "robot_description": ParameterValue(
            Command(["xacro ", xacro_file]),
            value_type=str
        )
    }

    gazebo = ExecuteProcess(
        cmd=[
            "gz",
            "sim",
            "-r",
            world_file
        ],
        output="screen"
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[
            robot_description,
            {"use_sim_time": True}
        ],
        output="screen"
    )

    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-topic",
            "robot_description",

            "-name",
            "robot_model",

            "-x", "0",
            "-y", "0",
            "-z", "0.25"
        ],
        output="screen"
    )

    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[

            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",

            "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",

            "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",

            "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",

            "/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image",

            "/camera/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo",

            "/imu@sensor_msgs/msg/Imu[gz.msgs.IMU",
        ],
        output="screen"
    )

    return LaunchDescription([

        gazebo,

        robot_state_publisher,

        bridge,

        TimerAction(
            period=5.0,
            actions=[
                spawn_robot
            ]
        ),
    ])
