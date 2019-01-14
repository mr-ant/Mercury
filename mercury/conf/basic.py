# coding=utf-8
import os
from maya import cmds

# 项目地址
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 创建工作目录，默认位置在用户文件夹==> maya.
WORK_ON_DIR = os.path.join(cmds.internalVar(userAppDir=True), 'Mercury')

# 工程地址，接收一个绝对路径地址列表，用于展示文件，并分类。
PROJECT_DIR = []
