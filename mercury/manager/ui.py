# coding=utf-8
import pprint

from maya import cmds

from PySide2 import QtWidgets, QtCore, QtGui
from .core import maya_main_window, ManagerFiles


class MainUI(QtWidgets.QDialog):
    """
    这个用来显示控制器面板
    """

    def __init__(self, parent=maya_main_window()):
        super(MainUI, self).__init__(parent)

        self.setWindowTitle("Mercury File Manager for Maya")
        # 移除问号。
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.library = ManagerFiles()

        self.buildUI()

    def buildUI(self):
        layout = QtWidgets.QVBoxLayout(self)
        saveWidget = QtWidgets.QWidget()
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)
        layout.addWidget(saveWidget)

        self.saveNameField = QtWidgets.QLineEdit()
        saveLayout.addWidget(self.saveNameField)

        saveBtn = QtWidgets.QPushButton('Save')
        saveBtn.clicked.connect(self.save)
        saveLayout.addWidget(saveBtn)

        size = 64
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.listWidget.setIconSize(QtCore.QSize(size, size))
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.listWidget.setGridSize(QtCore.QSize(size + 12, size + 12))
        layout.addWidget(self.listWidget)

        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        layout.addWidget(btnWidget)

        importBtn = QtWidgets.QPushButton("Import!")
        importBtn.clicked.connect(self.load)
        btnLayout.addWidget(importBtn)

        refreshBtn = QtWidgets.QPushButton("Refresh")
        refreshBtn.clicked.connect(self.populate)
        btnLayout.addWidget(refreshBtn)

        closeBtn = QtWidgets.QPushButton("Close")
        closeBtn.clicked.connect(self.close)
        btnLayout.addWidget(closeBtn)

        self.populate()

    def load(self):
        """
        加载文件
        :return: None
        """
        currentItem = self.listWidget.currentItem()
        if not currentItem:
            return

        name = currentItem.text()
        self.library.load(name)

    def save(self):
        """
        保存文件
        :return: None
        """
        name = self.saveNameField.text()

        if not name.strip():
            cmds.warning("You must give a name!")
            return
        self.library.save(name)
        self.populate()
        self.saveNameField.setText("")

    def populate(self):
        """
        加载文件，将目录中符合要求的文件加载到列表中。
        :return:
        """
        self.listWidget.clear()
        self.library.find()

        for name, info in self.library.items():
            item = QtWidgets.QListWidgetItem(name)
            item.setToolTip(pprint.pformat(info))

            thumbnail = info.get('thumbnail')
            if thumbnail:
                icon = QtGui.QIcon(thumbnail)
                item.setIcon(icon)

            self.listWidget.addItem(item)
