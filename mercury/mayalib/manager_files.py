# coding=utf-8
import os
import json

from maya import cmds

from mercury.conf import settings

DIRECTORY = settings.WORK_ON_DIR


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

        path = os.path.join(directory, '%s.ma' % name)
        self.generating_data(name, thumbnail, directory, **info)

        if cmds.ls(selection=True):
            # 如果选择了文件，则执行导出文件。
            cmds.file(path, force=True, exportSelected=True, type="mayaAscii")
        else:
            # 否则，直接强制保存当前文件。
            cmds.file(rename=path)
            cmds.file(save=True, force=True)

    def generating_data(self, name, thumbnail=True, directory=DIRECTORY, **info):
        self.createrDir(directory)
        json_file = os.path.join(directory, '%s.json' % name)
        path = os.path.join(directory, '%s.ma' % name)

        if thumbnail:
            info['thumbnail'] = self.saveThumbnail(name, directory=directory)
        info['name'] = name
        info['path'] = path

        with open(json_file, 'w') as f:
            json.dump(info, f, indent=True)

    def open(self, name):
        path = self[name]['path']
        cmds.file(path, force=True, open=True)

    def reference(self, name):
        path = self[name]['path']
        cmds.file(path, reference=True, namespace=name)

    def find(self, directory=DIRECTORY):
        """
        查找指定文件夹下的所有文件
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
