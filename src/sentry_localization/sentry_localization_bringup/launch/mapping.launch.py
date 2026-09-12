import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    share = get_package_share_directory("sentry_localization")
    point_lio_params = os.path.join(share, "config", "point_lio_mid360.yaml")
    slam_params = os.path.join(share, "config", "slam_toolbox.yaml")
    return LaunchDescription([
        DeclareLaunchArgument("use_sim_time", default_value="false"),
        Node(package="point_lio", executable="pointlio_mapping", name="point_lio", output="screen", parameters=[point_lio_params]),
        Node(package="slam_toolbox", executable="sync_slam_toolbox_node", name="slam_toolbox", output="screen", parameters=[slam_params], remappings=[("/map", "map"), ("/map_metadata", "map_metadata"), ("/map_updates", "map_updates")]),
    ])
