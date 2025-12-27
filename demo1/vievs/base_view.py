"""
视图基类
"""
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal


class BaseView(QWidget):
    """视图基类"""
    
    # 定义信号
    data_changed = Signal(object)
    error_occurred = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.connect_signals()
    
    def init_ui(self):
        """初始化UI - 子类重写"""
        pass
    
    def connect_signals(self):
        """连接信号槽 - 子类重写"""
        pass
    
    def show_message(self, message, msg_type="info"):
        """显示消息"""
        from PySide6.QtWidgets import QMessageBox
        
        if msg_type == "info":
            QMessageBox.information(self, "提示", message)
        elif msg_type == "warning":
            QMessageBox.warning(self, "警告", message)
        elif msg_type == "error":
            QMessageBox.critical(self, "错误", message)
    
    def update_view(self, data):
        """更新视图 - 子类重写"""
        pass
