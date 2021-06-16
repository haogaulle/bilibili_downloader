import ui
import sys
import ctypes
import bilibili
from threading import Thread
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QFileDialog
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox


class Jiemian(QObject):
    wrong_signal = pyqtSignal()
    succ_signal = pyqtSignal()
    log_signal = pyqtSignal(str)

    def __init__(self):
        QObject.__init__(self)
        self.Mainwindow = QMainWindow()
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self.Mainwindow)
        self.ui.lineEdit.setPlaceholderText("请输入视频网址")
        self.ui.lineEdit_2.setPlaceholderText("请输入视频名称")
        #  self.Mainwindow.setWindowIcon(QIcon('./icon/bilibili.png'))

        self.ui.pushButton.clicked.connect(self.download_btn)
        self.ui.pushButton_2.clicked.connect(self.reset_all_btn)
        self.ui.pushButton_4.clicked.connect(self.reset_filename_btn)
        self.ui.pushButton_3.clicked.connect(self.get_directory)

        self.wrong_signal.connect(self.show_wrong_info)
        self.succ_signal.connect(self.show_succ_info)
        self.log_signal.connect(self.show_log)

    def download_btn(self):
        self.ui.textBrowser.clear()
        url = self.ui.lineEdit.text()
        filename = self.ui.lineEdit_2.text()
        path = self.ui.lineEdit_3.text()
        if url.strip() == '':
            QMessageBox.about(self.Mainwindow, '警告', '请输入视频URL！')
        elif filename.strip() == '':
            QMessageBox.about(self.Mainwindow, '警告', '请输入视频文件名！')
        elif path.strip() == '':
            QMessageBox.about(self.Mainwindow, '警告', '请选择视频保存位置！')
        else:
            thread = Thread(target=bilibili.get_video, args=(self, url, filename, path))
            thread.start()

    def reset_all_btn(self):
        self.ui.textBrowser.clear()
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()

    def reset_filename_btn(self):
        self.ui.lineEdit_2.clear()

    def show_wrong_info(self):
        QMessageBox.about(self.Mainwindow, '提示', '连接失败，请重试！')

    def show_succ_info(self):
        QMessageBox.about(self.Mainwindow, '提示', self.ui.lineEdit_2.text()+' 下载成功！')

    def get_directory(self):
        path = QFileDialog.getExistingDirectory(self.Mainwindow, 'nome', './')
        self.ui.lineEdit_3.setText(path)

    def show_log(self, text):
        self.ui.textBrowser.append(text)


if __name__ == '__main__':
    #  屏蔽控制台(已优化)
    """
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
        ctypes.windll.kernel32.CloseHandle(whnd)
    """
    app = QApplication([])
    jiemian = Jiemian()
    jiemian.Mainwindow.show()
    sys.exit(app.exec_())
