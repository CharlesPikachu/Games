'''
Function:
    其他工具函数
Author:
    Charles
公众号:
    Charles的皮卡丘
'''
from PyQt5.QtGui import *


'''给板块的一个Cell填色'''
def drawCell(painter, x, y, shape, grid_size):
    colors = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC, 0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]
    if shape == 0:
        return
    color = QColor(colors[shape])
    painter.fillRect(x + 1, y + 1, grid_size - 2, grid_size - 2, color)
    painter.setPen(color.lighter())
    painter.drawLine(x, y + grid_size - 1, x, y)
    painter.drawLine(x, y, x + grid_size - 1, y)
    painter.setPen(color.darker())
    painter.drawLine(x + 1, y + grid_size - 1, x + grid_size - 1, y + grid_size - 1)
    painter.drawLine(x + grid_size - 1, y + grid_size - 1, x + grid_size - 1, y + 1)