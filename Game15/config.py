'''
Function:
	连连看小游戏配置文件
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import os


'''定义一些超参'''
WIDTH = 600
HEIGHT = 600
NUMGRID = 8
GRIDSIZE = 64
XMARGIN = (WIDTH - GRIDSIZE * NUMGRID) // 2
YMARGIN = (HEIGHT - GRIDSIZE * NUMGRID) // 2
ROOTDIR = os.getcwd()
FPS = 30