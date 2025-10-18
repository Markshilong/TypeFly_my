import time
import cv2
import numpy as np
from typing import Tuple
import airsim

from .abs.robot_wrapper import RobotWrapper

# 移动距离限制
MOVEMENT_MIN = 20
MOVEMENT_MAX = 300

# 场景变化阈值
SCENE_CHANGE_DISTANCE = 120
SCENE_CHANGE_ANGLE = 90

def cap_distance(distance):
    """限制移动距离在合理范围内"""
    if distance < MOVEMENT_MIN:
        return MOVEMENT_MIN
    elif distance > MOVEMENT_MAX:
        return MOVEMENT_MAX
    return distance

class FrameReader:
    """AirSim摄像头帧读取器"""
    def __init__(self, client):
        self.client = client

    @property
    def frame(self):
        """获取当前帧"""
        # 获取场景图像
        responses = self.client.simGetImages([
            airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)
        ])
        
        if responses and len(responses) > 0:
            response = responses[0]
            # 将图像数据转换为numpy数组
            img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)
            img_rgb = img1d.reshape(response.height, response.width, 3)
            return img_rgb
        else:
            # 如果无法获取图像，返回黑色图像
            return np.zeros((480, 640, 3), dtype=np.uint8)

class AirSimWrapper(RobotWrapper):
    """AirSim无人机控制包装器"""
    
    def __init__(self):
        self.client = None
        self.stream_on = False
        self.connected = False

    def keep_active(self):
        """保持连接活跃"""
        if self.connected:
            # AirSim连接通常比较稳定，不需要特殊处理
            pass

    def connect(self):
        """连接到AirSim"""
        try:
            self.client = airsim.MultirotorClient()
            self.client.confirmConnection()
            self.client.enableApiControl(True)
            self.connected = True
            print("已连接到AirSim")
        except Exception as e:
            print(f"连接AirSim失败: {e}")
            self.connected = False

    def takeoff(self) -> bool:
        """起飞"""
        if not self.connected:
            print("未连接到AirSim")
            return False
        
        try:
            self.client.armDisarm(True)
            self.client.takeoffAsync().join()
            print("无人机已起飞")
            return True
        except Exception as e:
            print(f"起飞失败: {e}")
            return False

    def land(self):
        """降落"""
        if not self.connected:
            return
        
        try:
            self.client.landAsync().join()
            self.client.armDisarm(False)
            print("无人机已降落")
        except Exception as e:
            print(f"降落失败: {e}")

    def start_stream(self):
        """开始视频流"""
        self.stream_on = True
        print("AirSim视频流已启动")

    def stop_stream(self):
        """停止视频流"""
        self.stream_on = False
        print("AirSim视频流已停止")

    def get_frame_reader(self):
        """获取帧读取器"""
        if not self.stream_on or not self.connected:
            return None
        return FrameReader(self.client)

    def move_forward(self, distance: int) -> Tuple[bool, bool]:
        """向前移动"""
        if not self.connected:
            return False, False
        
        try:
            distance = cap_distance(distance)
            # 在AirSim中，正X轴是向前
            self.client.moveByVelocityAsync(5, 0, 0, distance/100).join()  # 速度5m/s，时间distance/100秒
            self.movement_x_accumulator += distance
            time.sleep(0.5)
            return True, distance > SCENE_CHANGE_DISTANCE
        except Exception as e:
            print(f"向前移动失败: {e}")
            return False, False

    def move_backward(self, distance: int) -> Tuple[bool, bool]:
        """向后移动"""
        if not self.connected:
            return False, False
        
        try:
            distance = cap_distance(distance)
            # 在AirSim中，负X轴是向后
            self.client.moveByVelocityAsync(-5, 0, 0, distance/100).join()
            self.movement_x_accumulator -= distance
            time.sleep(0.5)
            return True, distance > SCENE_CHANGE_DISTANCE
        except Exception as e:
            print(f"向后移动失败: {e}")
            return False, False

    def move_left(self, distance: int) -> Tuple[bool, bool]:
        """向左移动"""
        if not self.connected:
            return False, False
        
        try:
            distance = cap_distance(distance)
            # 在AirSim中，正Y轴是向左
            self.client.moveByVelocityAsync(0, 5, 0, distance/100).join()
            self.movement_y_accumulator += distance
            time.sleep(0.5)
            return True, distance > SCENE_CHANGE_DISTANCE
        except Exception as e:
            print(f"向左移动失败: {e}")
            return False, False

    def move_right(self, distance: int) -> Tuple[bool, bool]:
        """向右移动"""
        if not self.connected:
            return False, False
        
        try:
            distance = cap_distance(distance)
            # 在AirSim中，负Y轴是向右
            self.client.moveByVelocityAsync(0, -5, 0, distance/100).join()
            self.movement_y_accumulator -= distance
            time.sleep(0.5)
            return True, distance > SCENE_CHANGE_DISTANCE
        except Exception as e:
            print(f"向右移动失败: {e}")
            return False, False

    def move_up(self, distance: int) -> Tuple[bool, bool]:
        """向上移动"""
        if not self.connected:
            return False, False
        
        try:
            distance = cap_distance(distance)
            # 在AirSim中，负Z轴是向上
            self.client.moveByVelocityAsync(0, 0, -5, distance/100).join()
            time.sleep(0.5)
            return True, False
        except Exception as e:
            print(f"向上移动失败: {e}")
            return False, False

    def move_down(self, distance: int) -> Tuple[bool, bool]:
        """向下移动"""
        if not self.connected:
            return False, False
        
        try:
            distance = cap_distance(distance)
            # 在AirSim中，正Z轴是向下
            self.client.moveByVelocityAsync(0, 0, 5, distance/100).join()
            time.sleep(0.5)
            return True, False
        except Exception as e:
            print(f"向下移动失败: {e}")
            return False, False

    def turn_ccw(self, degree: int) -> Tuple[bool, bool]:
        """逆时针旋转"""
        if not self.connected:
            return False, False
        
        try:
            # 使用yaw控制旋转
            self.client.rotateByYawRateAsync(degree/2, 2).join()  # 2秒内完成旋转
            self.rotation_accumulator += degree
            time.sleep(1)
            return True, False
        except Exception as e:
            print(f"逆时针旋转失败: {e}")
            return False, False

    def turn_cw(self, degree: int) -> Tuple[bool, bool]:
        """顺时针旋转"""
        if not self.connected:
            return False, False
        
        try:
            # 使用yaw控制旋转，负值表示顺时针
            self.client.rotateByYawRateAsync(-degree/2, 2).join()  # 2秒内完成旋转
            self.rotation_accumulator -= degree
            time.sleep(1)
            return True, False
        except Exception as e:
            print(f"顺时针旋转失败: {e}")
            return False, False

    def is_battery_good(self) -> bool:
        """检查电池状态（AirSim中总是返回True）"""
        print("> AirSim模拟环境，电池状态: 100% [OK]")
        return True

    def get_position(self):
        """获取当前位置"""
        if not self.connected:
            return None
        
        try:
            state = self.client.getMultirotorState()
            return state.kinematics_estimated.position
        except Exception as e:
            print(f"获取位置失败: {e}")
            return None

    def hover(self):
        """悬停"""
        if not self.connected:
            return
        
        try:
            self.client.hoverAsync().join()
            print("无人机已悬停")
        except Exception as e:
            print(f"悬停失败: {e}")
