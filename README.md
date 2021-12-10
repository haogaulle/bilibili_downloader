# 哔哩哔哩视频下载脚本（GUI）

**提示：** 如本项目对您有所帮助，请帮忙点一个⭐star支持一下作者。您的鼓励是我持续维护和优化本项目的最大动力。如有任何问题欢迎提交issue或discussion与我联系。



### Description

**特此声明：** 本项目用于学习交流，禁止用于任何商业用途！

- 本爬虫采取视频音频分别下载再进行数据混流(ffmpeg)的策略，虽然速度较慢，但无需带cookie
- 通过输入视频 **BV号** 下载哔哩哔哩视频
- 支持自定义下载路径
- 暂时仅支持下载目标视频的 **最高画质**
- 由[@HaoGaulle](https://github.com/HaoGaulle) 完成脚本的编写



### Dependencies
1. master分支gui界面使用 **pyQt5** 实现，可以实现跨平台运行；
   - Windows10 x64 
   - Ubuntu 20.04.2.0+
   - Python 3.8+
   - macOS系统下未知，欢迎尝试
   - 相关库详见requirements.txt
2. tkinter分支gui界面使用python内置模块Tkinter实现，在Linux运行需要安装Tk_模块
   - Windows10 x64 
   - Ubuntu 20.04.2.0+
   - Python 3.8+
   - 相关库详见requirements.txt


## Usage

### 一、下载release文件( **推荐** )
1. 下载release V1.0
2. 解压
3. 运行.exe文件启动程序

### 二、运行源代码
##### 1.安装Python
- 详见百度

##### 2.运行方式

1.  **clone /下载** 本项目到本地

2.  建议使用**虚拟环境**运行( 没有接触过虚拟环境可忽略 )

3.  安装依赖库

    - **win + R** 打开运行菜单
    - 输入**cmd**打开命令提示符
    - 输入：

        ```shell
        pip install -r requirements.txt
        ```
        若安装速度太慢，请切换阿里源：
        ```shell
        pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
        ```
    - 完成安装
    - 关闭命令提示符
    - 下载ffmpeg后复制到/dev目录下

4. 打开脚本所在文件夹，双击运行"**bilibili下载器.pyw**"

5. 输入BV号和文件名、选择下载位置即可开始下载视频

6. 请耐心等待下载进程

### Update
1. 修复了未能正确请求到网页时闪退的问题
2. 新增 **弹窗提醒**
3. 支持**自定义下载路径**
4. 修复了在Ubuntu概率性闪退问题
5. 其它优化

### End

本项目将由[@HaoGaulle](https://github.com/HaoGaulle) 持续维护:point_left:

如有任何问题或建议欢迎提交issue或discussion与我联系！

感谢使用！
