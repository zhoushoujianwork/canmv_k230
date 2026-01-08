"""
汤圆AI门禁系统 - ESP32通信模块
负责与ESP32进行UART通信，处理对话状态同步
"""

import time
from machine import UART, FPIOA
from libs.States import DialogueState, ESP32State

class ESP32Communicator:
    """ESP32通信管理器"""

    def __init__(self, uart_id=1, tx_pin=11, rx_pin=12, baudrate=115200, debug_mode=0):
        self.uart_id = uart_id
        self.tx_pin = tx_pin
        self.rx_pin = rx_pin
        self.baudrate = baudrate
        self.debug_mode = debug_mode

        self.uart = None
        self.esp32_state = ESP32State.IDLE
        self.last_command_time = 0
        self.command_timeout = 5.0  # 5秒超时

        # 通信缓冲区
        self.receive_buffer = ""
        self.command_queue = []

        # 回调函数
        self.on_voice_input = None
        self.on_ai_reply = None
        self.on_state_change = None

        self._init_uart()

    def _init_uart(self):
        """初始化UART通信"""
        try:
            # 配置FPIOA引脚
            fpioa = FPIOA()
            fpioa.set_function(self.tx_pin, FPIOA.UART1_TX)
            fpioa.set_function(self.rx_pin, FPIOA.UART1_RX)

            # 初始化UART
            self.uart = UART(self.uart_id, self.baudrate, 8, 1, 0, timeout=1000, read_buf_len=4096)

            if self.debug_mode > 0:
                print(f"ESP32 UART通信初始化成功: UART{self.uart_id}, 波特率{self.baudrate}")

        except Exception as e:
            print(f"ESP32 UART初始化失败: {e}")
            self.uart = None

    def send_command(self, command, data=""):
        """发送命令到ESP32"""
        if not self.uart:
            return False

        try:
            message = f"{command}|{data}\n"
            self.uart.write(message.encode('utf-8'))
            self.last_command_time = time.time()

            if self.debug_mode > 0:
                print(f"发送到ESP32: {message.strip()}")

            return True
        except Exception as e:
            print(f"发送命令失败: {e}")
            return False

    def receive_data(self):
        """接收ESP32数据"""
        if not self.uart:
            return None

        try:
            # 读取可用数据
            data = self.uart.read()
            if data:
                data_str = data.decode('utf-8', errors='ignore')
                self.receive_buffer += data_str

                # 处理完整的命令行
                lines = self.receive_buffer.split('\n')
                self.receive_buffer = lines[-1]  # 保留不完整的行

                # 处理每个完整行
                for line in lines[:-1]:
                    line = line.strip()
                    if line:
                        self._process_command(line)

        except Exception as e:
            if self.debug_mode > 0:
                print(f"接收数据错误: {e}")

    def _process_command(self, line):
        """处理ESP32发送的命令"""
        try:
            if self.debug_mode > 0:
                print(f"收到ESP32命令: {line}")

            parts = line.split("|")
            if len(parts) >= 1:
                command = parts[0]
                data = parts[1] if len(parts) > 1 else ""

                # 更新ESP32状态
                if command == "VOICE_STATUS":
                    self.esp32_state = data
                    if self.on_state_change:
                        self.on_state_change(data)
                elif command == "VOICE_INPUT":
                    if self.on_voice_input:
                        self.on_voice_input(data)
                elif command == "AI_REPLY":
                    if self.on_ai_reply:
                        self.on_ai_reply(data)
                elif command == "DIALOGUE_START":
                    self.esp32_state = ESP32State.LISTENING
                    if self.on_state_change:
                        self.on_state_change(ESP32State.LISTENING)
                elif command == "DIALOGUE_END":
                    self.esp32_state = ESP32State.IDLE
                    if self.on_state_change:
                        self.on_state_change(ESP32State.IDLE)

        except Exception as e:
            print(f"处理ESP32命令失败: {e}")

    def start_dialogue(self):
        """开始对话"""
        return self.send_command("DIALOGUE_START")

    def stop_dialogue(self):
        """停止对话"""
        return self.send_command("DIALOGUE_END")

    def send_face_register_success(self, username, features):
        """发送人脸注册成功信息"""
        data = f"{username}|{features}"
        return self.send_command("REGISTER", data)

    def send_face_detected(self, username, confidence):
        """发送人脸识别结果"""
        data = f"{username}|{confidence:.3f}"
        return self.send_command("DETECT", data)

    def send_system_status(self, status):
        """发送系统状态"""
        return self.send_command("STATUS", status)

    def get_esp32_state(self):
        """获取ESP32当前状态"""
        return self.esp32_state

    def is_connected(self):
        """检查ESP32连接状态"""
        if not self.uart:
            return False

        # 检查是否在超时时间内收到过响应
        current_time = time.time()
        return (current_time - self.last_command_time) < self.command_timeout

    def update(self):
        """更新通信状态，定期调用"""
        self.receive_data()

        # 检查连接状态
        if not self.is_connected():
            self.esp32_state = ESP32State.ERROR

    def set_callbacks(self, on_voice_input=None, on_ai_reply=None, on_state_change=None):
        """设置回调函数"""
        self.on_voice_input = on_voice_input
        self.on_ai_reply = on_ai_reply
        self.on_state_change = on_state_change