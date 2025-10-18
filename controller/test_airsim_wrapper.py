#!/usr/bin/env python3
"""
AirSimWrapper测试脚本
使用前请确保AirSim模拟器正在运行
"""

import sys
import os
import time

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from airsim_wrapper import AirSimWrapper

def test_airsim_wrapper():
    """测试AirSimWrapper的基本功能"""
    print("开始测试AirSimWrapper...")
    
    # 创建wrapper实例
    wrapper = AirSimWrapper()
    
    try:
        # 测试连接
        print("1. 测试连接...")
        wrapper.connect()
        if not wrapper.connected:
            print("连接失败，请确保AirSim模拟器正在运行")
            return False
        
        # 测试起飞
        print("2. 测试起飞...")
        if wrapper.takeoff():
            print("起飞成功")
        else:
            print("起飞失败")
            return False
        
        # 等待一下
        time.sleep(2)
        
        # 测试移动
        print("3. 测试移动...")
        print("向前移动50cm...")
        success, scene_change = wrapper.move_forward(50)
        print(f"移动结果: 成功={success}, 场景变化={scene_change}")
        
        time.sleep(1)
        
        print("向左移动30cm...")
        success, scene_change = wrapper.move_left(30)
        print(f"移动结果: 成功={success}, 场景变化={scene_change}")
        
        time.sleep(1)
        
        print("向上移动20cm...")
        success, scene_change = wrapper.move_up(20)
        print(f"移动结果: 成功={success}, 场景变化={scene_change}")
        
        time.sleep(1)
        
        # 测试旋转
        print("4. 测试旋转...")
        print("逆时针旋转45度...")
        success, scene_change = wrapper.turn_ccw(45)
        print(f"旋转结果: 成功={success}, 场景变化={scene_change}")
        
        time.sleep(1)
        
        print("顺时针旋转90度...")
        success, scene_change = wrapper.turn_cw(90)
        print(f"旋转结果: 成功={success}, 场景变化={scene_change}")
        
        time.sleep(1)
        
        # 测试摄像头
        print("5. 测试摄像头...")
        wrapper.start_stream()
        frame_reader = wrapper.get_frame_reader()
        if frame_reader:
            print("摄像头流启动成功")
            # 获取一帧图像
            frame = frame_reader.frame
            print(f"获取到图像，尺寸: {frame.shape}")
        else:
            print("摄像头流启动失败")
        
        # 测试悬停
        print("6. 测试悬停...")
        wrapper.hover()
        time.sleep(2)
        
        # 测试降落
        print("7. 测试降落...")
        wrapper.land()
        time.sleep(2)
        
        # 停止视频流
        wrapper.stop_stream()
        
        print("所有测试完成！")
        return True
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        return False
    
    finally:
        # 确保降落
        try:
            wrapper.land()
        except:
            pass

if __name__ == "__main__":
    print("AirSimWrapper测试脚本")
    print("请确保AirSim模拟器正在运行，然后按Enter键开始测试...")
    input()
    
    success = test_airsim_wrapper()
    if success:
        print("测试成功完成！")
    else:
        print("测试失败，请检查AirSim模拟器是否正在运行")
