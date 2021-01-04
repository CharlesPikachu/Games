'''配置文件'''
import os


'''屏幕大小'''
SCREENSIZE = (600, 600)
'''游戏元素尺寸'''
NUMGRID = 8
GRIDSIZE = 64
XMARGIN = (SCREENSIZE[0] - GRIDSIZE * NUMGRID) // 2
YMARGIN = (SCREENSIZE[1] - GRIDSIZE * NUMGRID) // 2
'''根目录'''
ROOTDIR = os.getcwd()
'''FPS'''
FPS = 30