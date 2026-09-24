# 2026 Sentry Workspace

按职责分层的 ROS 2 导航工程：

```text
sentry_interfaces   自定义消息和服务
sentry_description  URDF/Xacro 和 TF
sentry_hardware     雷达、底盘和裁判系统接入
sentry_localization Point-LIO、SLAM 和重定位
sentry_perception   地形、障碍物和点云处理
sentry_navigation   Nav2 插件、控制器和行为树
sentry_decision     比赛决策
sentry_bringup      实车一键启动和 RViz2 可视化
```

系统入口：

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch sentry_bringup sentry.launch.py mode:=localization
```

建图时使用 `mode:=mapping`。场地资源和集中配置位于 `config/`，第三方依赖版本
记录在 `third_party.repos`。
