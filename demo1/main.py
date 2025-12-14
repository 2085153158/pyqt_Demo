import sys, os
from PySide6.QtWidgets import QApplication
from PySide6 import QtWidgets, QtCore, QtGui
from vievs import *
import qtmodern.styles
import qtmodern.windows


class MainWindow(QtWidgets.QMainWindow, main_ui.Ui_MainWindow):
    MIN_WIDTH= 750
    MIN_HEIGHT= 500

    def __init__(self):
        super().__init__()  # 初始化 QMainWindow
        self.setupUi(self)  # 绑定 Ui_MainWindow 的控件到 self
        self.setWindowTitle("PuzzleSolver v1.0.5  Author: Byxs20")
        self.setMinimumSize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.setWindowIcon(QtGui.QIcon("./resources/icons/Logo.ico"))


def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app= QApplication(sys.argv)
    window= MainWindow()

    qtmodern.styles.dark(app)
    window= qtmodern.windows.ModernWindow(window)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()