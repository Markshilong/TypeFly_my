#!/usr/bin/env python3
"""
AirSimWrapper使用示例
展示如何在现有系统中使用AirSimWrapper
"""

import sys
import os
import time
import cv2

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from airsim_wrapper import AirSimWrapper
from abs.robot_wrapper import RobotType

def example_usage():
    """AirSimWrapper使用示例"""
    print("AirSimWrapper使用示例")
    print("=" * 50)
    
    # 创建AirSimWrapper实例
    drone = AirSimWrapper()
    
    try:
        # 1. 连接
        print("1. 连接到AirSim...")
        drone.connect()
        if not drone.connected:
            print("连接失败，请确保AirSim模拟器正在运行")
            return
        
        # 2. 起飞
        print("2. 起飞...")
        if not drone.takeoff():
            print("起飞失败")
            return
        
        time.sleep(2)
        
        # 3. 执行飞行任务
        print("3. 执行飞行任务...")
        
        # 向前飞行
        print("向前飞行100cm...")
        success, scene_change = drone.move_forward(100)
        print(f"结果: 成功={success}, 场景变化={scene_change}")
        
        # 向左飞行
        print("向左飞行50cm...")
        success, scene_change = drone.move_left(50)
        print(f"结果: 成功={success}, 场景变化={scene_change}")
        
        # 旋转
        print("逆时针旋转90度...")
        success, scene_change = drone.turn_ccw(90)
        print(f"结果: 成功={success}, 场景变化={scene_change}")
        
        # 继续向前
        print("继续向前飞行80cm...")
        success, scene_change = drone.move_forward(80)
        print(f"结果: 成功={success}, 场景变化={scene_change}")
        
        # 4. 获取摄像头图像
        print("4. 启动摄像头...")
        drone.start_stream()
        frame_reader = drone.get_frame_reader()
        
        if frame_reader:
            print("获取摄像头图像...")
            frame = frame_reader.frame
            print(f"图像尺寸: {frame.shape}")
            # # 这里可以保存图像或进行图像处理
            # cv2.imwrite('airsim_frame.jpg', frame)
        
        # 5. 悬停
        print("5. 悬停...")
        drone.hover()
        time.sleep(3)
        
        # 6. 降落
        print("6. 降落...")
        drone.land()
        
        # 7. 停止视频流
        drone.stop_stream()
        
        print("飞行任务完成！")
        
    except Exception as e:
        print(f"执行过程中出现错误: {e}")
        # 确保降落
        try:
            drone.land()
        except:
            pass

def compare_wrappers():
    """比较不同wrapper的使用方式"""
    print("\n" + "=" * 50)
    print("Wrapper使用方式比较")
    print("=" * 50)
    
    # 展示不同wrapper的相同接口
    wrappers = {
        "AirSim": AirSimWrapper(),
        # "Tello": TelloWrapper(),  # 需要实际Tello无人机
        # "Virtual": VirtualRobotWrapper(),  # 虚拟wrapper
    }
    
    for name, wrapper in wrappers.items():
        print(f"\n{name} Wrapper:")
        print(f"  - 类型: {type(wrapper).__name__}")
        print(f"  - 继承自: {type(wrapper).__bases__[0].__name__}")
        print(f"  - 方法: {[method for method in dir(wrapper) if not method.startswith('_')]}")

if __name__ == "__main__":
    print("AirSimWrapper使用示例")
    print("请确保AirSim模拟器正在运行")
    print("按Enter键开始...")
    input()
    
    # 运行使用示例
    example_usage()
    
    # 比较不同wrapper
    compare_wrappers()
