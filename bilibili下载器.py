from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
from PyQt5.QtGui import QIcon
import ui
from threading import Thread
import bilibili
import PyQt5.sip


class Jiemian:
    def __init__(self):
        self.Mainwindow = QMainWindow()
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self.Mainwindow)
        self.Mainwindow.setWindowIcon(QIcon('./icon/bilibili.png'))
        self.ui.pushButton.clicked.connect(self.download_btn)
        self.ui.pushButton_2.clicked.connect(self.reset_all_btn)
        self.ui.pushButton_4.clicked.connect(self.reset_filename_btn)

    def download_btn(self):
        self.ui.textBrowser.clear()
        url = self.ui.lineEdit.text()
        filename = self.ui.lineEdit_2.text()
        if url == '':
            QMessageBox.about(self.Mainwindow, '警告', '请输入视频URL！')
        elif filename == '':
            QMessageBox.about(self.Mainwindow, '警告', '请输入视频文件名！')
        else:
            thread = Thread(target=self.thread_start, args=(url, filename))
            thread.start()

    def thread_start(self, url, filename):
        bilibili.get_video(self, url, filename)

    def reset_all_btn(self):
        self.ui.textBrowser.clear()
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()

    def reset_filename_btn(self):
        self.ui.lineEdit_2.clear()


app = QApplication([])
jiemian = Jiemian()
jiemian.Mainwindow.show()
sys.exit(app.exec_())
