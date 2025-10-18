#!/usr/bin/env python3
"""
测试AirSim摄像头分辨率配置
"""
import airsim
import numpy as np
import cv2
import os

def test_camera_resolution():
    """测试摄像头分辨率是否为1280x720"""
    try:
        # 连接到AirSim
        client = airsim.MultirotorClient()
        client.confirmConnection()
        print("已连接到AirSim")
        
        # 获取图像
        responses = client.simGetImages([
            airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)
        ])
        
        if responses and len(responses) > 0:
            response = responses[0]
            print(f"图像宽度: {response.width}")
            print(f"图像高度: {response.height}")
            
            # 检查分辨率是否为1280x720
            if response.width == 1280 and response.height == 720:
                print("✅ 摄像头分辨率已成功设置为1280x720")
                
                # 保存测试图像
                img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)
                img_rgb = img1d.reshape(response.height, response.width, 3)
                
                # 创建测试图像目录
                test_dir = "test_images"
                if not os.path.exists(test_dir):
                    os.makedirs(test_dir)
                
                # 保存图像
                cv2.imwrite(f"{test_dir}/test_1280x720.jpg", cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR))
                print(f"测试图像已保存到: {test_dir}/test_1280x720.jpg")
                
                return True
            else:
                print(f"❌ 摄像头分辨率不正确，当前为: {response.width}x{response.height}")
                return False
        else:
            print("❌ 无法获取图像")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    print("开始测试AirSim摄像头分辨率...")
    print("请确保AirSim正在运行并且settings.json文件已正确配置")
    test_camera_resolution()
