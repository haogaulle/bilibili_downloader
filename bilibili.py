import os
import sys
import requests
from lxml import etree
import re
import moviepy.editor
import json


def get_video(jiemian, temp_url, filename):
# https://www.bilibili.com/video/BV1EX4y157hD
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
        jiemian.ui.textBrowser.append('已获取服务器正确响应! (响应码: 200)')
    else:
        jiemian.ui.textBrowser.append('未能获取服务器正确响应:\n   错误码: ' + str(response.status_code))
        jiemian.ui.textBrowser.append('本程序已经终止!')
        sys.exit(0)
    jiemian.ui.textBrowser.append('正在解析网页……')
    page = response.content.decode('utf-8')
    tree = etree.HTML(page)
    jiemian.ui.textBrowser.append('正在捕捉json文件……')
    script = tree.xpath('/html/head/script[5]/text()')[0]
    script = re.sub('window.__playinfo__=', '', script)
    jiemian.ui.textBrowser.append('正在重载信息树……')
    script = json.loads(script)

# 下载视频
    jiemian.ui.textBrowser.append('开始下载视频文件……')
    if not os.path.exists('工作环境'):
        os.makedirs('./工作环境')
    if not os.path.exists('下载视频'):
        os.makedirs('./下载视频')
    jiemian.ui.textBrowser.append('正在捕获url……')
    url = script['data']['dash']['video'][0]['baseUrl']
    headers = {
        'authority': '',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.182 Safari/537.36',
        'origin': 'https://www.bilibili.com',
        'referer': 'https://www.bilibili.com/',
        'Range': ''
    }
    headers['authority'] = re.findall('https://(.*?)/', url)[-1]
    video_range = 'bytes=0-%d'
    headers['Range'] = format(video_range % 1000)
    jiemian.ui.textBrowser.append('正在获取数据容量……')
    response = requests.get(url=url, headers=headers)
    video_length = int(response.headers['Content-Range'].split('/')[-1]) - 1
    jiemian.ui.textBrowser.append('正在修改二次请求参数……')
    headers['Range'] = format(video_range % video_length)
    jiemian.ui.textBrowser.append('正在写入数据……')
    response = requests.get(url=url, headers=headers)
    with open('./工作环境/bilibili.mp4', 'wb') as fp:
        fp.write(response.content)
    jiemian.ui.textBrowser.append('视频文件下载完成!')

# 下载音频
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
    with open('./工作环境/bilibili.mp3', 'wb') as fp:
        fp.write(response.content)
    jiemian.ui.textBrowser.append('音频文件下载完成!')

# 音视频混流
    jiemian.ui.textBrowser.append('开始进行数据混流……')
    jiemian.ui.textBrowser.append('正在进行数据混流……(请耐心等待)')
    video = moviepy.editor.VideoFileClip('./工作环境/bilibili.mp4')
    audio = moviepy.editor.AudioFileClip('./工作环境/bilibili.mp3')
    video = video.set_audio(audio)
    video.write_videofile('./下载视频/' + filename + '.mp4')
    jiemian.ui.textBrowser.append('数据混流完成！')

# 删除中间音视频工程文件
    jiemian.ui.textBrowser.append('正在清洗工作环境……')
    os.remove('./工作环境/bilibili.mp3')
    os.remove('./工作环境/bilibili.mp4')
    os.rmdir('./工作环境')  # 删除目录
    jiemian.ui.textBrowser.append('视频下载成功!')


if __name__ == '__main__':
    url = ''
    get_video(none,url)
