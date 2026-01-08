"""
汤圆AI门禁系统 - 简约UI模块
集成所有UI组件，提供统一的界面管理
"""

from libs.UIComponents import HeaderBar, VoiceTextArea, BottomToolbar
from libs.States import (
    FaceRecognitionState, DialogueState, ESP32State,
    UI_LAYOUT, COLORS
)

class SimpleUI:
    """简约UI管理器"""

    def __init__(self, display_size, debug_mode=0):
        self.display_size = display_size
        self.debug_mode = debug_mode

        # 初始化UI组件
        self.header_bar = HeaderBar(display_size, debug_mode)
        self.voice_text_area = VoiceTextArea(display_size, debug_mode)
        self.bottom_toolbar = BottomToolbar(display_size, debug_mode)

        # UI状态
        self.current_face_state = FaceRecognitionState.IDLE
        self.current_dialogue_state = DialogueState.INACTIVE
        self.esp32_state = ESP32State.IDLE

        # 按钮点击回调
        self.on_button_click = None

    def set_button_callback(self, callback):
        """设置按钮点击回调"""
        self.on_button_click = callback
        self.bottom_toolbar.set_button_callback(callback)

    def update_face_state(self, state):
        """更新人脸识别状态"""
        self.current_face_state = state
        self.header_bar.set_current_mode(state)
        self.bottom_toolbar.set_current_state(state)

    def update_dialogue_state(self, state):
        """更新对话状态"""
        self.current_dialogue_state = state
        self.voice_text_area.set_dialogue_state(state)

    def update_esp32_state(self, state):
        """更新ESP32状态"""
        self.esp32_state = state
        self.header_bar.set_esp32_state(state)

    def set_voice_input(self, text):
        """设置语音输入文本"""
        self.voice_text_area.set_voice_input(text)

    def set_ai_reply(self, text):
        """设置AI回复文本"""
        self.voice_text_area.set_ai_reply(text)

    def check_touch(self, touch_x, touch_y):
        """检查触摸事件"""
        return self.bottom_toolbar.check_touch(touch_x, touch_y)

    def draw_idle_screen(self, pl, user_count=0):
        """绘制空闲界面"""
        pl.osd_img.clear()

        # 绘制组件
        self.header_bar.draw(pl)

        # 主内容区
        center_x = self.display_size[0] // 2
        center_y = self.display_size[1] // 2

        # 欢迎信息
        welcome_text = "欢迎使用"
        pl.osd_img.draw_string_advanced(center_x - 60, center_y - 60, 24,
                                       welcome_text, color=COLORS["text"])

        system_text = "汤圆AI门禁系统"
        pl.osd_img.draw_string_advanced(center_x - 90, center_y - 30, 28,
                                       system_text, color=COLORS["primary"])

        # 状态信息
        status_y = center_y + 20
        status_texts = [
            f"状态: {self.current_face_state}",
            f"用户数: {user_count}",
            f"ESP32: {self.esp32_state}"
        ]

        for i, text in enumerate(status_texts):
            color = COLORS["text_secondary"]
            if "状态:" in text:
                color = COLORS.get(self.current_face_state, COLORS["text"])
            elif "ESP32:" in text:
                color = COLORS.get(self.esp32_state, COLORS["text_secondary"])

            pl.osd_img.draw_string_advanced(center_x - 60, status_y + i * 25, 18,
                                           text, color=color)

        # 绘制语音文本区和底部工具栏
        self.voice_text_area.draw(pl)
        self.bottom_toolbar.draw(pl)

    def draw_detecting_screen(self, pl, detections):
        """绘制人脸检测界面"""
        pl.osd_img.clear()

        # 绘制组件
        self.header_bar.draw(pl)

        center_x = self.display_size[0] // 2
        content_y = UI_LAYOUT["header_height"] + 50

        if detections:
            # 显示检测结果
            det = detections[0]  # 取第一个检测结果
            det_text = f"检测到人脸 ({len(detections)}人)"
            pl.osd_img.draw_string_advanced(center_x - 80, content_y, 22,
                                           det_text, color=COLORS["success"])

            # 人脸框信息
            box_y = content_y + 40
            pl.osd_img.draw_rectangle(center_x - 100, box_y, 200, 120,
                                     color=COLORS["primary"], thickness=2)

            info_texts = [
                f"位置: ({det[0]:.0f}, {det[1]:.0f})",
                f"大小: {det[2]:.0f} x {det[3]:.0f}",
                "状态: 正在识别..."
            ]

            for i, text in enumerate(info_texts):
                pl.osd_img.draw_string_advanced(center_x - 80, box_y + 130 + i * 20, 16,
                                               text, color=COLORS["text"])
        else:
            # 无检测结果
            no_det_text = "未检测到人脸"
            pl.osd_img.draw_string_advanced(center_x - 70, content_y, 22,
                                           no_det_text, color=COLORS["warning"])

            hint_text = "请正对摄像头"
            pl.osd_img.draw_string_advanced(center_x - 60, content_y + 40, 18,
                                           hint_text, color=COLORS["text_secondary"])

        # 绘制语音文本区和底部工具栏
        self.voice_text_area.draw(pl)
        self.bottom_toolbar.draw(pl)

    def draw_recognizing_screen(self, pl, username, confidence, feature=None):
        """绘制人脸识别结果界面"""
        pl.osd_img.clear()

        # 绘制组件
        self.header_bar.draw(pl)

        center_x = self.display_size[0] // 2
        content_y = UI_LAYOUT["header_height"] + 50

        # 识别结果
        if confidence > 0.5:  # 置信度阈值
            result_text = "识别成功"
            result_color = COLORS["success"]
        else:
            result_text = "识别失败"
            result_color = COLORS["error"]

        pl.osd_img.draw_string_advanced(center_x - 60, content_y, 24,
                                       result_text, color=result_color)

        # 用户信息
        user_y = content_y + 40
        user_info = f"用户名: {username}"
        pl.osd_img.draw_string_advanced(center_x - 80, user_y, 20,
                                       user_info, color=COLORS["text"])

        confidence_info = f"相似度: {confidence:.3f}"
        confidence_color = COLORS["success"] if confidence > 0.5 else COLORS["error"]
        pl.osd_img.draw_string_advanced(center_x - 80, user_y + 30, 18,
                                       confidence_info, color=confidence_color)

        # 绘制语音文本区和底部工具栏
        self.voice_text_area.draw(pl)
        self.bottom_toolbar.draw(pl)

    def draw_registering_screen(self, pl, step="准备注册"):
        """绘制注册界面"""
        pl.osd_img.clear()

        # 绘制组件
        self.header_bar.draw(pl)

        center_x = self.display_size[0] // 2
        center_y = self.display_size[1] // 2

        # 注册提示
        register_text = "人脸注册模式"
        pl.osd_img.draw_string_advanced(center_x - 70, center_y - 60, 24,
                                       register_text, color=COLORS["warning"])

        # 当前步骤
        step_text = f"步骤: {step}"
        pl.osd_img.draw_string_advanced(center_x - 50, center_y - 20, 18,
                                       step_text, color=COLORS["text"])

        # 提示信息
        hints = [
            "1. 正对摄像头",
            "2. 保持表情自然",
            "3. 等待注册完成"
        ]

        for i, hint in enumerate(hints):
            hint_color = COLORS["text_secondary"]
            if "1." in hint:
                hint_color = COLORS["primary"]
            pl.osd_img.draw_string_advanced(center_x - 60, center_y + 20 + i * 25, 16,
                                           hint, color=hint_color)

        # 绘制语音文本区和底部工具栏
        self.voice_text_area.draw(pl)
        self.bottom_toolbar.draw(pl)

    def draw_dialogue_screen(self, pl):
        """绘制对话界面"""
        pl.osd_img.clear()

        # 设置标题
        self.header_bar.set_title("AI对话模式")
        self.header_bar.draw(pl)

        center_x = self.display_size[0] // 2
        center_y = self.display_size[1] // 2 - 40

        # AI头像区域
        avatar_radius = 60
        pl.osd_img.draw_circle(center_x, center_y, avatar_radius,
                              color=COLORS["primary"], thickness=3)

        # AI头像表情符号
        pl.osd_img.draw_string_advanced(center_x - 20, center_y - 15, 32, "🤖",
                                       color=COLORS["primary"])

        # 欢迎文本
        welcome_texts = [
            "您好！我是汤圆AI助手",
            "请说'你好'开始对话"
        ]

        for i, text in enumerate(welcome_texts):
            pl.osd_img.draw_string_advanced(center_x - 100, center_y + 120 + i * 25, 20,
                                           text, color=COLORS["text"])

        # 绘制语音文本区和底部工具栏
        self.voice_text_area.draw(pl)
        self.bottom_toolbar.draw(pl)

    def draw_error_screen(self, pl, error_message):
        """绘制错误界面"""
        pl.osd_img.clear()

        # 绘制组件
        self.header_bar.draw(pl)

        center_x = self.display_size[0] // 2
        center_y = self.display_size[1] // 2

        # 错误提示
        error_text = "系统错误"
        pl.osd_img.draw_string_advanced(center_x - 50, center_y - 40, 24,
                                       error_text, color=COLORS["error"])

        # 错误信息
        pl.osd_img.draw_string_advanced(center_x - 100, center_y, 18,
                                       error_message, color=COLORS["text"])

        # 恢复提示
        recover_text = "请重启系统或联系管理员"
        pl.osd_img.draw_string_advanced(center_x - 120, center_y + 40, 16,
                                       recover_text, color=COLORS["text_secondary"])

        # 绘制语音文本区和底部工具栏
        self.voice_text_area.draw(pl)
        self.bottom_toolbar.draw(pl)