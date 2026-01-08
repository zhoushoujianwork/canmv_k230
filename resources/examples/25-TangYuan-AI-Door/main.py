#!/usr/bin/env python3
"""
汤圆AI门禁系统 - 主程序
基于CanMV K230的智能门卫机器人
集成人脸识别、语音AI对话、射频控制功能
"""

import os
import sys
import time

# 添加libs路径
sys.path.append('/sdcard/libs')

# 导入自定义模块
from libs.FaceRecognitionApp import FaceRecognitionApp
from libs.States import FaceRecognitionState

def main():
    """主函数"""
    print("=== 汤圆AI门禁系统启动 ===")

    # 配置参数
    display_mode = "hdmi"  # 可选: "hdmi", "lcd"

    if display_mode == "hdmi":
        display_size = [1920, 1080]
        rgb888p_size = [1920, 1080]
    else:  # LCD模式
        display_size = [800, 480]
        rgb888p_size = [800, 480]

    # 模型路径配置
    face_det_kmodel_path = "/sdcard/examples/kmodel/face_detection_320.kmodel"
    face_reg_kmodel_path = "/sdcard/examples/kmodel/face_recognition.kmodel"
    anchors_path = "/sdcard/examples/utils/prior_data_320.bin"
    database_dir = "/sdcard/examples/utils/db/"

    # 检查模型文件是否存在
    if not os.path.exists(face_det_kmodel_path):
        print(f"错误: 人脸检测模型不存在: {face_det_kmodel_path}")
        return

    if not os.path.exists(face_reg_kmodel_path):
        print(f"错误: 人脸识别模型不存在: {face_reg_kmodel_path}")
        return

    if not os.path.exists(anchors_path):
        print(f"错误: anchors文件不存在: {anchors_path}")
        return

    # 加载anchors
    try:
        with open(anchors_path, 'rb') as f:
            anchors = f.read()
        print(f"成功加载anchors文件: {len(anchors)} bytes")
    except Exception as e:
        print(f"加载anchors失败: {e}")
        return

    # 创建应用实例
    try:
        app = FaceRecognitionApp(
            face_det_kmodel=face_det_kmodel_path,
            face_reg_kmodel=face_reg_kmodel_path,
            det_input_size=[320, 240],  # 人脸检测模型输入尺寸
            reg_input_size=[112, 112],  # 人脸识别模型输入尺寸
            database_dir=database_dir,
            anchors=anchors,
            confidence_threshold=0.25,
            nms_threshold=0.3,
            face_recognition_threshold=0.75,
            rgb888p_size=rgb888p_size,
            display_size=display_size,
            debug_mode=1  # 调试模式
        )

        print("=== 系统初始化完成 ===")
        print(f"显示模式: {display_mode}")
        print(f"显示分辨率: {display_size[0]}x{display_size[1]}")
        print("ESP32通信: 已初始化")
        print("AI模型: 已加载")
        print("数据库: 已初始化")
        print("")
        print("=== 开始运行 ===")
        print("按 Ctrl+C 退出程序")

        # 运行主循环
        app.run()

    except KeyboardInterrupt:
        print("\n=== 程序退出 ===")
    except Exception as e:
        print(f"\n=== 程序错误 ===")
        print(f"错误信息: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()