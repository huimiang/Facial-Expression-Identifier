# UI文件
import sys

import matplotlib
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from matplotlib.figure import Figure
import os

matplotlib.use("Qt5Agg")
# 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import mainui
from classes.Evaluator import *
from definitions import *


class PlotCanvas(FigureCanvas):
    def __init__(self):
        fig = Figure( dpi=100)
        # 设置像素
        FigureCanvas.__init__(self, fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 设置大小
        FigureCanvas.updateGeometry(self)
        # 更新位置
        self._ax = self.figure.add_subplot(111)
        # 创建一个图表

    def change(self, res, flags):
        """
        生成函数图像
        :param res: 神经网络输出结果
        :param flags: 对哪些帧是异常进行标记的标记列表
        :return:
        """
        length = len(res)
        self._ax.cla()
        #将曲线图和坐标清空
        self._ax.set_title('Emotion Graph')
        # 标题
        self._ax.set_xlabel('Time')
        self._ax.set_ylabel('Probability')
        # 坐标轴名称
        x = [i * INTERVAL for i in range(length)]
        # 时间轴
        y = []
        for i in range(OUTPUT_NUM):
            y.append([res[j][i] for j in range(length)])
        # 情绪值
        xx = []
        # 调整后的时间轴
        yy = []
        # 调整后的情绪值
        for i in range(length):
            # 只保留正常的，即flag值为True的帧
            if flags[i]:
                xx.append(x[i])
        for i in range(OUTPUT_NUM):
            # 只保留正常的，即flag值为True的帧
            tmp = []
            for j in range(length):
                if flags[j]:
                    tmp.append(res[j][i])
            yy.append(tmp)

        colors = ['-r', '-b', 'g', '-c', '-m', '-y']
        # 指定各条曲线的颜色

        for i in range(OUTPUT_NUM):
            # 绑定函数关系
            self._ax.plot(xx, yy[i], colors[i], label=EXPRESSIONS[i])
        self._ax.legend(loc=1, ncol=1)
        #右上角标签显示
        self.draw()
        #绘图


class Main(QMainWindow, mainui.Ui_MainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.evaluator = Evaluator()
        self.picture_v.setVisible(False)
        self.seekv.setVisible(False)
        self.canvas = PlotCanvas()
        # 创建matplot对象
        layout = QHBoxLayout(self.picture_v)
        # 选定frame组件
        layout.setContentsMargins(0, 0, 0, 0)
        # 设置边距
        layout.addWidget(self.canvas)
        # 添加matplot对象到QT组件内，用于将matplotlib和qt绑定
        self.table_init()

    def table_init(self):
        self.picture_p.setColumnCount(OUTPUT_NUM)
        # 设置行数
        self.picture_p.setRowCount(2)
        # 设置列数
        for i in range(OUTPUT_NUM):
            self.picture_p.setItem(0, i, QTableWidgetItem(EXPRESSIONS[i]))

        self.picture_p.verticalHeader().setVisible(False)
        # 隐藏垂直表头
        self.picture_p.horizontalHeader().setVisible(False)
        # 隐藏水平表头
        self.picture_p.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 水平适应
        self.picture_p.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 垂直适应
    def video_mode(self):
        # 进入视频模式，该函数用以对UI的样式与可见性进行调整
        self.textEdit.clear()
        self.imageshow.setVisible(False)
        self.afterimageshow.setVisible(False)
        self.picture_v.setVisible(True)
        self.picture_p.setVisible(False)
        self.seekv.setVisible(True)
        self.seekp.setVisible(False)
        self.generate_v.setVisible(True)
        self.generate_p.setVisible(False)
        self.videoinput.setStyleSheet('QPushButton{font: 30pt "Microsoft YaHei UI";'
                                      'background-color:rgb(209, 209, 211); '
                                      'border-radius:10px;'
                                      'border-color:rgba(255,255,255,30);'
                                      'font:bold 20px;'
                                      'color:rgb(0, 0, 0); }')
        self.photoinput.setStyleSheet('QPushButton{font: 30pt "Microsoft YaHei UI";'
                                      'background-color:rgb(245, 245, 247);'
                                      'border-radius:10px;'
                                      'border-color:rgba(255,255,255,30);'
                                      'font:bold 20px;'
                                      'color:rgb(119, 119, 119);  }'

                                      'QPushButton:hover{background-color:rgb(209, 209, 211);'
                                      'border-color:rgba(255,255,255,30);'
                                      'border-style:inset;'
                                      'color:rgb(0, 0, 0); } ')

    def image_mode(self):
        # 进入图像模式，该函数用以对UI的样式与可见性进行调整
        self.textEdit.clear()
        self.picture_p.setVisible(True)
        self.picture_v.setVisible(False)
        self.seekp.setVisible(True)
        self.seekv.setVisible(False)
        self.generate_p.setVisible(True)
        self.generate_v.setVisible(False)
        self.photoinput.setStyleSheet('QPushButton{font: 30pt "Microsoft YaHei UI";'
                                      'background-color:rgb(209, 209, 211); '
                                      'border-radius:10px;'
                                      'border-color:rgba(255,255,255,30);'
                                      'font:bold 20px;'
                                      'color:rgb(0, 0, 0); }')
        self.videoinput.setStyleSheet('QPushButton{font: 30pt "Microsoft YaHei UI";'
                                      'background-color:rgb(245, 245, 247);'
                                      'border-radius:10px;'
                                      'border-color:rgba(255,255,255,30);'
                                      'font:bold 20px;'
                                      'color:rgb(119, 119, 119);  }'

                                      'QPushButton:hover{background-color:rgb(209, 209, 211);'
                                      'border-color:rgba(255,255,255,30);'
                                      'border-style:inset;'
                                      'color:rgb(0, 0, 0); } ')

    def get_video(self):
        # 获取上传视频
        file_name, file_type = QFileDialog.getOpenFileName(self, "选取视频", "./",
                                                           "Video Files (*.mp4 *.avi *.wmv "
                                                           "*.rmvb *.3gp *.flv *.rm)")
        if file_name == '' and self.textEdit.toPlainText() == '':
            # 未选择文件
            QMessageBox.warning(self, 'Warning', '请选取文件')
            return
        elif os.path.getsize(file_name) / (1024 ** 2) > 500:
            # 文件超过500MB
            QMessageBox.warning(self, 'Warning', '视频文件过大，请重新选择')
            return
        self.textEdit.setText(str(file_name))

    def get_image(self):
        # 获取上传图片
        file_name, file_type = QFileDialog.getOpenFileName(self, "选取图片", "./",
                                                           "Image Files (*.png *.jpg *.tiff *.bmp *.jpeg)")
        if file_name == '' and self.textEdit.toPlainText() == '':
            # 未选择文件
            QMessageBox.warning(self, 'Warning', '请选取文件')
            return
        self.textEdit.setText(str(file_name))
        self.imageshow.setVisible(True)
        self.imageshow.setPixmap(QPixmap(file_name))
        self.imageshow.setScaledContents(True)

    def generate_view_of_videos(self):
        # 生成视频情绪曲线图表
        res, flags = self.evaluator.evaluate_video(self.textEdit.toPlainText())
        self.canvas.change(res, flags)

    def generate_view_of_images(self):
        # 生成图像情绪表格
        path = self.textEdit.toPlainText()
        img_dir, res = self.evaluator.evaluate_one(path)
        if img_dir == 'No Face Found':
            # 没有找到脸
            QMessageBox.warning(self, 'Warning', '没有找到人脸！请再次确认', QMessageBox.Cancel)
            return
        elif img_dir == 'Multiple Faces Found':
            # 多个脸
            QMessageBox.warning(self, 'Warning', '找到多个人脸！请再次确认', QMessageBox.Cancel)
            return
        self.afterimageshow.setVisible(True)
        self.afterimageshow.setPixmap(QPixmap(img_dir))
        self.afterimageshow.setScaledContents(True)

        for i in range(OUTPUT_NUM):
            # 生成图标项目
            self.picture_p.setItem(1, i, QTableWidgetItem(str(round(res[i] * 100, 3)) + '%'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
