"""Complete real-robot startup matching the competition desktop script."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    GroupAction,
    IncludeLaunchDescription,
    TimerAction,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterFile
from nav2_common.launch import ReplaceString, RewrittenYaml


def include(package, filename, arguments=None, condition=None):
    path = os.path.join(get_package_share_directory(package), "launch", filename)
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource(path),
        launch_arguments=(arguments or {}).items(),
        condition=condition,
    )


def generate_launch_description():
    nav_share = get_package_share_directory("pb2025_nav_bringup")
    decision_share = get_package_share_directory("sentry_decision")
    params_file = os.path.join(nav_share, "config", "reality", "nav2_params.yaml")
    # Preserve the old bringup's root-namespace substitution for costmap topics.
    resolved_params = ReplaceString(
        source_file=params_file, replacements={"<robot_namespace>": ""}
    )
    use_sim_time = LaunchConfiguration("use_sim_time")
    autostart = LaunchConfiguration("autostart")
    configured_params = ParameterFile(
        RewrittenYaml(
            source_file=resolved_params, root_key="",
            param_rewrites={"use_sim_time": use_sim_time, "autostart": autostart},
            convert_types=True,
        ), allow_substs=True,
    )

    return LaunchDescription([
        DeclareLaunchArgument("use_sim_time", default_value="false"),
        DeclareLaunchArgument("autostart", default_value="true"),
        DeclareLaunchArgument("use_rviz", default_value="true"),
        DeclareLaunchArgument("udp_port", default_value="19002"),
        DeclareLaunchArgument("referee_device", default_value="/dev/ttyACM0"),
        # Keep the description RViz disabled without overwriting this
        # bringup's own use_rviz launch configuration.
        GroupAction(
            actions=[
                include("sentry_description", "description.launch.py", {
                    "use_sim_time": use_sim_time,
                    "use_rviz": "false",
                }),
            ],
            scoped=True,
        ),
        include("sentry_hardware", "lidar.launch.py", {"frame_id": "front_mid360"}),
        Node(package="rclcpp_components", executable="component_container_isolated",
             name="nav2_container", output="screen",
             parameters=[configured_params, {"autostart": autostart}]),
        include("sentry_localization", "mapping.launch.py", {
            "params_file": resolved_params, "use_sim_time": use_sim_time,
            "autostart": autostart,
        }),
        include("pb2025_nav_bringup", "navigation_launch.py", {
            "params_file": resolved_params, "use_sim_time": use_sim_time,
            "autostart": autostart, "use_composition": "True",
            "container_name": "nav2_container",
        }),
        include("pb2025_nav_bringup", "joy_teleop_launch.py", {
            "joy_config_file": resolved_params, "use_sim_time": use_sim_time,
        }),
        Node(package="rviz2", executable="rviz2", name="rviz2", output="screen",
             condition=IfCondition(LaunchConfiguration("use_rviz")),
             arguments=["-d", os.path.join(nav_share, "rviz", "nav2_default_view.rviz")]),
        # The desktop script starts these three processes three seconds after navigation.
        TimerAction(period=3.0, actions=[
            Node(package="extra_cmd", executable="cmd_vel_to_udp", name="cmd_vel_to_udp",
                 output="screen", parameters=[{"udp_ip": "0.0.0.0",
                                               "udp_port": LaunchConfiguration("udp_port")}]),
            Node(package="referee_serial_bridge", executable="referee_serial_bridge_node",
                 name="referee_serial_bridge", output="screen",
                 parameters=[{"device": LaunchConfiguration("referee_device")}]),
            include("sentry_decision", "sentry_decision_launch.py", {
                "params_file": os.path.join(decision_share, "config", "sentry_decision_params.yaml"),
            }),
        ]),
    ])
