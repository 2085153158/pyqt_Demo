import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QTabBar,
    QFileDialog, QMessageBox, QLabel
)
from PySide6.QtGui import QAction
from PySide6 import QtCore, QtGui
import qtmodern.styles
import qtmodern.windows
from core import DataProcessor


class MainWindow(QMainWindow):
    """主窗口"""
    
    MIN_WIDTH = 750
    MIN_HEIGHT = 500
    
    def __init__(self):
        super().__init__()
        
        # 初始化核心处理器
        self.data_processor = DataProcessor()
        
        # 存储各分类的TabWidget
        self.outer_tab_widget = None
        self.category_tabs = {}
        
        # 设置窗口属性
        self.setWindowTitle("PuzzleSolver Pro v2.0  Build: 2024.9.22")
        self.setMinimumSize(self.MIN_WIDTH, self.MIN_HEIGHT)
        # self.setWindowIcon(QtGui.QIcon("./resources/icons/Logo.ico"))
        
        # 初始化UI
        self.init_ui()
        self.create_menubar()
        self.create_statusbar()
        self.connect_signals()
        
        # 加载模块
        self.load_modules()
    
    def init_ui(self):
        """初始化UI"""
        # 创建中心部件
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        self.mainLayout = QVBoxLayout(central_widget)
        
        # 创建外层TabWidget（分类级别）
        self.outer_tab_widget = QTabWidget(self)
        self.outer_tab_widget.setObjectName("outerTabWidget")
        
        # 为外层TabWidget设置TabBar
        outer_tab_bar = QTabBar(self.outer_tab_widget)
        outer_tab_bar.setObjectName("outerTabBar")
        self.outer_tab_widget.setTabBar(outer_tab_bar)
        
        # 设置TabWidget属性，使标签页更像按钮
        self.outer_tab_widget.setDocumentMode(False)  # 不使用文档模式
        self.outer_tab_widget.setUsesScrollButtons(True)  # 启用滚动按钮
        self.outer_tab_widget.setElideMode(QtCore.Qt.ElideNone)  # 不省略文本
        
        self.mainLayout.addWidget(self.outer_tab_widget)
    
    def create_menubar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 工具菜单
        menu_tools = menubar.addMenu("工具")
        
        self.action_open = QAction("打开...", self)
        self.action_open.setShortcut("Ctrl+O")
        menu_tools.addAction(self.action_open)
        
        self.action_save = QAction("保存", self)
        self.action_save.setShortcut("Ctrl+S")
        menu_tools.addAction(self.action_save)
        
        menu_tools.addSeparator()
        
        self.action_settings = QAction("设置...", self)
        menu_tools.addAction(self.action_settings)
        
        menu_tools.addSeparator()
        
        self.action_exit = QAction("退出", self)
        self.action_exit.setShortcut("Ctrl+Q")
        menu_tools.addAction(self.action_exit)
        
        # 帮助菜单
        menu_help = menubar.addMenu("帮助")
        
        self.action_help = QAction("帮助文档", self)
        self.action_help.setShortcut("F1")
        menu_help.addAction(self.action_help)
        
        self.action_about = QAction("关于...", self)
        menu_help.addAction(self.action_about)
    
    def create_statusbar(self):
        """创建状态栏"""
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("就绪")
    
    def connect_signals(self):
        """连接信号槽"""
        # 菜单栏动作
        self.action_open.triggered.connect(self.on_action_open)
        self.action_save.triggered.connect(self.on_action_save)
        self.action_exit.triggered.connect(self.close)
        self.action_about.triggered.connect(self.on_action_about)
    
    # ==================== 菜单栏动作 ====================
    def on_action_open(self):
        """打开文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开文件", "", "所有文件 (*)"
        )
        if file_path:
            self.load_file(file_path)
    
    def on_action_save(self):
        """保存文件"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存文件", "", "文本文件 (*.txt);;所有文件 (*)"
        )
        if file_path:
            self.save_file(file_path)
    
    def on_action_about(self):
        """显示关于对话框"""
        QMessageBox.about(
            self,
            "关于",
            "<h2>PuzzleSolver Pro v2.0</h2>"
            "<p>基于 PySide6 开发的现代化应用程序</p>"
            "<p><b>作者:</b> Byxs20</p>"
            "<p><b>版本:</b> 2.0</p>"
            "<p><b>更新日期:</b> 2024</p>"
        )
    
    # ==================== 核心功能 ====================
    def load_file(self, file_path):
        """加载文件"""
        try:
            success = self.data_processor.load_data(file_path)
            if success:
                self.statusbar.showMessage(f"已加载: {os.path.basename(file_path)}")
            else:
                QMessageBox.warning(self, "警告", "加载文件失败！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载文件时出错: {e}")
    
    def save_file(self, file_path):
        """保存文件"""
        try:
            # 这里添加保存逻辑
            self.statusbar.showMessage("文件保存成功")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存文件时出错: {e}")
    
    def closeEvent(self, event):
        """关闭事件"""
        # 清理资源
        self.data_processor.cleanup()
        # 清理模块
        if self.outer_tab_widget:
            for i in range(self.outer_tab_widget.count()):
                inner_tab = self.outer_tab_widget.widget(i)
                if isinstance(inner_tab, QTabWidget):
                    for j in range(inner_tab.count()):
                        widget = inner_tab.widget(j)
                        if hasattr(widget, 'cleanup'):
                            widget.cleanup()
        event.accept()
    
    # ==================== 模块管理 ====================
    def add_category(self, category_name, index=None):
        """添加分类（外层TabWidget）"""
        if category_name in self.category_tabs:
            print(f"分类 {category_name} 已存在")
            return
        
        # 创建该分类的内层TabWidget
        inner_tab = QTabWidget()
        inner_tab.setObjectName(f"innerTab_{category_name}")
        
        # 为内层TabWidget设置TabBar
        inner_tab_bar = QTabBar(inner_tab)
        inner_tab_bar.setObjectName(f"innerTabBar_{category_name}")
        inner_tab.setTabBar(inner_tab_bar)
        
        # 设置内层TabWidget属性
        inner_tab.setDocumentMode(False)
        inner_tab.setUsesScrollButtons(True)
        inner_tab.setElideMode(QtCore.Qt.ElideNone)
        
        self.category_tabs[category_name] = inner_tab
        
        # 添加到外层TabWidget
        if index is None:
            self.outer_tab_widget.addTab(inner_tab, category_name)
        else:
            self.outer_tab_widget.insertTab(index, inner_tab, category_name)
        
        print(f"✅ 分类 '{category_name}' 添加成功")
    
    def add_module(self, category_name, module_name, widget, icon=None):
        """添加模块到指定分类的内层TabWidget"""
        if category_name not in self.category_tabs:
            print(f"分类 {category_name} 不存在")
            return
        
        inner_tab = self.category_tabs[category_name]
        
        # 添加到内层TabWidget
        if icon:
            inner_tab.addTab(widget, icon, module_name)
        else:
            inner_tab.addTab(widget, module_name)
        
        print(f"  ✅ 模块 '{module_name}' 添加到分类 '{category_name}'")
    
    def load_modules(self):
        """加载模块 - 双层结构"""
        from vievs.modules.text_module import TextModuleUI
        from vievs.modules.image_module import ImageModuleUI
        from core import TextProcessor
        
        # ========== 1. 图像处理分类 ==========
        self.add_category('图像处理', 0)
        
        # 1.1 区块处理
        image_ui = ImageModuleUI(self)
        self.add_module('图像处理', '区块处理', image_ui)
        
        # 1.2 单帧图处理
        single_frame_ui = self._create_placeholder("🎯 单帧图处理")
        self.add_module('图像处理', '单帧图处理', single_frame_ui)
        
        # 1.3 双重编码编码
        double_encode_ui = self._create_placeholder("🔐 双重编码编码")
        self.add_module('图像处理', '双重编码编码', double_encode_ui)
        
        # 1.4 块是处理
        block_ui = self._create_placeholder("🧩 块是处理")
        self.add_module('图像处理', '块是处理', block_ui)
        
        # 1.5 除工具条
        tool_ui = self._create_placeholder("🔧 除工具条")
        self.add_module('图像处理', '除工具条', tool_ui)
        
        # ========== 2. 物理处理分类 ==========
        self.add_category('物理处理', 1)
        
        # 2.1 ImageSteganography
        steg_ui = self._create_placeholder("🔍 ImageSteganography")
        self.add_module('物理处理', 'ImageSteganography', steg_ui)
        
        # 2.2 BruteForceImage
        brute_ui = self._create_placeholder("🔑 BruteForceImage")
        self.add_module('物理处理', 'BruteForceImage', brute_ui)
        
        # ========== 3. 文本处理分类 ==========
        self.add_category('文本处理', 2)
        
        # 3.1 文本处理
        text_processor = TextProcessor()
        text_ui = TextModuleUI(self, text_processor)
        self.add_module('文本处理', '文本处理', text_ui)
        
        # ========== 4. 文件处理分类 ==========
        self.add_category('文件处理', 3)
        
        # 4.1 FrequencyColor
        freq_ui = self._create_placeholder("🎨 FrequencyColor")
        self.add_module('文件处理', 'FrequencyColor', freq_ui)
        
        # ========== 5. 块是处理分类 ==========
        self.add_category('块是处理', 4)
        
        # 5.1 GIF
        gif_ui = self._create_placeholder("🎬 GIF")
        self.add_module('块是处理', 'GIF', gif_ui)
        
        # ========== 6. 关于分类 ==========
        self.add_category('关于', 5)
        
        # 6.1 Misc
        misc_ui = self._create_placeholder("📦 Misc")
        self.add_module('关于', 'Misc', misc_ui)
    
    def _create_placeholder(self, title):
        """创建占位模块"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        label = QLabel(f"{title}\n\n功能开发中...")
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setObjectName("placeholderLabel")
        layout.addWidget(label)
        return widget


def main():
    """主函数"""
    # 设置高DPI缩放
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # 创建应用
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    
    # 应用qtmodern暗黑主题（保持Windows风格按钮）
    qtmodern.styles.dark(app)
    
    # 使用ModernWindow包装（提供拖动、缩放功能）
    modern_window = qtmodern.windows.ModernWindow(window)
    modern_window.show()
    
    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()