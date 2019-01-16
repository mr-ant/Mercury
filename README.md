# Mercury
一个文件管理的插件。  
* 讨论，求助：https://ttmeow.com
* Code Bug：https://github.com/mr-ant/Mercury/issues
# 安装方式
1. 下载`mercury.zip` 或者下载源码，或者使用git方式，然后复制 `mercury` 『注意是小写的文件夹』到  
    * OSX: `~/Library/Preferences/Autodesk/maya/scripts`  
    * Linux: `~/maya/scripts`  
    * Windows: `C:/Users/USERNAME/Documents/maya/scripts`   
2. 打开 Maya2018，打开脚本编辑器并切换到 Python 标签，之后运行下面的代码
```python
from mercury import ui
ui.show()
```
3. Down

# 使用方式
秉持着简洁的设计原则，尽可能的让一切操作朝着你所觉得的方向发展。
### 保存文件
保存文件之前，你需要在输入框中输入文件名。理论上来说你可以输入任意文字，但为了保持良好的命名习惯，推荐你采用字母加下划线的方式命名，请以字母开头！
然后点击「Save」保存文件。 文件保存路径，默认文件会保存到：`C:/Users/USERNAME/Documents/maya/Mercury`,下一个版本会支持自定义路径。   
### 导入文件
在对话框中选择你需要导入的文件，然后点击「Import」导入文件。
### 引用文件
选择你需要引用的文件，然后点击「Reference」引用文件。
### 打开文件
选择你需要打开的文件，然后点击「Open」打开文件。注意打开文件的方式没有使用兼容的模式，所以保持高版本能打开低版本的文件，如果你使用低版本打开高版本的
文件，理论上来说会报错。
### 小提示
如果你发现你的文件没有现在在本插件中，请查看以下方式是否可以解决你的问题。
* 你的文件是否是使用本插件保存或导出的。
* 点击 Refresh 刷新一下。
# 帮助这个项目
如果这个项目对你来说有点用，你可以通过这几点来帮助本项目发展。
1. 给这个项目点个 Star
2. 推荐给你的朋友
3. 积极反馈bug，向我提建议
4. 在[社区](https://ttmeow.com)中帮助别的朋友
# 感谢
这个项目启发自 Dhruv Govil 的教学项目 [PythonForMayaSamples](https://github.com/dgovil/PythonForMayaSamples) 中的一个章节。
