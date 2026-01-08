# 汤圆AI门禁系统 - 模块化版本

## 概述

这是基于CanMV K230官方SDK移植的汤圆AI门禁系统模块化版本，集成了人脸识别、语音AI对话、射频控制等功能。采用简约UI设计，支持AI对话状态显示和语音文本展示。

本次更新将原来单一的大文件拆分为多个模块，提高代码可维护性和可扩展性。

## 功能特性

### ✅ 核心功能
- **人脸识别**: 实时检测和识别已注册用户
- **人脸注册**: 支持用户注册和管理
- **AI对话**: 支持语音交互和状态显示
- **语音文本展示**: 实时显示语音输入和AI回复
- **ESP32通信**: 通过UART与ESP32进行状态同步

### ✅ 界面设计
- **简约风格**: 纯文本+简单图形，性能优异
- **四区域布局**:
  - 顶部状态栏: 系统状态和时间
  - 主内容区: 人脸识别/注册/对话界面
  - 语音文本区: 语音输入和AI回复显示
  - 底部控制栏: 注册/对话/清除按钮

### ✅ AI对话功能
- **状态显示**: 聆听中/处理中/播放中/错误
- **表情符号**: 🤖🎤🤔🗣️❌ 状态指示
- **实时文本**: 语音输入和AI回复的实时显示

## 新增功能

### 🆕 模块化架构
- **States.py**: 状态管理模块
- **ESP32Communicator.py**: ESP32通信模块
- **UIComponents.py**: UI组件模块
- **SimpleUI.py**: UI管理器模块
- **FaceRecognitionApp.py**: 人脸识别应用模块

### 🆕 面向对象设计
- 清晰的类层次结构
- 模块间的低耦合高内聚
- 易于扩展和维护

## 文件结构

```
25-TangYuan-AI-Door/
├── main.py               # 主程序入口 (模块化版本)
├── lckfb_lsp.py          # 原版主程序 (保留)
├── run.sh                # 运行脚本
├── test_import.py        # 导入测试
├── README.md             # 原版说明文档
└── README_v2.md          # 新版说明文档 (本文件)

libs/                     # 模块化库文件
├── States.py             # 状态管理模块 (新)
├── ESP32Communicator.py  # ESP32通信模块 (新)
├── UIComponents.py       # UI组件模块 (新)
├── SimpleUI.py           # UI管理器模块 (新)
├── FaceRecognitionApp.py # 人脸识别应用模块 (新)
├── Utils.py              # 工具函数
├── PipeLine.py            # 媒体管道
├── AIBase.py             # AI基础类
├── AI2D.py               # AI2D处理
└── PlatTasks.py          # 平台任务
```

## 运行方法

### 方法1: 运行模块化版本 (推荐)

```bash
# 在K230开发板上运行
cd /sdcard/examples/25-TangYuan-AI-Door
python main.py
```

### 方法2: 运行原版

```bash
# 在K230开发板上运行
python /sdcard/examples/25-TangYuan-AI-Door/lckfb_lsp.py
```

### 方法3: 通过CanMV IDE运行

1. 打开CanMV IDE
2. 连接到K230开发板
3. 打开文件 `/sdcard/examples/25-TangYuan-AI-Door/main.py`
4. 点击运行按钮

## 模块说明

### States.py - 状态管理模块
- 定义了人脸识别和对话的状态枚举
- 包含UI布局配置和配色方案
- 提供状态颜色映射

### ESP32Communicator.py - ESP32通信模块
- 负责与ESP32的UART通信
- 处理对话状态同步
- 支持命令收发和状态回调

### UIComponents.py - UI组件模块
- **HeaderBar**: 状态栏组件
- **VoiceTextArea**: 语音文本展示区
- **BottomToolbar**: 底部控制栏

### SimpleUI.py - UI管理器模块
- 集成所有UI组件
- 提供统一的界面绘制接口
- 支持多场景界面切换

### FaceRecognitionApp.py - 人脸识别应用模块
- 主要应用逻辑
- 集成AI模型、UI、通信功能
- 管理应用状态和用户交互

## 技术规格

- **框架**: CanMV K230官方SDK (模块化)
- **AI推理**: KPU硬件加速
- **显示**: OpenMV图形库
- **通信**: UART串口
- **存储**: MicroPython文件系统
- **架构**: 面向对象设计

## 配置说明

### 显示模式配置
```python
# 在main.py中修改
display_mode = "hdmi"  # 可选: "hdmi", "lcd"
```

### 调试模式配置
```python
# 设置调试等级 (0-2)
debug_mode = 1  # 0:无调试, 1:基本调试, 2:详细调试
```

## UART通信协议

### ESP32 → K230:
```
VOICE_INPUT|用户说话内容    # 语音输入
AI_REPLY|AI回复内容        # AI回复
DIALOGUE_START            # 开始对话
DIALOGUE_END              # 结束对话
VOICE_STATUS|状态          # 语音状态
```

### K230 → ESP32:
```
REGISTER|用户名|特征数据    # 注册成功
DETECT|用户名|置信度      # 识别结果
STATUS|状态信息           # 系统状态
DIALOGUE_REQUEST          # 请求对话
DIALOGUE_CANCEL           # 取消对话
```

## 界面预览

### 模块化版本界面
- 保持与原版相同的视觉效果
- 更流畅的状态切换
- 更好的错误处理

## 优势对比

| 特性 | 原版 | 模块化版本 |
|------|------|-----------|
| 代码组织 | 单文件 | 多模块 |
| 可维护性 | 一般 | 优秀 |
| 可扩展性 | 一般 | 优秀 |
| 错误处理 | 基础 | 完善 |
| 性能 | 相同 | 相同 |

## 开发指南

### 添加新功能
1. 在相应模块中添加新类/方法
2. 更新状态枚举 (如需要)
3. 在FaceRecognitionApp中集成
4. 测试功能完整性

### 自定义UI
1. 修改UIComponents.py中的组件
2. 更新SimpleUI.py的绘制逻辑
3. 调整States.py中的配色和布局

### 扩展通信
1. 修改ESP32Communicator.py
2. 添加新的命令处理
3. 更新回调机制

## 注意事项

1. **兼容性**: 模块化版本保持与原版的接口兼容
2. **性能**: 模块化设计不影响运行性能
3. **内存**: 注意MicroPython的内存限制
4. **调试**: 建议在调试模式下运行以查看详细日志

## 更新日志

- **v2.0** (2024-12-XX)
  - 模块化重构，拆分为多个独立模块
  - 引入面向对象设计
  - 完善错误处理机制
  - 优化代码结构和可维护性
  - 保持与原版功能完全兼容

- **v1.0** (2024-12-XX)
  - 初始移植版本
  - 集成简约UI设计
  - 支持AI对话状态显示
  - 支持语音文本展示
  - 支持ESP32通信同步

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 许可证

与CanMV K230官方SDK保持一致。