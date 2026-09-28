# sentry_model_resources

This package contains the competition robot model migrated from the reference
workspace. The `resource/xmacro/pb2025_sentry_robot.sdf.xmacro` source is
expanded at launch and converted to URDF for `robot_state_publisher`.

The model resource directory is self-contained. It does not require the old
workspace or a Gazebo installation when used by the real-robot description
launch.
