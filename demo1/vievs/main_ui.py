# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(850, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setObjectName(u"mainLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_outer_1 = QWidget()
        self.tab_outer_1.setObjectName(u"tab_outer_1")
        self.outerTabLayout = QVBoxLayout(self.tab_outer_1)
        self.outerTabLayout.setObjectName(u"outerTabLayout")
        self.innerTabContainer = QWidget(self.tab_outer_1)
        self.innerTabContainer.setObjectName(u"innerTabContainer")
        self.innerContainerLayout = QVBoxLayout(self.innerTabContainer)
        self.innerContainerLayout.setObjectName(u"innerContainerLayout")
        self.innerContainerLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget_inner = QTabWidget(self.innerTabContainer)
        self.tabWidget_inner.setObjectName(u"tabWidget_inner")
        self.tab_inner_1 = QWidget()
        self.tab_inner_1.setObjectName(u"tab_inner_1")
        self.innerTab1Layout = QVBoxLayout(self.tab_inner_1)
        self.innerTab1Layout.setObjectName(u"innerTab1Layout")
        self.tabWidget_inner.addTab(self.tab_inner_1, "")
        self.tab_inner_2 = QWidget()
        self.tab_inner_2.setObjectName(u"tab_inner_2")
        self.innerTab2Layout = QVBoxLayout(self.tab_inner_2)
        self.innerTab2Layout.setObjectName(u"innerTab2Layout")
        self.tabWidget_inner.addTab(self.tab_inner_2, "")

        self.innerContainerLayout.addWidget(self.tabWidget_inner)


        self.outerTabLayout.addWidget(self.innerTabContainer)

        self.tabWidget.addTab(self.tab_outer_1, "")
        self.tab_outer_2 = QWidget()
        self.tab_outer_2.setObjectName(u"tab_outer_2")
        self.outerTab2Layout = QVBoxLayout(self.tab_outer_2)
        self.outerTab2Layout.setObjectName(u"outerTab2Layout")
        self.tabWidget.addTab(self.tab_outer_2, "")

        self.mainLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 850, 33))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.tabWidget_inner.setTabText(self.tabWidget_inner.indexOf(self.tab_inner_1), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.tabWidget_inner.setTabText(self.tabWidget_inner.indexOf(self.tab_inner_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_outer_1), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_outer_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u5de5\u5177", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9", None))
    # retranslateUi

