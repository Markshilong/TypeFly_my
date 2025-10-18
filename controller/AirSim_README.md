# AirSimWrapper 使用说明

## 概述

`AirSimWrapper` 是一个基于AirSim模拟器的无人机控制包装器，实现了与 `TelloWrapper` 和 `VirtualRobotWrapper` 相同的接口，可以在AirSim模拟环境中控制无人机。

## 功能特性

- ✅ 无人机连接和断开
- ✅ 起飞和降落
- ✅ 六自由度移动控制（前进、后退、左移、右移、上升、下降）
- ✅ 旋转控制（顺时针、逆时针）
- ✅ 摄像头视频流获取
- ✅ 悬停功能
- ✅ 位置获取
- ✅ 电池状态检查（模拟环境）

## 依赖要求

```bash
pip install airsim
pip install opencv-python
pip install numpy
```

## 使用方法

### 1. 基本使用

```python
from airsim_wrapper import AirSimWrapper

# 创建wrapper实例
drone = AirSimWrapper()

# 连接
drone.connect()

# 起飞
drone.takeoff()

# 移动
drone.move_forward(100)  # 向前移动100cm
drone.move_left(50)     # 向左移动50cm
drone.move_up(30)       # 向上移动30cm

# 旋转
drone.turn_ccw(90)      # 逆时针旋转90度

# 降落
drone.land()
```

### 2. 摄像头使用

```python
# 启动视频流
drone.start_stream()

# 获取帧读取器
frame_reader = drone.get_frame_reader()

if frame_reader:
    # 获取当前帧
    frame = frame_reader.frame
    print(f"图像尺寸: {frame.shape}")
    
    # 可以保存图像
    import cv2
    cv2.imwrite('airsim_frame.jpg', frame)

# 停止视频流
drone.stop_stream()
```

### 3. 完整飞行任务示例

```python
def flight_mission():
    drone = AirSimWrapper()
    
    try:
        # 连接和起飞
        drone.connect()
        drone.takeoff()
        
        # 执行飞行路径
        drone.move_forward(100)
        drone.turn_ccw(90)
        drone.move_forward(100)
        drone.turn_cw(90)
        drone.move_forward(100)
        
        # 悬停
        drone.hover()
        
        # 降落
        drone.land()
        
    except Exception as e:
        print(f"飞行任务失败: {e}")
        drone.land()  # 确保降落
```

## API 参考

### 连接和控制

- `connect()`: 连接到AirSim模拟器
- `takeoff() -> bool`: 起飞，返回是否成功
- `land()`: 降落
- `hover()`: 悬停

### 移动控制

- `move_forward(distance: int) -> Tuple[bool, bool]`: 向前移动
- `move_backward(distance: int) -> Tuple[bool, bool]`: 向后移动
- `move_left(distance: int) -> Tuple[bool, bool]`: 向左移动
- `move_right(distance: int) -> Tuple[bool, bool]`: 向右移动
- `move_up(distance: int) -> Tuple[bool, bool]`: 向上移动
- `move_down(distance: int) -> Tuple[bool, bool]`: 向下移动

### 旋转控制

- `turn_ccw(degree: int) -> Tuple[bool, bool]`: 逆时针旋转
- `turn_cw(degree: int) -> Tuple[bool, bool]`: 顺时针旋转

### 摄像头

- `start_stream()`: 启动视频流
- `stop_stream()`: 停止视频流
- `get_frame_reader()`: 获取帧读取器

### 状态查询

- `is_battery_good() -> bool`: 检查电池状态
- `get_position()`: 获取当前位置
- `keep_active()`: 保持连接活跃

## 配置参数

```python
# 移动距离限制
MOVEMENT_MIN = 20    # 最小移动距离 (cm)
MOVEMENT_MAX = 300   # 最大移动距离 (cm)

# 场景变化阈值
SCENE_CHANGE_DISTANCE = 120  # 距离阈值 (cm)
SCENE_CHANGE_ANGLE = 90      # 角度阈值 (度)
```

## 注意事项

1. **AirSim模拟器**: 使用前请确保AirSim模拟器正在运行
2. **坐标系**: AirSim使用右手坐标系，Z轴向下为正
3. **速度控制**: 移动速度固定为5m/s，可根据需要调整
4. **错误处理**: 所有操作都包含异常处理，确保飞行安全
5. **连接状态**: 操作前会检查连接状态，未连接时返回失败

## 测试

运行测试脚本：

```bash
python test_airsim_wrapper.py
```

运行使用示例：

```bash
python example_usage.py
```

## 与其他Wrapper的兼容性

`AirSimWrapper` 实现了与 `TelloWrapper` 和 `VirtualRobotWrapper` 相同的接口，可以在现有系统中直接替换使用：

```python
# 可以轻松切换不同的wrapper
from airsim_wrapper import AirSimWrapper
from tello_wrapper import TelloWrapper
from virtual_robot_wrapper import VirtualRobotWrapper

# 根据环境选择wrapper
if use_airsim:
    drone = AirSimWrapper()
elif use_tello:
    drone = TelloWrapper()
else:
    drone = VirtualRobotWrapper()

# 使用相同的接口
drone.connect()
drone.takeoff()
drone.move_forward(100)
drone.land()
```

## 故障排除

1. **连接失败**: 确保AirSim模拟器正在运行
2. **移动失败**: 检查距离是否在合理范围内
3. **摄像头无图像**: 确保已调用 `start_stream()`
4. **旋转不准确**: 调整旋转速度和时间参数

## 扩展功能

可以基于 `AirSimWrapper` 扩展更多功能：

- 路径规划
- 避障算法
- 图像识别
- 自动导航
- 多机协同
