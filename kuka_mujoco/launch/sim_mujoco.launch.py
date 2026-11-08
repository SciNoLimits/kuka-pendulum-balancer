import os
from launch import LaunchDescription
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # 1. Locate package directories
    package_share = FindPackageShare("kuka_mujoco")

    # 2. Define file paths for your Xacro and Controllers YAML
    xacro_file = PathJoinSubstitution([
        package_share,
        "urdf",
        "kuka_mujoco.urdf.xacro",
    ])
    
    controllers_yaml = PathJoinSubstitution([
        package_share,
        "config",
        "controllers.yaml",
    ])

    # 3. Render Xacro to URDF String
    robot_description_content = Command(["xacro ", xacro_file])
    robot_description = {
        "robot_description": ParameterValue(
            robot_description_content,
            value_type=str,
        )
    }

    # 4. Standard Robot State Publisher (Publishes raw URDF to /robot_description)
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

    # 5. Runtime URDF to MJCF Translation Converter Node (Crucial Step)
    robot_description_to_mjcf = Node(
        package="mujoco_ros2_control",
        executable="robot_description_to_mjcf.sh",
        output="both",
        emulate_tty=True,
        arguments=[
            "--publish_topic", "/mujoco_robot_description",
        ],
    )

    # 6. Corrected MuJoCo Control Node (Uses dedicated simulation executable)
    control_node = Node(
        package="mujoco_ros2_control",
        executable="ros2_control_node", 
        output="both",
        parameters=[
            controllers_yaml, 
            {"use_sim_time": True},
        ],
    )

    # 7. Joint State Broadcaster Spawner
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
        output="screen",
    )

    # 8. Main Arm Trajectory Controller Spawner
    iiwa_arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["iiwa_arm_controller"],
        output="screen",
    )

    return LaunchDescription([
        robot_state_publisher,
        robot_description_to_mjcf,  # Spins up the dynamic converter bridge
        control_node,
        joint_state_broadcaster_spawner,
        iiwa_arm_controller_spawner,
    ])
