"""
汤圆AI门禁系统 - UI组件模块
包含状态栏、语音文本区、底部控制栏等UI组件
"""

import time
import math
from libs.States import (
    FaceRecognitionState, DialogueState, ESP32State,
    STATUS_COLORS, UI_LAYOUT, COLORS
)

class HeaderBar:
    """状态栏组件"""

    def __init__(self, display_size, debug_mode=0):
        self.display_size = display_size
        self.debug_mode = debug_mode
        self.title = "汤圆AI门禁系统"
        self.esp32_state = ESP32State.IDLE
        self.current_mode = FaceRecognitionState.IDLE
        self.system_time = time.localtime()

    def set_title(self, title):
        """设置标题"""
        self.title = title

    def set_esp32_state(self, state):
        """设置ESP32状态"""
        self.esp32_state = state

    def set_current_mode(self, mode):
        """设置当前模式"""
        self.current_mode = mode

    def get_esp32_status_color(self):
        """获取ESP32状态颜色"""
        return STATUS_COLORS.get(self.esp32_state, COLORS["text_secondary"])

    def get_mode_status_text(self):
        """获取模式状态文本"""
        mode_texts = {
            FaceRecognitionState.IDLE: "待机",
            FaceRecognitionState.DETECTING: "识别中",
            FaceRecognitionState.REGISTERING: "注册中",
            FaceRecognitionState.DIALOGUE: "对话中",
        }
        return mode_texts.get(self.current_mode, "未知")

    def draw(self, pl):
        """绘制状态栏"""
        # 背景
        pl.osd_img.draw_rectangle(0, 0, self.display_size[0], UI_LAYOUT["header_height"],
                                 color=COLORS["background"], thickness=-1)
        pl.osd_img.draw_rectangle(0, 0, self.display_size[0], UI_LAYOUT["header_height"],
                                 color=COLORS["primary"], thickness=2)

        # 标题
        pl.osd_img.draw_string_advanced(20, 20, 24, self.title,
                                       color=COLORS["text"], scale=1)

        # 模式状态 (中间)
        mode_text = self.get_mode_status_text()
        mode_color = STATUS_COLORS.get(self.current_mode, COLORS["text"])
        mode_x = self.display_size[0] // 2 - len(mode_text) * 6
        pl.osd_img.draw_string_advanced(mode_x, 20, 18, mode_text, color=mode_color)

        # ESP32状态 (右侧)
        esp32_text = f"ESP32: {self.esp32_state}"
        esp32_color = self.get_esp32_status_color()
        esp32_x = self.display_size[0] - 200
        pl.osd_img.draw_string_advanced(esp32_x, 20, 18, esp32_text, color=esp32_color)

        # 系统时间
        self.system_time = time.localtime()
        time_text = f"{self.system_time[3]:02d}:{self.system_time[4]:02d}:{self.system_time[5]:02d}"
        pl.osd_img.draw_string_advanced(esp32_x, 40, 16, time_text, color=COLORS["text_secondary"])


class VoiceTextArea:
    """语音文本展示区组件"""

    def __init__(self, display_size, debug_mode=0):
        self.display_size = display_size
        self.debug_mode = debug_mode

        # 文本内容
        self.current_voice_input = ""
        self.current_ai_reply = ""
        self.dialogue_state = DialogueState.INACTIVE

        # 动画相关
        self.reply_animation_start = 0
        self.reply_display_chars = 0

    def set_voice_input(self, text):
        """设置语音输入文本"""
        self.current_voice_input = text

    def set_ai_reply(self, text):
        """设置AI回复文本"""
        self.current_ai_reply = text
        self.reply_animation_start = time.time()
        self.reply_display_chars = 0

    def set_dialogue_state(self, state):
        """设置对话状态"""
        self.dialogue_state = state

    def get_voice_status_text(self):
        """获取语音状态文本"""
        status_texts = {
            DialogueState.LISTENING: "正在聆听...",
            DialogueState.PROCESSING: "正在处理...",
            DialogueState.SPEAKING: "正在播放...",
            DialogueState.ERROR: "语音处理错误",
            DialogueState.INACTIVE: "就绪",
        }
        return status_texts.get(self.dialogue_state, "未知状态")

    def get_voice_status_color(self):
        """获取语音状态颜色"""
        return STATUS_COLORS.get(self.dialogue_state, COLORS["text_secondary"])

    def _truncate_text(self, text, max_chars):
        """截断文本"""
        if len(text) <= max_chars:
            return text
        return text[:max_chars-3] + "..."

    def draw_voice_input_animation(self, pl, x, y):
        """绘制语音输入时的动画效果"""
        if self.dialogue_state == DialogueState.LISTENING:
            # 波形动画
            wave_height = 20
            wave_count = 5
            base_y = y

            for i in range(wave_count):
                # 计算每个波的相位
                phase = (time.time() * 3 + i * 0.5) % (2 * math.pi)
                height = wave_height * (0.5 + 0.5 * math.sin(phase))

                wave_x = x + i * 15
                pl.osd_img.draw_line(wave_x, base_y - height, wave_x, base_y + height,
                                   color=COLORS["primary"], thickness=3)

    def draw_reply_animation(self, pl, x, y):
        """绘制AI回复打字动画"""
        if self.dialogue_state == DialogueState.SPEAKING and self.current_ai_reply:
            elapsed = time.time() - self.reply_animation_start
            chars_per_second = 15  # 每秒15个字符
            target_chars = int(elapsed * chars_per_second)

            if target_chars > len(self.current_ai_reply):
                target_chars = len(self.current_ai_reply)

            if target_chars > self.reply_display_chars:
                self.reply_display_chars = target_chars

            display_text = self.current_ai_reply[:self.reply_display_chars]

            # 添加光标效果
            if self.reply_display_chars < len(self.current_ai_reply):
                display_text += "█"

            pl.osd_img.draw_string_advanced(x, y, 16, display_text, color=COLORS["primary"])
        else:
            # 正常显示
            pl.osd_img.draw_string_advanced(x, y, 16, f"🤖 {self.current_ai_reply}",
                                           color=COLORS["primary"])

    def draw(self, pl):
        """绘制语音文本展示区"""
        area_y = self.display_size[1] - UI_LAYOUT["voice_area_height"] - UI_LAYOUT["footer_height"]
        area_height = UI_LAYOUT["voice_area_height"]

        # 背景框
        pl.osd_img.draw_rectangle(UI_LAYOUT["margin"], area_y,
                                 self.display_size[0] - 2*UI_LAYOUT["margin"], area_height,
                                 color=COLORS["background"], thickness=-1)
        pl.osd_img.draw_rectangle(UI_LAYOUT["margin"], area_y,
                                 self.display_size[0] - 2*UI_LAYOUT["margin"], area_height,
                                 color=COLORS["primary"], thickness=1)

        # 语音输入行
        input_y = area_y + 10
        input_text = self._truncate_text(self.current_voice_input, 40) or "等待语音输入..."
        pl.osd_img.draw_string_advanced(20, input_y, 16, f"🎤 {input_text}",
                                       color=COLORS["text"])

        # AI回复行
        reply_y = area_y + 35
        if self.dialogue_state == DialogueState.SPEAKING:
            self.draw_reply_animation(pl, 20, reply_y)
        else:
            reply_text = self._truncate_text(self.current_ai_reply, 40) or "等待AI回复..."
            pl.osd_img.draw_string_advanced(20, reply_y, 16, f"🤖 {reply_text}",
                                           color=COLORS["primary"])

        # 状态提示行
        status_y = area_y + 55
        status_text = self.get_voice_status_text()
        status_color = self.get_voice_status_color()
        pl.osd_img.draw_string_advanced(20, status_y, 14, f"💬 {status_text}",
                                       color=status_color)

        # 语音输入动画
        if self.dialogue_state == DialogueState.LISTENING:
            self.draw_voice_input_animation(pl, self.display_size[0] - 100, input_y + 10)


class BottomToolbar:
    """底部控制栏组件"""

    def __init__(self, display_size, debug_mode=0):
        self.display_size = display_size
        self.debug_mode = debug_mode

        self.current_state = FaceRecognitionState.IDLE
        self.buttons = [
            ("注册", "register", FaceRecognitionState.REGISTERING),
            ("对话", "dialogue", FaceRecognitionState.DIALOGUE),
            ("设置", "settings", None),
            ("历史", "history", None),
            ("清除", "clear", None),
        ]

        # 按钮回调
        self.on_button_click = None

    def set_current_state(self, state):
        """设置当前状态"""
        self.current_state = state

    def set_button_callback(self, callback):
        """设置按钮点击回调"""
        self.on_button_click = callback

    def check_touch(self, touch_x, touch_y):
        """检查触摸事件"""
        if not self.on_button_click:
            return False

        toolbar_y = self.display_size[1] - UI_LAYOUT["footer_height"]
        button_height = UI_LAYOUT["button_height"]
        button_width = UI_LAYOUT["button_width"]
        margin = UI_LAYOUT["margin"]

        if touch_y < toolbar_y or touch_y > toolbar_y + button_height:
            return False

        # 检查每个按钮
        for i, (text, action, state) in enumerate(self.buttons):
            x = margin + i * (button_width + margin)
            if touch_x >= x and touch_x <= x + button_width:
                self.on_button_click(action, state)
                return True

        return False

    def draw(self, pl):
        """绘制底部控制栏"""
        toolbar_y = self.display_size[1] - UI_LAYOUT["footer_height"]
        button_width = UI_LAYOUT["button_width"]
        button_height = UI_LAYOUT["button_height"]
        margin = UI_LAYOUT["margin"]

        for i, (text, action, state) in enumerate(self.buttons):
            x = margin + i * (button_width + margin)

            # 按钮背景
            is_active = (state == self.current_state)
            bg_color = COLORS["button_active"] if is_active else COLORS["button_bg"]
            border_color = COLORS["primary"] if is_active else COLORS["border"]

            pl.osd_img.draw_rectangle(x, toolbar_y, button_width, button_height,
                                     color=bg_color, thickness=-1)
            pl.osd_img.draw_rectangle(x, toolbar_y, button_width, button_height,
                                     color=border_color, thickness=2)

            # 按钮文字
            text_color = COLORS["text"] if is_active else COLORS["text_secondary"]
            text_x = x + (button_width - len(text) * 12) // 2
            text_y = toolbar_y + 15
            pl.osd_img.draw_string_advanced(text_x, text_y, 18, text, color=text_color)