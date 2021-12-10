import os
import re
import json
import tempfile
import requests
import subprocess
# import win32con
# import win32api
# import moviepy.editor
# from lxml import etree
# from time import sleep
# from requests.exceptions import MissingSchema


LOG = ""
STATUS_CODE = 0
PER = 0


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/95.0.4638.69 Safari/537.36',
}


video_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/95.0.4638.69 Safari/537.36',
    'range': 'bytes=0-',
    'referer': 'https://www.bilibili.com',
}


def get_cid(bvid: str) -> str:
    url = 'https://api.bilibili.com/x/player/pagelist?bvid=' + bvid
    res = requests.get(url).json()
    return res['data'][0]['cid']


def get_url(cid: str, bvid: str) -> []:
    global headers
    url = 'https://api.bilibili.com/x/player/playurl'
    params = {
        'cid': cid,
        'bvid': bvid,
        'fnval': '976'
    }
    res = requests.get(url=url, params=params, headers=headers)
    res = res.json()
    return [res['data']['dash']['video'][0]['base_url'], res['data']['dash']['audio'][0]['base_url']]


def handle_time(ts):
    ts = ts.split(':')
    t_length = int(ts[0]) * 3600
    t_length += int(ts[1]) * 60
    ts_s = ts[2].split('.')
    t_length += int(ts_s[0]) + int(ts_s[1]) * 0.01
    return t_length


def get_video(myWindow, temp_url, filename, path):
    global LOG, STATUS_CODE, PER, video_headers

    PER = "00.00 %"
    myWindow.event_generate("<<per>>")

    bvid = temp_url  # 视频BV号

    # myWindow.log_signal.emit('正在向目标服务器发起请求……')
    LOG = '正在向目标服务器发起请求……'
    myWindow.event_generate('<<log>>')

    # 获取cid
    LOG = '正在获取视频cid'
    myWindow.event_generate('<<log>>')
    try:
        cid = get_cid(bvid=bvid)  # 获取视频的cid
    except Exception:
        STATUS_CODE = 404
        myWindow.event_generate('<<status>>')  # 报错连接失败
        return
    LOG = 'cid获取成功'
    myWindow.event_generate('<<log>>')
    PER = "5.45 %"
    myWindow.event_generate("<<per>>")

    # 获取视频url
    LOG = '正在获取视频url'
    myWindow.event_generate('<<log>>')
    try:
        urls = get_url(cid=cid, bvid=bvid)  # 获取视频的url
    except Exception:
        STATUS_CODE = 404
        myWindow.event_generate('<<status>>')  # 报错连接失败
        return
    LOG = '视频url获取成功'
    myWindow.event_generate('<<log>>')
    PER = "10.28 %"
    myWindow.event_generate("<<per>>")

    # 已废弃
    # try:
    #     response = requests.get(url=url, headers=headers)
    # except MissingSchema:
    #     response = None
    #     LOG = "请输入正确的URL！"
    #     myWindow.event_generate('<<log>>')
    #     # myWindow.log_signal.emit('进程已中止')
    #     LOG = '进程已中止'
    #     myWindow.event_generate('<<log>>')
    #     STATUS_CODE = 404
    #     myWindow.event_generate('<<status>>')
    #     return 0
    # if response.status_code == 200:
    #     sleep(0.2)
    #     LOG = '已获取服务器正确响应(status_code = 200)'
    #     myWindow.event_generate('<<log>>')
    #     # myWindow.log_signal.emit('已获取服务器正确响应! (响应码: 200)')
    # else:
    #     sleep(0.2)
    #     LOG = '未能获取服务器正确响应:\n   错误码: ' + str(response.status_code)
    #     myWindow.event_generate('<<log>>')
    #     # myWindow.log_signal.emit('未能获取服务器正确响应:\n   错误码: ' + str(response.status_code))
    #     LOG = '进程已中止'
    #     myWindow.event_generate('<<log>>')
    #     # myWindow.log_signal.emit('进程已中止')
    #     STATUS_CODE = 404
    #     myWindow.event_generate('<<status>>')
    #     # myWindow.wrong_signal.emit('连接失败！')
    #     return 0
    #
    # PER = "5.01 %"
    # myWindow.event_generate("<<per>>")
    #
    # LOG = '正在解析网页'
    # myWindow.event_generate('<<log>>')
    # # myWindow.log_signal.emit('正在解析网页……')
    #
    # page = response.content.decode('utf-8')
    # tree = etree.HTML(page)
    #
    # LOG = '正在捕捉json文件……'
    # myWindow.event_generate('<<log>>')
    # # myWindow.log_signal.emit('正在捕捉json文件……')
    # script = tree.xpath('/html/head/script[5]/text()')[0]
    # script = re.sub('window.__playinfo__=', '', script)
    #
    # LOG = '正在加载json'
    # myWindow.event_generate('<<log>>')
    # # myWindow.log_signal.emit('正在加载json')
    # script = json.loads(script)

    script = urls  # 映射

    # 下载视频
    LOG = '开始下载视频文件……'
    myWindow.event_generate('<<log>>')
    # myWindow.log_signal.emit('开始下载视频文件……')

    # 创建系统临时文件夹
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

    LOG = '正在捕获url……'
    myWindow.event_generate('<<log>>')
    # myWindow.log_signal.emit('正在捕获url……')
    url = script[0]  # 视频url

    # 已废弃
    # headers = {
    #     'authority': re.findall('https://(.*?)/', url)[-1],
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    #                   'Chrome/88.0.4324.182 Safari/537.36',
    #     'origin': 'https://www.bilibili.com',
    #     'referer': 'https://www.bilibili.com/',
    #     'Range': '',
    #            }
    # video_range = 'bytes=0-%d'
    # headers['Range'] = format(video_range % 1000)
    # sleep(0.2)
    #
    # LOG = '正在获取数据容量……'
    # myWindow.event_generate('<<log>>')
    # # myWindow.log_signal.emit('正在获取数据容量……')
    # try:
    #     response = requests.get(url=url, headers=headers, verify=False)
    # except Exception:
    #     STATUS_CODE = 404
    #     myWindow.event_generate('<<status>>')
    #     return
    # video_length = int(response.headers['Content-Range'].split('/')[-1]) - 1
    #
    # LOG = '正在修改二次请求参数……'
    # myWindow.event_generate('<<log>>')
    # # myWindow.log_signal.emit('正在修改二次请求参数……')
    # headers['Range'] = format(video_range % video_length)

    LOG = '正在写入视频数据……'
    myWindow.event_generate('<<log>>')
    # myWindow.log_signal.emit('正在写入数据……')
    try:
        response = requests.get(url=url, headers=video_headers, verify=False)
    except Exception:
        STATUS_CODE = 404
        myWindow.event_generate('<<status>>')
        return
    with open(t_path + '/bilibili.mp4', 'wb') as fp:
        fp.write(response.content)

    LOG = '视频文件下载完成!'
    myWindow.event_generate('<<log>>')
    # myWindow.log_signal.emit('视频文件下载完成!')
    PER = "16.87 %"
    myWindow.event_generate("<<per>>")

    # 下载音频
    LOG = '开始下载音频文件……'
    myWindow.event_generate('<<log>>')
    # myWindow.log_signal.emit('开始下载音频文件……')

    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    #                   'Chrome/88.0.4324.182 Safari/537.36',
    #     'origin': 'https://www.bilibili.com',
    #     'referer': 'https://www.bilibili.com/',
    #     'Range': '',
    # }
    # audio_range = 'bytes=0-%d'
    # headers['Range'] = format(audio_range % 1000)

    LOG = '正在捕获url……'
    myWindow.event_generate('<<log>>')
    # myWindow.log_signal.emit('正在捕获url……')
    url = script[-1]

    # 已废弃
    # try:
    #     response = requests.get(url=url, headers=headers, verify=False)
    # except Exception:
    #     STATUS_CODE = 404
    #     myWindow.event_generate('<<status>>')
    #     return
    #
    # LOG = '正在获取数据容量……'
    # myWindow.event_generate('<<log>>')
    # # myWindow.log_signal.emit('正在获取数据容量……')
    # audio_length = int(response.headers['Content-Range'].split('/')[-1]) - 1
    #
    # LOG = '正在修改二次请求参数……'
    # myWindow.event_generate('<<log>>')
    # # myWindow.log_signal.emit('正在修改二次请求参数……')
    # headers['Range'] = format(audio_range % audio_length)

    LOG = '正在写入数据……'
    myWindow.event_generate('<<log>>')
    # myWindow.log_signal.emit('正在写入数据……')

    try:
        response = requests.get(url=url, headers=video_headers, verify=False)
    except Exception:
        STATUS_CODE = 404
        myWindow.event_generate('<<status>>')
        return
    with open(t_path + '/bilibili.mp3', 'wb') as fp:
        fp.write(response.content)

    LOG = '音频文件下载完成!'
    myWindow.event_generate('<<log>>')
    PER = "19.01 %"
    myWindow.event_generate("<<per>>")
    # myWindow.log_signal.emit('音频文件下载完成!')

    # 音视频混流
    LOG = '开始进行数据混流……'
    myWindow.event_generate('<<log>>')
    # myWindow.log_signal.emit('开始进行数据混流……')
    LOG = '正在进行数据混流……(请耐心等待)'
    myWindow.event_generate('<<log>>')
    # myWindow.log_signal.emit('正在进行数据混流……(请耐心等待)')
    cmd_s = "./dev/ffmpeg.exe -i " + t_path + '/bilibili.mp4 ' + "-i " + t_path + '/bilibili.mp3 ' + "-y " + path + '/' + filename + '.mp4'
    st = subprocess.STARTUPINFO()
    st.dwFlags = subprocess.STARTF_USESHOWWINDOW
    st.wShowWindow = subprocess.SW_HIDE
    pop = subprocess.Popen(cmd_s, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', startupinfo=st)
    # video = moviepy.editor.VideoFileClip(t_path + '/bilibili.mp4')
    # audio = moviepy.editor.AudioFileClip(t_path + '/bilibili.mp3')
    # video = video.set_audio(audio)
    # video.write_videofile(path + '/' + filename + '.mp4', verbose=False, logger=None)

    all_t = 0
    per = 20.00
    PER = str(per) + " %"
    myWindow.event_generate("<<per>>")
    while True:
        status = pop.poll()
        if status is not None:
            flag = status
            break
        line = pop.stderr.readline().strip()
        if line:
            pat = re.compile('(?<=Duration:\s).*?(?=,)')
            re_line = pat.findall(line)
            if re_line:
                sum_t = handle_time(re_line[0])
                all_t = sum_t
            # re_line = re.search('(?<=time=).*?(?=\s)', line)
            pat = re.compile('(?<=time=).*?(?=\s)')
            re_line = pat.findall(line)
            if re_line:
                sum_t = handle_time(re_line[0])
                per = round(20 + round((sum_t/all_t) * 100, 2) * 0.8, 2)
                PER = str(per) + ' %'
                myWindow.event_generate("<<per>>")
    per = 100.0
    PER = str(per) + ' %'
    myWindow.event_generate("<<per>>")
    pop.stderr.close()
    if flag == 0:
        LOG = '数据混流完成！'
        myWindow.event_generate("<<log>>")
        # myWindow.log_signal.emit('数据混流完成！')
    else:
        STATUS_CODE = 500
        myWindow.event_generate('<<status>>')
        return
        # 删除中间音视频工程文件(已优化)
    # os.remove('./工作环境/bilibili.mp3')
    # os.remove('./工作环境/bilibili.mp4')
    # os.rmdir('./工作环境')  # 删除目录
    t_dir.cleanup()
    LOG = '视频下载成功!'
    myWindow.event_generate("<<log>>")
    # myWindow.log_signal.emit('视频下载成功!')
    STATUS_CODE = 200
    myWindow.event_generate("<<status>>")


if __name__ == '__main__':
    pass
