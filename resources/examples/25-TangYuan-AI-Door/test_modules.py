#!/usr/bin/env python3
"""
汤圆AI门禁系统 - 模块测试脚本
测试所有模块的导入和基本功能
"""

import sys
import os

# 添加libs路径
sys.path.append('/sdcard/libs')

def test_imports():
    """测试模块导入"""
    print("=== 测试模块导入 ===")

    modules_to_test = [
        ('libs.States', '状态管理模块'),
        ('libs.ESP32Communicator', 'ESP32通信模块'),
        ('libs.UIComponents', 'UI组件模块'),
        ('libs.SimpleUI', 'UI管理器模块'),
        ('libs.FaceRecognitionApp', '人脸识别应用模块'),
        ('libs.Utils', '工具函数模块'),
        ('libs.PipeLine', '媒体管道模块'),
        ('libs.AIBase', 'AI基础模块'),
        ('libs.AI2D', 'AI2D处理模块'),
    ]

    success_count = 0

    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {description}: 导入成功")
            success_count += 1
        except ImportError as e:
            print(f"❌ {description}: 导入失败 - {e}")
        except Exception as e:
            print(f"⚠️  {description}: 导入异常 - {e}")

    print(f"\n导入测试完成: {success_count}/{len(modules_to_test)} 个模块成功")
    return success_count == len(modules_to_test)

def test_states():
    """测试状态管理模块"""
    print("\n=== 测试状态管理模块 ===")

    try:
        from libs.States import (
            FaceRecognitionState, DialogueState, ESP32State,
            STATUS_COLORS, UI_LAYOUT, COLORS
        )

        # 测试枚举值
        print(f"人脸识别状态: {FaceRecognitionState.IDLE}, {FaceRecognitionState.DETECTING}")
        print(f"对话状态: {DialogueState.LISTENING}, {DialogueState.SPEAKING}")
        print(f"ESP32状态: {ESP32State.IDLE}, {ESP32State.LISTENING}")

        # 测试颜色配置
        print(f"IDLE状态颜色: {STATUS_COLORS[FaceRecognitionState.IDLE]}")
        print(f"主色调: {COLORS['primary']}")

        # 测试UI布局
        print(f"状态栏高度: {UI_LAYOUT['header_height']}px")
        print(f"按钮宽度: {UI_LAYOUT['button_width']}px")

        print("✅ 状态管理模块测试通过")
        return True

    except Exception as e:
        print(f"❌ 状态管理模块测试失败: {e}")
        return False

def test_esp32_communicator():
    """测试ESP32通信模块"""
    print("\n=== 测试ESP32通信模块 ===")

    try:
        from libs.ESP32Communicator import ESP32Communicator

        # 创建通信器实例 (不实际连接)
        comm = ESP32Communicator(debug_mode=0)

        # 测试属性
        print(f"UART ID: {comm.uart_id}")
        print(f"波特率: {comm.baudrate}")
        print(f"ESP32状态: {comm.esp32_state}")

        print("✅ ESP32通信模块测试通过")
        return True

    except Exception as e:
        print(f"❌ ESP32通信模块测试失败: {e}")
        return False

def test_ui_components():
    """测试UI组件模块"""
    print("\n=== 测试UI组件模块 ===")

    try:
        from libs.UIComponents import HeaderBar, VoiceTextArea, BottomToolbar

        # 测试组件创建
        display_size = [800, 480]

        header = HeaderBar(display_size)
        voice_area = VoiceTextArea(display_size)
        toolbar = BottomToolbar(display_size)

        # 测试属性设置
        header.set_title("测试标题")
        voice_area.set_voice_input("测试输入")
        voice_area.set_ai_reply("测试回复")

        print(f"标题: {header.title}")
        print(f"语音输入: {voice_area.current_voice_input}")
        print(f"AI回复: {voice_area.current_ai_reply}")

        print("✅ UI组件模块测试通过")
        return True

    except Exception as e:
        print(f"❌ UI组件模块测试失败: {e}")
        return False

def test_simple_ui():
    """测试UI管理器模块"""
    print("\n=== 测试UI管理器模块 ===")

    try:
        from libs.SimpleUI import SimpleUI

        # 创建UI管理器
        display_size = [800, 480]
        ui = SimpleUI(display_size)

        # 测试状态更新
        from libs.States import FaceRecognitionState, DialogueState, ESP32State

        ui.update_face_state(FaceRecognitionState.DETECTING)
        ui.update_dialogue_state(DialogueState.LISTENING)
        ui.update_esp32_state(ESP32State.SPEAKING)

        print(f"人脸状态: {ui.current_face_state}")
        print(f"对话状态: {ui.current_dialogue_state}")
        print(f"ESP32状态: {ui.esp32_state}")

        print("✅ UI管理器模块测试通过")
        return True

    except Exception as e:
        print(f"❌ UI管理器模块测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("汤圆AI门禁系统 - 模块测试")
    print("=" * 40)

    # 测试导入
    import_success = test_imports()

    if not import_success:
        print("\n❌ 模块导入测试失败，退出测试")
        return False

    # 测试各个模块
    tests = [
        test_states,
        test_esp32_communicator,
        test_ui_components,
        test_simple_ui,
    ]

    success_count = 0
    for test_func in tests:
        if test_func():
            success_count += 1

    print("\n" + "=" * 40)
    print(f"测试完成: {success_count}/{len(tests)} 个测试通过")

    if success_count == len(tests):
        print("🎉 所有测试通过！模块化版本准备就绪。")
        return True
    else:
        print("⚠️  部分测试失败，请检查相关模块。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)