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

旧桌面脚本的实车建图入口（新工作空间独立运行，不需要旧工作空间）：

```bash
cd /home/gzu-prink/2026_sentry_ws
bash scripts/start_sentry.sh
```

入口固定为旧桌面脚本的 `slam:=True use_robot_state_pub:=True` 建图配置。
启动顺序：模型与动态关节、MID360、Nav2 组件容器、Point-LIO + SLAM Toolbox
及地图保存、点云转激光、地形分析和导航、摇杆；3 秒后启动底盘 UDP 桥
（原脚本参数 `0.0.0.0:19002`）、裁判桥和决策。默认启动 RViz，可传
`use_rviz:=false` 关闭。按 Ctrl+C 停止整个 launch；
不要同时启动旧桌面脚本，否则节点名、传感器端口和底盘指令会冲突。

代码、模型、导航和决策参数都从本工作空间读取。主要实车参数在
`src/sentry_navigation/pb2025_nav_bringup/config/reality/nav2_params.yaml`，
决策参数在 `src/sentry_decision/config/sentry_decision_params.yaml`。
`src/sentry_bringup/launch/sentry.launch.py` 是本次桌面脚本范围内的统一入口；
其他单包 launch 可用于分层调试，不是完整比赛启动。
启动脚本使用 `install/local_setup.bash`，避免旧构建遗留的
`install/setup.bash` 父级环境重新注入旧工作空间。

首次使用需在不加载旧工作空间的终端单独编译，例如：

```bash
source /opt/ros/humble/setup.bash
colcon build --symlink-install --parallel-workers 1
```

实车运行前请核对雷达网卡地址、串口权限及底盘安全状态；没有实际传感器和
底盘连接时，进程能够拉起并不代表建图、裁判通信或自主运动已验证。
建图模式会按旧参数将 Point-LIO 点云写入
`src/sentry_localization/point_lio/PCD/`，需要保留地图时请另行备份。
