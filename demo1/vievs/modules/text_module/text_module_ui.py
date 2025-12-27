"""
文本处理模块UI - 对应 core.TextProcessor

这个UI模块展示如何创建界面并调用 core 中的业务逻辑
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QTextEdit, QGroupBox, QComboBox)
from PySide6.QtCore import Qt


class TextModuleUI(QWidget):
    """文本处理模块UI"""
    
    def __init__(self, parent=None, processor=None):
        super().__init__(parent)
        self.parent_window = parent
        self.processor = processor  # TextProcessor 实例
        
        # 初始化处理器
        if self.processor:
            self.processor.initialize()
        
        self.init_ui()
        self.connect_signals()
    
    def init_ui(self):
        """初始化界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(12)
        
        # 输入区域
        input_group = QGroupBox("📝 输入文本")
        input_layout = QVBoxLayout()
        
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("在这里输入要处理的文本...")
        self.input_text.setMaximumHeight(150)
        input_layout.addWidget(self.input_text)
        
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)
        
        # 处理模式选择
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("处理模式:"))
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "转大写 (UPPER)",
            "转小写 (lower)",
            "首字母大写 (Title)",
            "分析文本 (Analyze)"
        ])
        mode_layout.addWidget(self.mode_combo)
        mode_layout.addStretch()
        
        main_layout.addLayout(mode_layout)
        
        # 操作按钮
        button_layout = QHBoxLayout()
        
        self.btn_process = QPushButton("🚀 开始处理")
        self.btn_process.setMinimumHeight(35)
        self.btn_clear = QPushButton("🧹 清空")
        self.btn_clear.setMinimumHeight(35)
        
        button_layout.addStretch()
        button_layout.addWidget(self.btn_process)
        button_layout.addWidget(self.btn_clear)
        
        main_layout.addLayout(button_layout)
        
        # 输出区域
        output_group = QGroupBox("✅ 处理结果")
        output_layout = QVBoxLayout()
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("处理结果将显示在这里...")
        output_layout.addWidget(self.output_text)
        
        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group)
        
        # 统计信息
        self.stats_label = QLabel("统计信息: --")
        self.stats_label.setObjectName("statsLabel")
        main_layout.addWidget(self.stats_label)
        
        # 初始化日志
        self.log("✅ 文本处理模块已加载", "success")
        self.log("💡 提示: 输入文本，选择处理模式，然后点击'开始处理'", "info")
    
    def connect_signals(self):
        """连接信号槽"""
        self.btn_process.clicked.connect(self.on_process_clicked)
        self.btn_clear.clicked.connect(self.on_clear_clicked)
    
    def on_process_clicked(self):
        """处理按钮点击"""
        # 获取输入
        input_data = self.input_text.toPlainText().strip()
        
        if not input_data:
            self.log("⚠️ 请先输入文本！", "warning")
            return
        
        # 获取处理模式
        mode_index = self.mode_combo.currentIndex()
        mode_map = {0: 'upper', 1: 'lower', 2: 'title', 3: 'analyze'}
        mode = mode_map.get(mode_index, 'upper')
        
        self.log(f"📝 处理模式: {self.mode_combo.currentText()}", "info")
        
        # 调用核心处理器
        if self.processor:
            try:
                success = self.processor.process(
                    input_data,
                    options={'mode': mode}
                )
                
                if success:
                    # 获取并显示结果
                    result = self.processor.get_result()
                    self.output_text.setPlainText(result)
                    self.log("✨ 处理完成！", "success")
                    
                    # 显示统计信息
                    stats = self.processor.get_statistics()
                    stats_text = (
                        f"字符数: {stats.get('char_count', 0)} | "
                        f"单词数: {stats.get('word_count', 0)} | "
                        f"行数: {stats.get('line_count', 0)} | "
                        f"空格数: {stats.get('space_count', 0)}"
                    )
                    self.stats_label.setText(f"统计信息: {stats_text}")
                else:
                    self.log("❌ 处理失败", "error")
            
            except Exception as e:
                self.log(f"❌ 错误: {e}", "error")
        else:
            self.log("❌ 没有可用的处理器", "error")
    
    def on_clear_clicked(self):
        """清空"""
        self.output_text.clear()
        self.stats_label.setText("统计信息: --")
        self.log("🧹 已清空输出", "info")
    
    def log(self, message, level="info"):
        """输出日志"""
        from PySide6.QtGui import QTextCursor
        
        color_map = {
            "info": "#0078d4",
            "success": "#107c10",
            "warning": "#ff8c00",
            "error": "#e81123"
        }
        color = color_map.get(level, "#000000")
        
        # 移动到末尾
        cursor = self.output_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.output_text.setTextCursor(cursor)
        self.output_text.insertHtml(f'<span style="color:{color};">{message}</span><br>')
        
        # 更新状态栏
        if self.parent_window and hasattr(self.parent_window, 'statusbar'):
            self.parent_window.statusbar.showMessage(message)
    
    def cleanup(self):
        """清理资源"""
        if self.processor:
            self.processor.cleanup()
