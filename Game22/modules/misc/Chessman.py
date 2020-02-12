'''
Function:
    定义棋子类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from modules.misc.utils import *


'''棋子类'''
class Chessman(QLabel):
    def __init__(self, imagepath, parent=None, **kwargs):
        super(Chessman, self).__init__(parent)
        self.color = imagepath.split('.')[-2][-5:]
        self.image = QPixmap(imagepath)
        self.setFixedSize(self.image.size())
        self.setPixmap(self.image)
    def move(self, point):
        x, y = Pixel2Chesspos(point)
        x = 30 * x + 50 - self.image.width() / 2
        y = 30 * y + 50 - self.image.height() / 2
        super().move(x, y)