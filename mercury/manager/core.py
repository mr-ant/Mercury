# coding=utf-8
import os
import json

import maya.OpenMayaUI as omui
from maya import cmds
from shiboken2 import wrapInstance
from mercury.Qt import QtWidgets

DIRECTORY = os.path.join(cmds.internalVar(userAppDir=True), 'Mercury')


def maya_main_window():
    win = omui.MQtUtil_mainWindow()
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
    return ptr


class ManagerFiles(dict):
    def createrDir(self, directory=DIRECTORY):
        if not os.path.exists(directory):
            os.mkdir(directory)

    def save(self, name, thumbnail=True, directory=DIRECTORY, **info):
        """
        这个方法用来保存场景文件。
        :param name:文件名
        :param thumbnail:缩略图
        :param directory:保存路径
        :param info:信息
        :return:None
        """

        self.generating_data(name, thumbnail, directory, **info)

        if cmds.ls(selection=True):
            # 如果选择了文件，则执行导出文件。
            cmds.file(force=True, exportSelected=True)
        else:
            # 否则，直接强制保存当前文件。
            cmds.file(save=True, force=True)

    def generating_data(self, name, thumbnail=True, directory=DIRECTORY, **info):
        self.createrDir(directory)
        json_file = os.path.join(directory, '%s.json' % name)
        path = os.path.join(directory, '%s.ma' % name)

        if thumbnail:
            info['thumbnail'] = self.saveThumbnail(name, directory=directory)
        info['name'] = name
        info['path'] = path

        cmds.file(rename=path)

        with open(json_file, 'w') as f:
            json.dump(info, f, indent=True)

    def find(self, directory=DIRECTORY):
        """
        查找指定文件夹下的左右文件
        :param directory: 文件路径
        :return: None
        """
        if not os.path.exists(directory):
            return

        files = os.listdir(directory)
        mayaFiles = [f for f in files if f.endswith('.ma')]

        for ma in mayaFiles:
            name, ext = os.path.splitext(ma)
            infoFile = '%s.json' % name
            thumbnail = '%s.jpg' % name
            if infoFile in files:
                infoFile = os.path.join(directory, infoFile)
                with open(infoFile, 'r') as f:
                    data = json.load(f)
            else:
                data = {}

            if thumbnail in files:
                data['thumbnail'] = os.path.join(directory, thumbnail)
            data['name'] = name
            data['path'] = os.path.join(directory, ma)
            self[name] = data

    def load(self, name):
        path = self[name]['path']
        cmds.file(path, i=True, usingNamespaces=False)

    def saveThumbnail(self, name, directory):
        """
        保存拍屏。
        :param name: 当前文件的名字
        :param directory: 保存的路径
        :return: 拍屏图片的绝对路径
        """
        path = os.path.join(directory, '%s.jpg' % name)
        # 适配视图
        cmds.viewFit()
        # 修改渲染设置中的输出文件底下的图片格式为 jpg。
        cmds.setAttr("defaultRenderGlobals.imageFormat", 8)
        # 拍屏
        cmds.playblast(completeFilename=path, forceOverwrite=True, format='image', width=200, height=200,
                       showOrnaments=False, startTime=1, endTime=1, viewer=False)
        return path
