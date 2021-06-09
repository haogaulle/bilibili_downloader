# 哔哩哔哩视频下载脚本（GUI）

**提示：** 如本项目对您有所帮助，请帮忙点一个⭐star支持一下作者。您的鼓励是我持续维护和优化本项目的最大动力。如有任何问题欢迎提交issue或discussion与我联系。



### Description

**特此声明：** 本项目用于学习交流，禁止用于任何商业用途！

- 通过输入视频 **URL** 下载哔哩哔哩视频 ( *BV号版本正在更新中......* )
- 下载的视频会保存在代码同目录下的文件夹"**下载视频**"中 ( *<u>自定义路径</u>已经在路上啦！* ):clap:
- 脚本运行过程中会产生"**工作环境**"目录，别管它，它很快就会消失 :sunglasses:
- 暂时仅支持下载目标视频的 **最高画质**
- ~~未能正确请求到视频页面时，程序会**闪退** ( *将会尽快被优化* )~~
- 由[@HaoGaulle](https://github.com/HaoGaulle) 完成脚本的编写，也正时刻欢迎你的帮助！



### Dependencies

- Windows10 x64 
- Ubuntu 20.04.2.0+
- Python 3.8+
- macOS系统下未知，欢迎尝试
- 相关库详见requirements.txt



### Usage

##### 安装Python
- 详见百度

##### 运行方式

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

4. 打开脚本所在文件夹，运行"**bilibili下载器.pyw**"

5. 输入URL和文件名即可开始下载视频

6. 请耐心等待下载进程

7. 下载完成后可在代码同目录下的文件夹"**下载视频**"中找到刚刚下载好的视频

### Update
1. 修复了未能正确请求到网页时闪退的问题
2. 新增 **弹窗提醒**

### End

本项目将由[@HaoGaulle](https://github.com/HaoGaulle) 持续维护:point_left:

如有任何问题或建议欢迎提交issue或discussion与我联系！

感谢使用！
