# sentry_description

实车使用的最小机器人描述包。它只负责发布导航所需的 TF，不依赖 Gazebo、SDF
宏生成器或外观模型资源。

```bash
colcon build --symlink-install --packages-up-to sentry_description
source install/setup.bash
ros2 launch sentry_description description.launch.py
```

关键坐标系：`base_footprint -> chassis -> gimbal_yaw -> front_mid360`。
雷达驱动使用的 `front_mid360` 与该包保持一致。
