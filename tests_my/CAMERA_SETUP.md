# AirSim摄像头分辨率配置说明

## 概述
本文档说明如何将AirSim无人机的摄像头分辨率从默认的256x144调整为1280x720。

## 配置文件
已创建 `settings.json` 文件，包含以下配置：

### 摄像头设置
- **分辨率**: 1280x720 (从默认的256x144调整)
- **视场角**: 90度
- **自动曝光速度**: 100
- **运动模糊**: 0
- **目标伽马值**: 1.0

### 配置详情
```json
{
  "CaptureSettings": [
    {
      "ImageType": 0,
      "Width": 1280,
      "Height": 720,
      "FOV_Degrees": 90,
      "AutoExposureSpeed": 100,
      "AutoExposureBias": 0,
      "AutoExposureMaxBrightness": 0.64,
      "AutoExposureMinBrightness": 0.03,
      "MotionBlurAmount": 0,
      "TargetGamma": 1.0
    }
  ]
}
```

## 使用方法

### 1. 启动AirSim
确保AirSim正在运行，并且settings.json文件位于正确的位置。

### 2. 测试配置
运行测试脚本来验证分辨率设置：
```bash
python test_camera_resolution.py
```

### 3. 在代码中使用
在您的Python代码中，摄像头将自动使用1280x720分辨率：

```python
import airsim

# 连接到AirSim
client = airsim.MultirotorClient()
client.confirmConnection()

# 获取1280x720分辨率的图像
responses = client.simGetImages([
    airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)
])

if responses and len(responses) > 0:
    response = responses[0]
    print(f"图像分辨率: {response.width}x{response.height}")  # 应该显示 1280x720
```

## 注意事项

1. **性能影响**: 更高的分辨率会增加计算负载，可能影响仿真性能
2. **内存使用**: 1280x720图像比256x144占用更多内存
3. **文件位置**: 确保settings.json文件位于AirSim可以找到的位置

## 故障排除

如果分辨率没有改变：
1. 确保AirSim完全重启
2. 检查settings.json文件格式是否正确
3. 确认文件位置是否正确
4. 查看AirSim日志文件中的错误信息

## 默认配置对比

| 参数 | 默认值 | 新配置 |
|------|--------|--------|
| 宽度 | 256像素 | 1280像素 |
| 高度 | 144像素 | 720像素 |
| 视场角 | 90度 | 90度 |
| 自动曝光速度 | 100 | 100 |
| 运动模糊量 | 0 | 0 |
| 目标伽马值 | 1.0 | 1.0 |
