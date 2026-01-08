"""
汤圆AI门禁系统 - 人脸识别应用模块
重构后的主要应用类，集成UI、通信和AI功能
"""

import time
import gc
import ujson
import os
from libs.PipeLine import PipeLine
from libs.AIBase import AIBase
from libs.States import FaceRecognitionState, DialogueState, ESP32State
from libs.SimpleUI import SimpleUI
from libs.ESP32Communicator import ESP32Communicator

class FaceRecognitionApp:
    """人脸识别应用主类"""

    def __init__(self, face_det_kmodel, face_reg_kmodel, det_input_size, reg_input_size,
                 database_dir, anchors, confidence_threshold=0.25, nms_threshold=0.3,
                 face_recognition_threshold=0.75, rgb888p_size=[1280,720],
                 display_size=[1920,1080], debug_mode=0):

        # AI模型参数
        self.face_det_kmodel = face_det_kmodel
        self.face_reg_kmodel = face_reg_kmodel
        self.det_input_size = det_input_size
        self.reg_input_size = reg_input_size
        self.database_dir = database_dir
        self.anchors = anchors
        self.confidence_threshold = confidence_threshold
        self.nms_threshold = nms_threshold
        self.face_recognition_threshold = face_recognition_threshold

        # 显示参数
        self.rgb888p_size = [ALIGN_UP(rgb888p_size[0], 16), rgb888p_size[1]]
        self.display_size = [ALIGN_UP(display_size[0], 16), display_size[1]]
        self.debug_mode = debug_mode

        # 数据库参数
        self.max_register_face = 100
        self.feature_num = 128
        self.valid_register_face = 0
        self.db_name = []
        self.db_data = []

        # 状态管理
        self.current_state = FaceRecognitionState.IDLE
        self.last_state_change = time.time()
        self.register_step = 0
        self.register_name = ""

        # 检测结果缓存
        self.last_detections = []
        self.last_recognition_result = None

        # 初始化组件
        self._init_ai_models()
        self._init_ui()
        self._init_communication()
        self._init_pipeline()

        # 数据库初始化
        self.database_init()

    def _init_ai_models(self):
        """初始化AI模型"""
        # 人脸检测模型
        self.face_det = FaceDetApp(
            self.face_det_kmodel,
            model_input_size=self.det_input_size,
            anchors=self.anchors,
            confidence_threshold=self.confidence_threshold,
            nms_threshold=self.nms_threshold,
            rgb888p_size=self.rgb888p_size,
            display_size=self.display_size,
            debug_mode=0
        )

        # 人脸注册模型
        self.face_reg = FaceRegistrationApp(
            self.face_reg_kmodel,
            model_input_size=self.reg_input_size,
            rgb888p_size=self.rgb888p_size,
            display_size=self.display_size
        )

        # 配置预处理
        self.face_det.config_preprocess()

    def _init_ui(self):
        """初始化UI"""
        self.ui = SimpleUI(self.display_size, self.debug_mode)
        self.ui.set_button_callback(self._on_button_click)

    def _init_communication(self):
        """初始化ESP32通信"""
        self.esp32_comm = ESP32Communicator(debug_mode=self.debug_mode)

        # 设置通信回调
        self.esp32_comm.set_callbacks(
            on_voice_input=self._on_voice_input,
            on_ai_reply=self._on_ai_reply,
            on_state_change=self._on_esp32_state_change
        )

    def _init_pipeline(self):
        """初始化媒体管道"""
        self.pipeline = PipeLine(
            rgb888p_size=self.rgb888p_size,
            display_mode="hdmi",  # 可以根据需要修改
            display_size=self.display_size,
            debug_mode=self.debug_mode
        )

    def _on_button_click(self, action, state):
        """按钮点击回调"""
        if self.debug_mode > 0:
            print(f"按钮点击: {action}, 状态: {state}")

        if action == "register":
            self.start_registration()
        elif action == "dialogue":
            self.start_dialogue()
        elif action == "clear":
            self.clear_database()
        elif action == "settings":
            self.show_settings()
        elif action == "history":
            self.show_history()

    def _on_voice_input(self, text):
        """语音输入回调"""
        if self.debug_mode > 0:
            print(f"语音输入: {text}")

        self.ui.set_voice_input(text)
        self.ui.update_dialogue_state(DialogueState.PROCESSING)

    def _on_ai_reply(self, text):
        """AI回复回调"""
        if self.debug_mode > 0:
            print(f"AI回复: {text}")

        self.ui.set_ai_reply(text)
        self.ui.update_dialogue_state(DialogueState.SPEAKING)

    def _on_esp32_state_change(self, state):
        """ESP32状态变化回调"""
        if self.debug_mode > 0:
            print(f"ESP32状态变化: {state}")

        self.ui.update_esp32_state(state)

    def database_init(self):
        """数据库初始化"""
        try:
            if not os.path.exists(self.database_dir):
                os.makedirs(self.database_dir)

            # 加载已注册的人脸数据
            for i in range(self.max_register_face):
                name_file = f"{self.database_dir}/name_{i}.txt"
                data_file = f"{self.database_dir}/data_{i}.bin"

                if os.path.exists(name_file) and os.path.exists(data_file):
                    # 读取姓名
                    with open(name_file, 'r') as f:
                        name = f.read().strip()

                    # 读取特征数据
                    with open(data_file, 'rb') as f:
                        data = f.read()
                        feature = []
                        for j in range(self.feature_num):
                            val = int.from_bytes(data[j*4:j*4+4], 'little', signed=True)
                            feature.append(val / 10000.0)  # 恢复浮点数

                    self.db_name.append(name)
                    self.db_data.append(feature)
                    self.valid_register_face += 1
                else:
                    break

            if self.debug_mode > 0:
                print(f"数据库初始化完成，已注册用户: {self.valid_register_face}")

        except Exception as e:
            print(f"数据库初始化失败: {e}")

    def start_registration(self):
        """开始人脸注册"""
        if self.current_state == FaceRecognitionState.REGISTERING:
            # 取消注册
            self.current_state = FaceRecognitionState.IDLE
            self.register_step = 0
            self.register_name = ""
        else:
            # 开始注册
            self.current_state = FaceRecognitionState.REGISTERING
            self.register_step = 0
            self.register_name = ""

        self.ui.update_face_state(self.current_state)

    def start_dialogue(self):
        """开始/结束对话"""
        if self.current_state == FaceRecognitionState.DIALOGUE:
            # 结束对话
            self.esp32_comm.stop_dialogue()
            self.current_state = FaceRecognitionState.IDLE
            self.ui.update_dialogue_state(DialogueState.INACTIVE)
        else:
            # 开始对话
            self.esp32_comm.start_dialogue()
            self.current_state = FaceRecognitionState.DIALOGUE

        self.ui.update_face_state(self.current_state)

    def clear_database(self):
        """清除数据库"""
        try:
            # 删除所有数据库文件
            for i in range(self.max_register_face):
                name_file = f"{self.database_dir}/name_{i}.txt"
                data_file = f"{self.database_dir}/data_{i}.bin"

                if os.path.exists(name_file):
                    os.remove(name_file)
                if os.path.exists(data_file):
                    os.remove(data_file)

            # 清空内存数据
            self.db_name.clear()
            self.db_data.clear()
            self.valid_register_face = 0

            if self.debug_mode > 0:
                print("数据库已清除")

        except Exception as e:
            print(f"清除数据库失败: {e}")

    def show_settings(self):
        """显示设置"""
        # TODO: 实现设置界面
        pass

    def show_history(self):
        """显示历史"""
        # TODO: 实现历史界面
        pass

    def register_face(self, name):
        """注册人脸"""
        if self.valid_register_face >= self.max_register_face:
            return False, "数据库已满"

        try:
            # 查找空闲位置
            for i in range(self.max_register_face):
                name_file = f"{self.database_dir}/name_{i}.txt"
                data_file = f"{self.database_dir}/data_{i}.bin"

                if not os.path.exists(name_file):
                    # 保存姓名
                    with open(name_file, 'w') as f:
                        f.write(name)

                    # 这里应该提取人脸特征并保存
                    # TODO: 实现特征提取和保存

                    self.db_name.append(name)
                    self.valid_register_face += 1

                    # 通知ESP32
                    self.esp32_comm.send_face_register_success(name, [])

                    return True, f"用户 {name} 注册成功"
        except Exception as e:
            return False, f"注册失败: {e}"

    def recognize_face(self, detections):
        """识别人脸"""
        if not detections or self.valid_register_face == 0:
            return None, 0.0

        # TODO: 实现人脸特征提取和比对
        # 这里应该从检测结果中提取特征并与数据库比对

        # 临时返回模拟结果
        return "张三", 0.85

    def update(self):
        """主更新循环"""
        # 更新通信
        self.esp32_comm.update()

        # 根据当前状态更新UI
        if self.current_state == FaceRecognitionState.IDLE:
            self.ui.draw_idle_screen(self.pipeline, self.valid_register_face)

        elif self.current_state == FaceRecognitionState.DETECTING:
            # 执行人脸检测
            self.pipeline.update()
            detections = self.face_det.inference(self.pipeline.cur_frame)

            self.ui.draw_detecting_screen(self.pipeline, detections)
            self.last_detections = detections

            # 如果检测到人脸，尝试识别
            if detections:
                username, confidence = self.recognize_face(detections)
                if username and confidence > self.face_recognition_threshold:
                    self.last_recognition_result = (username, confidence)
                    # 通知ESP32
                    self.esp32_comm.send_face_detected(username, confidence)

        elif self.current_state == FaceRecognitionState.REGISTERING:
            self.ui.draw_registering_screen(self.pipeline, f"步骤 {self.register_step + 1}")

        elif self.current_state == FaceRecognitionState.DIALOGUE:
            self.ui.draw_dialogue_screen(self.pipeline)

    def run(self):
        """运行主循环"""
        try:
            while True:
                self.update()
                time.sleep(0.05)  # 20 FPS

        except KeyboardInterrupt:
            print("程序退出")
        except Exception as e:
            print(f"运行错误: {e}")
            self.ui.draw_error_screen(self.pipeline, str(e))