from os.path import join, dirname, abspath

from qtpy.QtCore import Qt, QMetaObject, Signal, Slot, QEvent
from qtpy.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QToolButton,
                            QLabel, QSizePolicy)
from ._utils import QT_VERSION, PLATFORM



_FL_STYLESHEET = join(dirname(abspath(__file__)), 'resources/frameless.qss')
""" str: Frameless window stylesheet. """


class WindowDragger(QWidget):
    """ Window dragger.

        Args:
            window (QWidget): Associated window.
            parent (QWidget, optional): Parent widget.
    """

    doubleClicked = Signal()

    def __init__(self, window, parent=None):
        QWidget.__init__(self, parent)

        self._window = window
        self._mousePressed = False

    def mousePressEvent(self, event):
        self._mousePressed = True
        self._mousePos = event.globalPos()
        self._windowPos = self._window.pos()

    def mouseMoveEvent(self, event):
        if self._mousePressed:
            self._window.move(self._windowPos +
                              (event.globalPos() - self._mousePos))

    def mouseReleaseEvent(self, event):
        self._mousePressed = False

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()


class ModernWindow(QWidget):
    """ Modern window.

        Args:
            w (QWidget): Main widget.
            parent (QWidget, optional): Parent widget.
    """

    def __init__(self, w, parent=None):
        QWidget.__init__(self, parent)

        self._w = w
        self._resizing = False
        self._resize_dir = None
        self._resize_margin = 5  # 边缘热区宽度
        self.setupUi()

        contentLayout = QHBoxLayout()
        contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.addWidget(w)

        self.windowContent.setLayout(contentLayout)

        self.setWindowTitle(w.windowTitle())
        self.setGeometry(w.geometry())

        # Adding attribute to clean up the parent window when the child is closed
        self._w.setAttribute(Qt.WA_DeleteOnClose, True)
        self._w.destroyed.connect(self.__child_was_closed)

    def setupUi(self):
        # create title bar, content
        self.vboxWindow = QVBoxLayout(self)
        self.vboxWindow.setContentsMargins(0, 0, 0, 0)

        self.windowFrame = QWidget(self)
        self.windowFrame.setObjectName('windowFrame')

        self.vboxFrame = QVBoxLayout(self.windowFrame)
        self.vboxFrame.setContentsMargins(0, 0, 0, 0)

        self.titleBar = WindowDragger(self, self.windowFrame)
        self.titleBar.setObjectName('titleBar')
        self.titleBar.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,
                                                QSizePolicy.Fixed))

        self.hboxTitle = QHBoxLayout(self.titleBar)
        self.hboxTitle.setContentsMargins(0, 0, 0, 0)
        self.hboxTitle.setSpacing(0)

        self.lblTitle = QLabel('Title')
        self.lblTitle.setObjectName('lblTitle')
        self.lblTitle.setAlignment(Qt.AlignCenter)

        spButtons = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.btnMinimize = QToolButton(self.titleBar)
        self.btnMinimize.setObjectName('btnMinimize')
        self.btnMinimize.setSizePolicy(spButtons)
        self.btnMinimize.setText('―')  # Windows 水平线

        self.btnRestore = QToolButton(self.titleBar)
        self.btnRestore.setObjectName('btnRestore')
        self.btnRestore.setSizePolicy(spButtons)
        self.btnRestore.setVisible(False)
        self.btnRestore.setText('❐')  # Windows 重叠方块

        self.btnMaximize = QToolButton(self.titleBar)
        self.btnMaximize.setObjectName('btnMaximize')
        self.btnMaximize.setSizePolicy(spButtons)
        self.btnMaximize.setText('□')  # Windows 空心方块

        self.btnClose = QToolButton(self.titleBar)
        self.btnClose.setObjectName('btnClose')
        self.btnClose.setSizePolicy(spButtons)
        self.btnClose.setText('✕')  # Windows 叉号

        self.vboxFrame.addWidget(self.titleBar)

        self.windowContent = QWidget(self.windowFrame)
        self.vboxFrame.addWidget(self.windowContent)

        self.vboxWindow.addWidget(self.windowFrame)

        if PLATFORM == "Darwin":
            self.hboxTitle.addWidget(self.btnClose)
            self.hboxTitle.addWidget(self.btnMinimize)
            self.hboxTitle.addWidget(self.btnRestore)
            self.hboxTitle.addWidget(self.btnMaximize)
            self.hboxTitle.addWidget(self.lblTitle)
        else:
            self.hboxTitle.addWidget(self.lblTitle)
            self.hboxTitle.addWidget(self.btnMinimize)
            self.hboxTitle.addWidget(self.btnRestore)
            self.hboxTitle.addWidget(self.btnMaximize)
            self.hboxTitle.addWidget(self.btnClose)

        # set window flags
        self.setWindowFlags(
                Qt.Window | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)

        if QT_VERSION >= (5,):
            self.setAttribute(Qt.WA_TranslucentBackground)

        # set stylesheet
        with open(_FL_STYLESHEET, encoding='utf-8') as stylesheet:
            self.setStyleSheet(stylesheet.read())

        # automatically connect slots
        QMetaObject.connectSlotsByName(self)

    def __child_was_closed(self):
        self._w = None  # The child was deleted, remove the reference to it and close the parent window
        self.close()

    def closeEvent(self, event):
        if not self._w:
            event.accept()
        else:
            self._w.close()
            event.setAccepted(self._w.isHidden())

    def setWindowTitle(self, title):
        """ Set window title.

            Args:
                title (str): Title.
        """

        super(ModernWindow, self).setWindowTitle(title)
        self.lblTitle.setText(title)

    @Slot()
    def on_btnMinimize_clicked(self):
        self.setWindowState(Qt.WindowMinimized)

    @Slot()
    def on_btnRestore_clicked(self):
        self.btnRestore.setVisible(False)
        self.btnMaximize.setVisible(True)

        self.setWindowState(Qt.WindowNoState)

    @Slot()
    def on_btnMaximize_clicked(self):
        self.btnRestore.setVisible(True)
        self.btnMaximize.setVisible(False)

        self.setWindowState(Qt.WindowMaximized)

    @Slot()
    def on_btnClose_clicked(self):
        self.close()

    @Slot()
    def on_titleBar_doubleClicked(self):
        if self.btnMaximize.isVisible():
            self.on_btnMaximize_clicked()
        else:
            self.on_btnRestore_clicked()
    
    def mousePressEvent(self, event):
        """鼠标按下事件 - 用于边缘拖动调整大小"""
        if event.button() == Qt.LeftButton:
            self._resize_dir = self._get_resize_direction(event.pos())
            if self._resize_dir:
                self._resizing = True
                self._mouse_press_pos = event.globalPos()
                self._window_rect = self.geometry()
                event.accept()
                return
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件 - 调整窗口大小或更改光标"""
        if self._resizing and self._resize_dir:
            self._resize_window(event.globalPos())
            event.accept()
        else:
            # 更改光标样式
            resize_dir = self._get_resize_direction(event.pos())
            if resize_dir:
                self._set_cursor_shape(resize_dir)
            else:
                self.unsetCursor()
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self._resizing = False
            self._resize_dir = None
            self.unsetCursor()
        super().mouseReleaseEvent(event)
    
    def _get_resize_direction(self, pos):
        """获取调整大小的方向"""
        if self.isMaximized():
            return None
        
        margin = self._resize_margin
        x, y = pos.x(), pos.y()
        w, h = self.width(), self.height()
        
        # 判断边缘位置
        on_left = x <= margin
        on_right = x >= w - margin
        on_top = y <= margin
        on_bottom = y >= h - margin
        
        # 返回方向
        if on_top and on_left:
            return 'top-left'
        elif on_top and on_right:
            return 'top-right'
        elif on_bottom and on_left:
            return 'bottom-left'
        elif on_bottom and on_right:
            return 'bottom-right'
        elif on_left:
            return 'left'
        elif on_right:
            return 'right'
        elif on_top:
            return 'top'
        elif on_bottom:
            return 'bottom'
        return None
    
    def _set_cursor_shape(self, direction):
        """设置光标形状"""
        cursor_map = {
            'top': Qt.SizeVerCursor,
            'bottom': Qt.SizeVerCursor,
            'left': Qt.SizeHorCursor,
            'right': Qt.SizeHorCursor,
            'top-left': Qt.SizeFDiagCursor,
            'bottom-right': Qt.SizeFDiagCursor,
            'top-right': Qt.SizeBDiagCursor,
            'bottom-left': Qt.SizeBDiagCursor,
        }
        cursor = cursor_map.get(direction)
        if cursor:
            self.setCursor(cursor)
    
    def _resize_window(self, global_pos):
        """调整窗口大小"""
        delta = global_pos - self._mouse_press_pos
        x, y = self._window_rect.x(), self._window_rect.y()
        w, h = self._window_rect.width(), self._window_rect.height()
        
        # 根据方向调整
        if 'left' in self._resize_dir:
            new_x = x + delta.x()
            new_w = w - delta.x()
            if new_w >= self.minimumWidth():
                x = new_x
                w = new_w
        
        if 'right' in self._resize_dir:
            w = max(w + delta.x(), self.minimumWidth())
        
        if 'top' in self._resize_dir:
            new_y = y + delta.y()
            new_h = h - delta.y()
            if new_h >= self.minimumHeight():
                y = new_y
                h = new_h
        
        if 'bottom' in self._resize_dir:
            h = max(h + delta.y(), self.minimumHeight())
        
        self.setGeometry(x, y, w, h)
