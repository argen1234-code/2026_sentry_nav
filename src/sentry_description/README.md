# sentry_description

实车使用的机器人描述包。它在启动时展开迁移后的
`pb2025_sentry_robot.sdf.xmacro`，再转换为 URDF，由
`robot_state_publisher` 发布旧工程同名的模型 TF 和关节语义。

```bash
colcon build --symlink-install --packages-up-to sentry_description
source install/setup.bash
ros2 launch sentry_description description.launch.py use_rviz:=true
```

关键坐标系：`base_footprint -> chassis -> gimbal_yaw -> front_mid360`。
雷达驱动使用的 `front_mid360` 与该包保持一致。
