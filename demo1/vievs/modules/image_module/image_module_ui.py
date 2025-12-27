# -*- coding: utf-8 -*-
"""
图像处理模块UI
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QGroupBox, QComboBox, QFileDialog,
                               QTextEdit, QCheckBox, QSpinBox, QFormLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class ImageModuleUI(QWidget):
    """图像处理模块UI"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.current_image_path = ""
        
        self.init_ui()
        self.connect_signals()
    
    def init_ui(self):
        """初始化界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(12)
        
        # 文件选择区域
        file_group = QGroupBox("📁 图像文件")
        file_layout = QHBoxLayout()
        
        self.file_label = QLabel("未选择文件")
        file_layout.addWidget(self.file_label)
        
        self.btn_browse = QPushButton("📁 浏览...")
        self.btn_browse.setMaximumWidth(100)
        file_layout.addWidget(self.btn_browse)
        
        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)
        
        # 处理选项
        options_group = QGroupBox("⚙️ 处理选项")
        options_layout = QFormLayout()
        
        # 处理类型
        self.process_combo = QComboBox()
        self.process_combo.addItems([
            "灰度化",
            "二值化", 
            "边缘检测",
            "模糊处理",
            "锐化",
            "旋转",
            "缩放"
        ])
        options_layout.addRow("处理类型:", self.process_combo)
        
        # 质量参数
        self.quality_spin = QSpinBox()
        self.quality_spin.setRange(1, 100)
        self.quality_spin.setValue(85)
        options_layout.addRow("质量:", self.quality_spin)
        
        # 保留原图
        self.keep_original_check = QCheckBox("保留原始图像")
        self.keep_original_check.setChecked(True)
        options_layout.addRow(self.keep_original_check)
        
        options_group.setLayout(options_layout)
        main_layout.addWidget(options_group)
        
        # 操作按钮
        button_layout = QHBoxLayout()
        
        self.btn_process = QPushButton("🚀 开始处理")
        self.btn_process.setMinimumHeight(35)
        self.btn_preview = QPushButton("👁️ 预览")
        self.btn_preview.setMinimumHeight(35)
        self.btn_save = QPushButton("💾 保存结果")
        self.btn_save.setMinimumHeight(35)
        
        button_layout.addStretch()
        button_layout.addWidget(self.btn_preview)
        button_layout.addWidget(self.btn_process)
        button_layout.addWidget(self.btn_save)
        
        main_layout.addLayout(button_layout)
        
        # 日志输出
        log_group = QGroupBox("📋 处理日志")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(180)
        self.log_text.setPlaceholderText("处理日志将显示在这里...")
        log_layout.addWidget(self.log_text)
        
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)
        
        # 添加伸缩
        main_layout.addStretch()
        
        # 初始日志
        self.log("✅ 图像处理模块已加载")
        self.log("💡 提示: 请先选择图像文件，然后选择处理类型")
    
    def connect_signals(self):
        """连接信号槽"""
        self.btn_browse.clicked.connect(self.on_browse_clicked)
        self.btn_process.clicked.connect(self.on_process_clicked)
        self.btn_preview.clicked.connect(self.on_preview_clicked)
        self.btn_save.clicked.connect(self.on_save_clicked)
    
    def on_browse_clicked(self):
        """浏览文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "选择图像文件", 
            "", 
            "图像文件 (*.png *.jpg *.jpeg *.bmp *.gif);;所有文件 (*)"
        )
        if file_path:
            self.current_image_path = file_path
            import os
            self.file_label.setText(os.path.basename(file_path))
            self.log(f"📁 已选择: {os.path.basename(file_path)}")
    
    def on_process_clicked(self):
        """开始处理"""
        if not self.current_image_path:
            self.log("⚠️ 请先选择图像文件！")
            return
        
        process_type = self.process_combo.currentText()
        quality = self.quality_spin.value()
        keep_original = self.keep_original_check.isChecked()
        
        self.log(f"🔧 处理类型: {process_type}")
        self.log(f"📊 质量参数: {quality}")
        self.log(f"🚀 开始处理图像...")
        
        # TODO: 调用实际的图像处理逻辑
        self.log("✨ 处理完成！")
    
    def on_preview_clicked(self):
        """预览"""
        if not self.current_image_path:
            self.log("⚠️ 请先选择图像文件！")
            return
        self.log("👁️ 预览功能开发中...")
    
    def on_save_clicked(self):
        """保存结果"""
        if not self.current_image_path:
            self.log("⚠️ 没有可保存的结果！")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存处理结果",
            "",
            "PNG图像 (*.png);;JPEG图像 (*.jpg);;所有文件 (*)"
        )
        if file_path:
            self.log(f"💾 已保存到: {file_path}")
    
    def log(self, message):
        """输出日志"""
        from PySide6.QtGui import QTextCursor
        
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.log_text.setTextCursor(cursor)
        self.log_text.append(message)
        
        # 更新状态栏
        if self.parent_window and hasattr(self.parent_window, 'statusbar'):
            self.parent_window.statusbar.showMessage(message)
    
    def cleanup(self):
        """清理资源"""
        pass
