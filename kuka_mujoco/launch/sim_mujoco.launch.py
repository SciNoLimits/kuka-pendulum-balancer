from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution


def generate_launch_description():
    description_share = FindPackageShare("kuka_mujoco")

    xacro_file = PathJoinSubstitution([
        description_share,
        "urdf",
        "kuka_mujoco.urdf.xacro",
    ])

    controllers_file = PathJoinSubstitution([
        description_share,
        "config",
        "controllers.yaml",
    ])


    robot_description = {
        "robot_description": ParameterValue(
            Command(["xacro ", xacro_file]),
            value_type=str,
        )
    }

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            robot_description,
            {"use_sim_time": True},
        ],
    )

    control_node = Node(
        package="mujoco_ros2_control",
        executable="ros2_control_node",
        name="controller_manager",
        output="both",
        emulate_tty=True,
        parameters=[
            {"use_sim_time": True},
            controllers_file,
        ],
    )

    joint_state_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--param-file",
            controllers_file,
        ],
        output="screen",
    )

    iiwa_torque_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "iiwa_torque_controller",
            "--param-file",
            controllers_file,
        ],
        output="screen",
    )

    return LaunchDescription([
        robot_state_publisher,
        control_node,
        joint_state_spawner,
        iiwa_torque_controller_spawner,
    ])