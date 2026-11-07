from launch import LaunchDescription
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    description_share = FindPackageShare("lbr_iiwa14_r820_description")
