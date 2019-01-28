# coding=utf-8
import pprint

from maya import cmds

from mercury.qtlib import QtWidgets, QtCore, QtGui
from mercury.qtlib import maya_main_window
from mercury.mayalib import ManagerFiles


class MercuryWidget(QtWidgets.QDialog):
    """
    这个用来显示控制器面板
    """

    def __init__(self, parent=maya_main_window()):
        super(MercuryWidget, self).__init__(parent)

        self.setWindowTitle("Mercury File Manager for Maya")
        # 移除问号。
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.library = ManagerFiles()

        self.buildUI()
        self.show()

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

        openBtn = QtWidgets.QPushButton("Open")
        openBtn.clicked.connect(self.open_file)
        btnLayout.addWidget(openBtn)

        refBtn = QtWidgets.QPushButton("Reference")
        refBtn.clicked.connect(self.reference)
        btnLayout.addWidget(refBtn)

        importBtn = QtWidgets.QPushButton("Import")
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
        name = self.get_current_item()
        self.library.load(name)

    def get_current_item(self):
        currentItem = self.listWidget.currentItem()
        if not currentItem:
            return KeyError('Not Exist')

        name = currentItem.text()
        return name

    def open_file(self):
        name = self.get_current_item()
        self.library.open(name)

    def reference(self):
        name = self.get_current_item()
        self.library.reference(name)

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
