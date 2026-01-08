"""
汤圆AI门禁系统 - 状态管理模块
包含人脸识别和对话状态的管理
"""

class FaceRecognitionState:
    """人脸识别状态枚举"""
    IDLE = "idle"                    # 空闲状态 - 欢迎界面
    DETECTING = "detecting"          # 检测中 - 实时检测人脸
    REGISTERING = "registering"      # 注册中 - 人脸注册流程
    DIALOGUE = "dialogue"            # 对话中 - AI对话模式

class DialogueState:
    """对话状态枚举"""
    INACTIVE = "inactive"     # 未激活 - 对话未开始
    LISTENING = "listening"   # 聆听中 - 正在接收语音输入
    PROCESSING = "processing" # 处理中 - 正在处理语音输入
    SPEAKING = "speaking"     # 播放中 - 正在播放AI回复
    ERROR = "error"          # 错误状态 - 出现错误

class ESP32State:
    """ESP32状态枚举"""
    IDLE = "IDLE"           # 空闲
    LISTENING = "LISTENING" # 聆听中
    PROCESSING = "PROCESSING" # 处理中
    SPEAKING = "SPEAKING"   # 播放中
    ERROR = "ERROR"         # 错误

# 状态颜色配置
STATUS_COLORS = {
    # 人脸识别状态颜色
    FaceRecognitionState.IDLE: (64, 64, 64),        # 灰色 - 待机
    FaceRecognitionState.DETECTING: (0, 255, 0),    # 绿色 - 识别中
    FaceRecognitionState.REGISTERING: (255, 165, 0), # 橙色 - 注册中
    FaceRecognitionState.DIALOGUE: (0, 255, 255),   # 青色 - 对话中

    # 对话状态颜色
    DialogueState.INACTIVE: (128, 128, 128),  # 灰色
    DialogueState.LISTENING: (255, 165, 0),   # 橙色
    DialogueState.PROCESSING: (255, 255, 0),  # 黄色
    DialogueState.SPEAKING: (0, 255, 0),      # 绿色
    DialogueState.ERROR: (255, 0, 0),         # 红色

    # ESP32状态颜色
    ESP32State.IDLE: (128, 128, 128),
    ESP32State.LISTENING: (255, 165, 0),
    ESP32State.PROCESSING: (255, 255, 0),
    ESP32State.SPEAKING: (0, 255, 0),
    ESP32State.ERROR: (255, 0, 0),
}

# 界面布局配置
UI_LAYOUT = {
    "header_height": 60,      # 状态栏高度
    "footer_height": 60,      # 底部控制栏高度
    "voice_area_height": 80,  # 语音文本区域高度
    "margin": 10,             # 边距
    "button_width": 80,       # 按钮宽度
    "button_height": 50,      # 按钮高度
}

# 配色方案
COLORS = {
    "primary": (0, 255, 255),      # 主色调 - 青色
    "success": (0, 255, 0),        # 成功色 - 绿色
    "warning": (255, 255, 0),      # 警告色 - 黄色
    "error": (255, 0, 0),          # 错误色 - 红色
    "background": (32, 32, 32),    # 背景色 - 深灰色
    "text": (255, 255, 255),       # 文本色 - 白色
    "text_secondary": (200, 200, 200),  # 次级文本色
    "border": (128, 128, 128),     # 边框色
    "button_bg": (64, 64, 64),     # 按钮背景
    "button_active": (0, 100, 100), # 激活按钮背景
}