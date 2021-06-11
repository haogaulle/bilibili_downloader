import os
import re
import json
import tempfile
import requests
import win32con
import win32api
import moviepy.editor
from lxml import etree
from time import sleep


def get_video(jiemian, temp_url, filename, path):
    url = temp_url
    headers = {
        'authority': 'www.bilibili.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.182 Safari/537.36',
        'origin': 'https://www.bilibili.com'
    }
    jiemian.ui.textBrowser.append('正在向目标服务器发起请求……')
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        sleep(0.2)
        jiemian.ui.textBrowser.append('已获取服务器正确响应! (响应码: 200)')
    else:
        sleep(0.2)
        jiemian.ui.textBrowser.append('未能获取服务器正确响应:\n   错误码: ' + str(response.status_code))
        jiemian.wrong_signal.emit()
        return 0
    jiemian.ui.textBrowser.append('正在解析网页……')
    page = response.content.decode('utf-8')
    tree = etree.HTML(page)
    jiemian.ui.textBrowser.append('正在捕捉json文件……')
    script = tree.xpath('/html/head/script[5]/text()')[0]
    script = re.sub('window.__playinfo__=', '', script)
    jiemian.ui.textBrowser.append('正在加载json')
    script = json.loads(script)

    # 下载视频
    jiemian.ui.textBrowser.append('开始下载视频文件……')
    """
    # 已优化
    if not os.path.exists('工作环境'):
        os.makedirs('./工作环境')
        win32api.SetFileAttributes('./工作环境', win32con.FILE_ATTRIBUTE_HIDDEN)
    """
    t_dir = tempfile.TemporaryDirectory()  # eg:C:\Users\86181\AppData\Local\Temp\tmpyu5xsn7n
    t_path = t_dir.name
    if not os.path.exists(path):
        os.makedirs(path)
    jiemian.ui.textBrowser.append('正在捕获url……')
    url = script['data']['dash']['video'][0]['baseUrl']
    headers = {'authority': re.findall('https://(.*?)/', url)[-1],
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/88.0.4324.182 Safari/537.36', 'origin': 'https://www.bilibili.com',
               'referer': 'https://www.bilibili.com/', 'Range': ''}
    video_range = 'bytes=0-%d'
    headers['Range'] = format(video_range % 1000)
    sleep(0.2)
    jiemian.ui.textBrowser.append('正在获取数据容量……')
    response = requests.get(url=url, headers=headers)
    video_length = int(response.headers['Content-Range'].split('/')[-1]) - 1
    jiemian.ui.textBrowser.append('正在修改二次请求参数……')
    headers['Range'] = format(video_range % video_length)
    jiemian.ui.textBrowser.append('正在写入数据……')
    response = requests.get(url=url, headers=headers)
    with open(t_path + '/bilibili.mp4', 'wb') as fp:
        fp.write(response.content)
    jiemian.ui.textBrowser.append('视频文件下载完成!')

    # 下载音频
    sleep(0.2)
    jiemian.ui.textBrowser.append('开始下载视频文件……')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.182 Safari/537.36',
        'origin': 'https://www.bilibili.com',
        'referer': 'https://www.bilibili.com/',
        'Range': ''
    }
    audio_range = 'bytes=0-%d'
    headers['Range'] = format(audio_range % 1000)
    jiemian.ui.textBrowser.append('正在捕获url……')
    url = script['data']['dash']['audio'][0]['baseUrl']
    response = requests.get(url=url, headers=headers)
    jiemian.ui.textBrowser.append('正在获取数据容量……')
    audio_length = int(response.headers['Content-Range'].split('/')[-1]) - 1
    jiemian.ui.textBrowser.append('正在修改二次请求参数……')
    headers['Range'] = format(audio_range % audio_length)
    jiemian.ui.textBrowser.append('正在写入数据……')
    response = requests.get(url=url, headers=headers)
    with open(t_path + '/bilibili.mp3', 'wb') as fp:
        fp.write(response.content)
    jiemian.ui.textBrowser.append('音频文件下载完成!')

    # 音视频混流
    sleep(0.2)
    jiemian.ui.textBrowser.append('开始进行数据混流……')
    jiemian.ui.textBrowser.append('正在进行数据混流……(请耐心等待)')
    video = moviepy.editor.VideoFileClip(t_path + '/bilibili.mp4')
    audio = moviepy.editor.AudioFileClip(t_path + '/bilibili.mp3')
    video = video.set_audio(audio)
    video.write_videofile(path + '/' + filename + '.mp4', verbose=False, logger=None)
    jiemian.ui.textBrowser.append('数据混流完成！')

    # 删除中间音视频工程文件(已优化)
    # os.remove('./工作环境/bilibili.mp3')
    # os.remove('./工作环境/bilibili.mp4')
    # os.rmdir('./工作环境')  # 删除目录
    t_dir.cleanup()
    jiemian.ui.textBrowser.append('视频下载成功!')
    jiemian.succ_signal.emit()


if __name__ == '__main__':
    pass
