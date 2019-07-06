'''
Function:
	配置文件
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import os


SCREENWIDTH = 640
SCREENHEIGHT = 480
BRICKWIDTH = 10
BRICKHEIGHT = 10
PADDLEWIDTH = 60
PADDLEHEIGHT = 12
BALLRADIUS = 8
FONTPATH = os.path.join(os.getcwd(), 'resources/font/font.TTF')
HITSOUNDPATH = os.path.join(os.getcwd(), 'resources/audios/hit.wav')
BGMPATH = os.path.join(os.getcwd(), 'resources/audios/bgm.mp3')
LEVELROOTPATH = os.path.join(os.getcwd(), 'levels')
LEVELPATHS = [os.path.join(LEVELROOTPATH, '%s.level' % str(i+1)) for i in range(len(os.listdir(LEVELROOTPATH)))]
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (212, 149, 174) 
PURPLE = (168, 152, 191)
YELLOW = (245, 237, 162)
BLUE  = (51, 170, 230)
AQUA = (182, 225, 225)