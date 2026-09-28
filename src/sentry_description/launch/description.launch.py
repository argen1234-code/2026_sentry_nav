"""Publish the competition robot TF tree from the migrated SDF xmacro."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchContext, LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, OpaqueFunction, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterFile
from nav2_common.launch import RewrittenYaml
from sdformat_tools.urdf_generator import UrdfGenerator
from sdformat_tools.xmacro4sdf import XMLMacro4sdf


def launch_setup(context: LaunchContext):
    model_share = get_package_share_directory("sentry_model_resources")
    model_root = os.path.join(model_share, "resource", "models")
    # sdformat_tools resolves model:// URIs through this workspace-local root.
    os.environ["SENTRY_MODEL_PATH"] = model_root

    xmacro = XMLMacro4sdf()
    xmacro.set_xml_file(context.launch_configurations["robot_xmacro_file"])
    xmacro.generate()

    urdf_generator = UrdfGenerator()
    urdf_generator.parse_from_sdf_string(xmacro.to_string())
    robot_description = urdf_generator.to_string()

    namespace = LaunchConfiguration("namespace")
    params_file = LaunchConfiguration("params_file")
    configured_params = ParameterFile(
        RewrittenYaml(
            source_file=params_file,
            root_key=namespace,
            param_rewrites={"use_sim_time": LaunchConfiguration("use_sim_time")},
            convert_types=True,
        ),
        allow_substs=True,
    )

    return [
        SetEnvironmentVariable("SENTRY_MODEL_PATH", model_root),
        GroupAction(
            [
                Node(
                    package="joint_state_publisher",
                    executable="joint_state_publisher",
                    name="joint_state_publisher",
                    output="screen",
                    respawn=LaunchConfiguration("use_respawn"),
                    respawn_delay=2.0,
                    parameters=[configured_params],
                    arguments=["--ros-args", "--log-level", LaunchConfiguration("log_level")],
                ),
                Node(
                    package="robot_state_publisher",
                    executable="robot_state_publisher",
                    name="robot_state_publisher",
                    output="screen",
                    respawn=LaunchConfiguration("use_respawn"),
                    respawn_delay=2.0,
                    parameters=[configured_params, {"robot_description": robot_description}],
                    arguments=["--ros-args", "--log-level", LaunchConfiguration("log_level")],
                ),
                Node(
                    condition=IfCondition(LaunchConfiguration("use_rviz")),
                    package="rviz2",
                    executable="rviz2",
                    name="robot_model_rviz",
                    output="screen",
                    arguments=["-d", LaunchConfiguration("rviz_config_file")],
                ),
            ]
        ),
    ]


def generate_launch_description():
    model_share = get_package_share_directory("sentry_model_resources")
    description_share = get_package_share_directory("sentry_description")
    return LaunchDescription([
        DeclareLaunchArgument("namespace", default_value=""),
        DeclareLaunchArgument("use_sim_time", default_value="false"),
        DeclareLaunchArgument("robot_name", default_value="pb2025_sentry_robot"),
        DeclareLaunchArgument(
            "robot_xmacro_file",
            default_value=[
                TextSubstitution(text=os.path.join(model_share, "resource", "xmacro", "")),
                LaunchConfiguration("robot_name"),
                TextSubstitution(text=".sdf.xmacro"),
            ],
        ),
        DeclareLaunchArgument(
            "params_file",
            default_value=os.path.join(description_share, "config", "robot_state_publisher.yaml"),
        ),
        DeclareLaunchArgument(
            "rviz_config_file",
            default_value=os.path.join(description_share, "rviz", "sentry_description.rviz"),
        ),
        DeclareLaunchArgument("use_rviz", default_value="false"),
        DeclareLaunchArgument("use_respawn", default_value="false"),
        DeclareLaunchArgument("log_level", default_value="info"),
        OpaqueFunction(function=launch_setup),
    ])
