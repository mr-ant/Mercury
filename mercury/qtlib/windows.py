import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from mercury.qtlib import QtWidgets


def maya_main_window():
    win = omui.MQtUtil_mainWindow()
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
    return ptr
