''
Function:
	연속적인 미니게임 구성 파일
Author:
	Charles
WeChat 공개번호:
	 Charles의 피카츄
'''
import os


'''몇개의 슈퍼 매개변수 정의'''
WIDTH = 600
HEIGHT = 600
NUMGRID = 8
GRIDSIZE = 64
XMARGIN = (WIDTH - GRIDSIZE * NUMGRID) // 2
YMARGIN = (HEIGHT - GRIDSIZE * NUMGRID) // 2
ROOTDIR = os.getcwd()
FPS = 30