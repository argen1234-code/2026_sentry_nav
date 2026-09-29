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
（原脚本参数 `0.0.0.0:19002`）、裁判桥和决策。默认启动 RViz，
`visualization:=headless` 关闭可视化（旧参数 `use_rviz:=false` 仍兼容）。
按 Ctrl+C 停止整个 launch；
不要同时启动旧桌面脚本，否则节点名、传感器端口和底盘指令会冲突。

代码、模型、导航和决策参数都从本工作空间读取。主要实车参数在
`src/sentry_navigation/pb2025_nav_bringup/config/reality/nav2_params.yaml`，
决策参数在 `src/sentry_decision/config/sentry_decision_params.yaml`。
`src/sentry_bringup/launch/sentry.launch.py` 是本次桌面脚本范围内的统一入口；
其他单包 launch 可用于分层调试，不是完整比赛启动。

可视化模式通过 launch 启动参数选择（这里不是 C/C++ 意义上的宏定义）：

```bash
# RViz2，默认模式；保留目标点工具和规划路径显示
./scripts/start_sentry.sh visualization:=rviz

# 无图形界面，适合机器人端或性能受限环境
./scripts/start_sentry.sh visualization:=headless

# Foxglove Bridge，不启动 RViz2
./scripts/start_sentry.sh visualization:=foxglove
```

本机桌面还有对应的 `2026哨兵导航-RViz.desktop`、
`2026哨兵导航-Foxglove.desktop` 和 `2026哨兵导航-无显示.desktop` 双击入口。
这些桌面文件位于工作空间之外，不包含在本仓库中；换电脑部署时使用上述命令。
三种模式会启动同一套实车节点，不能同时运行。桌面入口打开终端后，
在终端按 Ctrl+C 即可停止。

Foxglove 模式首次使用需要安装桥接包（只需安装一次）。桥接默认监听
`0.0.0.0:8765`，允许同一网络的设备连接；只允许本机访问时传入
`foxglove_address:=127.0.0.1`，请勿将该端口暴露到公网：

```bash
sudo apt install ros-humble-foxglove-bridge
```

启动后，在 Foxglove Dashboard
[`2ca5dad3`](https://app.foxglove.dev/2ca5dad3/dashboard) 选择 WebSocket 连接：

```text
ws://127.0.0.1:8765       # Foxglove 在机器人本机运行
ws://机器人IP:8765         # Foxglove 在局域网另一台电脑运行
```

Foxglove 3D 面板可使用以下数据源显示机器人状态：

```text
模型       /robot_description
TF         /tf 和 /tf_static
点云       /livox/lidar/pointcloud（或 /terrain_map_ext）
地图       /map
全局代价图 /global_costmap/costmap
局部代价图 /local_costmap/costmap
全局路径   /plan
局部路径   /local_plan
```

首次连接后，在 3D 面板中选择固定坐标系 `map`，手动开启所需的话题图层；
只看见模型和网格时先检查图层是否开启。`/terrain_map_ext` 使用 `odom` 坐标系，
适合查看处理后的点云；`/livox/lidar/pointcloud` 使用雷达坐标系。
`/cloud_registered` 使用 `camera_init` 坐标系，当前与 `map` 没有可用 TF，
不建议直接在 `map` 视角显示。`/plan` 和 `/local_plan` 只有产生导航规划后才有路径。

RViz 配置中的 `GoalTool` 和 `SetInitialPose` 已启用，仍可直接设置目标点和初始位姿；
Foxglove 侧支持显示路径，但当前工程的目标点由 Nav2 `navigate_to_pose` Action 接收，
仅向 `/goal_pose` 发布消息不会发起导航。Foxglove Dashboard 的布局属于云端配置，
本工程提供桥接和话题，不能从本地代码直接修改该网页布局。

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
