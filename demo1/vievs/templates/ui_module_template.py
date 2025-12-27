"""
UI模块模板 - 界面层

这个模块负责界面显示，对应 core 中的业务逻辑处理器

使用方法：
1. 在 core/ 中创建业务逻辑处理器（如 my_processor.py）
2. 复制这个文件，重命名为 my_module_ui.py
3. 修改 YourModuleUI 为你的UI类名
4. 在 init_ui() 中设计界面
5. 在 MainWindow 中组合UI和处理器

示例：
    # core/my_processor.py
    from core.base import BaseCore
    class MyProcessor(BaseCore): ...
    
    # vievs/my_module_ui.py
    from vievs.ui_module_template import YourModuleUI
    class MyModuleUI(YourModuleUI): ...
    
    # vievs/main_window.py - load_default_modules()
    from core import MyProcessor
    from .my_module_ui import MyModuleUI
    processor = MyProcessor()
    ui = MyModuleUI(self, processor)
    self.add_module('my_module', ui, '我的模块')
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                               QLabel, QTextEdit, QLineEdit, QGroupBox, QFormLayout)
from PySide6.QtCore import Signal, Qt


class YourModuleUI(QWidget):
    """
    你的UI模块
    
    这个类只负责界面显示和用户交互，业务逻辑由 processor 处理
    
    Signals:
        status_changed: 状态改变信号
        error_occurred: 错误发生信号
    """
    
    # 定义信号
    status_changed = Signal(str)
    error_occurred = Signal(str)
    
    def __init__(self, parent=None, processor=None):
        """
        初始化UI模块
        
        Args:
            parent: 父窗口（MainWindow）
            processor: 业务逻辑处理器（来自 core/）
        """
        super().__init__(parent)
        self.parent_window = parent
        self.processor = processor  # 核心处理器
        
        # 初始化处理器
        if self.processor:
            self.processor.initialize()
        
        # 初始化UI
        self.init_ui()
        
        # 连接信号槽
        self.connect_signals()
    
    def init_ui(self):
        """
        初始化界面
        
        在这里设计你的UI布局和控件
        """
        main_layout = QVBoxLayout(self)
        
        # ==================== 标题区域 ====================
        title = QLabel("📋 你的模块标题")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # ==================== 输入区域 ====================
        input_group = QGroupBox("输入参数")
        input_layout = QFormLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("输入数据...")
        input_layout.addRow("数据:", self.input_field)
        
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)
        
        # ==================== 操作按钮 ====================
        button_layout = QHBoxLayout()
        
        self.btn_process = QPushButton("开始处理")
        self.btn_clear = QPushButton("清空")
        
        button_layout.addStretch()
        button_layout.addWidget(self.btn_process)
        button_layout.addWidget(self.btn_clear)
        
        main_layout.addLayout(button_layout)
        
        # ==================== 输出区域 ====================
        output_group = QGroupBox("处理结果")
        output_layout = QVBoxLayout()
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("结果将显示在这里...")
        output_layout.addWidget(self.output_text)
        
        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group)
        
        # 初始化日志
        self.log("✅ 模块已加载", "success")
    
    def connect_signals(self):
        """连接信号槽"""
        # 按钮信号
        self.btn_process.clicked.connect(self.on_process_clicked)
        self.btn_clear.clicked.connect(self.on_clear_clicked)
        
        # 回车触发处理
        self.input_field.returnPressed.connect(self.on_process_clicked)
    
    # ==================== 事件处理 ====================
    def on_process_clicked(self):
        """
        处理按钮点击事件
        
        这里调用 core 中的 processor 进行业务逻辑处理
        """
        # 获取输入
        input_data = self.input_field.text().strip()
        
        if not input_data:
            self.log("⚠️ 请先输入数据！", "warning")
            return
        
        # 禁用按钮
        self.btn_process.setEnabled(False)
        self.log(f"📝 正在处理: {input_data}", "info")
        
        try:
            # ==================== 调用核心处理器 ====================
            if self.processor:
                # 调用处理器的 process 方法
                success = self.processor.process(
                    input_data,
                    options={'mode': 'default'}
                )
                
                if success:
                    # 获取处理结果
                    result = self.processor.get_result()
                    self.log(f"✨ 处理完成: {result}", "success")
                    self.status_changed.emit("处理成功")
                else:
                    self.log("❌ 处理失败", "error")
                    self.error_occurred.emit("处理失败")
            else:
                # 没有处理器，只做UI演示
                self.log(f"💡 演示模式: {input_data.upper()}", "info")
        
        except Exception as e:
            self.log(f"❌ 错误: {e}", "error")
            self.error_occurred.emit(str(e))
        
        finally:
            # 恢复按钮
            self.btn_process.setEnabled(True)
    
    def on_clear_clicked(self):
        """清空输出"""
        self.output_text.clear()
        self.log("🧹 输出已清空", "info")
    
    # ==================== 工具方法 ====================
    def log(self, message, level="info"):
        """
        输出日志到界面
        
        Args:
            message (str): 日志消息
            level (str): 日志级别 (info/success/warning/error)
        """
        color_map = {
            "info": "#0078d4",      # 蓝色
            "success": "#107c10",   # 绿色
            "warning": "#ff8c00",   # 橙色
            "error": "#e81123"      # 红色
        }
        color = color_map.get(level, "#000000")
        self.output_text.append(f'<span style="color:{color};">{message}</span>')
        
        # 更新父窗口状态栏
        if self.parent_window and hasattr(self.parent_window, 'statusbar'):
            self.parent_window.statusbar.showMessage(message)
    
    def get_data(self):
        """
        获取UI数据（用于保存/序列化）
        
        Returns:
            dict: UI状态数据
        """
        return {
            'input': self.input_field.text(),
            'output': self.output_text.toPlainText()
        }
    
    def set_data(self, data):
        """
        设置UI数据（用于加载/反序列化）
        
        Args:
            data (dict): UI状态数据
        """
        if 'input' in data:
            self.input_field.setText(data['input'])
        if 'output' in data:
            self.output_text.setPlainText(data['output'])
    
    def cleanup(self):
        """清理资源"""
        if self.processor:
            self.processor.cleanup()


# ==================== 完整使用流程 ====================
"""
步骤1: 在 core/ 中创建业务逻辑处理器
---------------------------------------
# core/text_processor.py
from .base import BaseCore

class TextProcessor(BaseCore):
    def __init__(self):
        super().__init__()
        self.result = None
    
    def initialize(self):
        self._initialized = True
        print("TextProcessor 已初始化")
    
    def process(self, *args, **kwargs):
        text = args[0] if args else ""
        self.result = text.upper()  # 转大写
        return True
    
    def get_result(self):
        return self.result
    
    def cleanup(self):
        self.result = None

# core/__init__.py
from .text_processor import TextProcessor
__all__ = ['BaseCore', 'DataProcessor', 'TextProcessor']


步骤2: 在 vievs/ 中创建UI模块
------------------------------
# vievs/text_module_ui.py
from .ui_module_template import YourModuleUI

class TextModuleUI(YourModuleUI):
    # 可以重写 init_ui() 来自定义界面
    # 可以添加额外的方法
    pass


步骤3: 在 MainWindow 中组合
---------------------------
# vievs/main_window.py
def load_default_modules(self):
    # 导入
    from core import TextProcessor
    from .text_module_ui import TextModuleUI
    
    # 创建处理器
    processor = TextProcessor()
    
    # 创建UI，传入处理器
    ui = TextModuleUI(self, processor)
    
    # 添加到主窗口
    self.add_module('text_module', ui, '📝 文本处理')


这样就完成了一个完整的模块！
- core/text_processor.py: 负责业务逻辑
- vievs/text_module_ui.py: 负责界面显示
- main_window.py: 组合两者
"""
