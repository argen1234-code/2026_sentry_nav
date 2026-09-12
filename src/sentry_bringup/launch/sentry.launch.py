import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import LaunchConfigurationEquals, LaunchConfigurationNotEquals
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def include(package, launch_file, arguments=None, condition=None):
    source = os.path.join(get_package_share_directory(package), "launch", launch_file)
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource(source),
        launch_arguments=(arguments or {}).items(),
        condition=condition,
    )


def generate_launch_description():
    mode = LaunchConfiguration("mode")
    nav_params = os.path.join(
        get_package_share_directory("pb2025_nav_bringup"),
        "config", "reality", "nav2_params.yaml",
    )
    return LaunchDescription([
        DeclareLaunchArgument("mode", default_value="localization", description="mapping or localization"),
        DeclareLaunchArgument("use_sim_time", default_value="false"),
        include("sentry_hardware", "lidar.launch.py", {"frame_id": "front_mid360"}),
        include("sentry_description", "description.launch.py", {"use_sim_time": LaunchConfiguration("use_sim_time")}),
        include("sentry_perception", "perception.launch.py"),
        include("sentry_localization", "mapping.launch.py", condition=LaunchConfigurationEquals("mode", "mapping")),
        include("sentry_localization", "localization.launch.py", condition=LaunchConfigurationNotEquals("mode", "mapping")),
        include("pb2025_nav_bringup", "navigation_launch.py", {"params_file": nav_params, "use_sim_time": LaunchConfiguration("use_sim_time")}),
    ])
