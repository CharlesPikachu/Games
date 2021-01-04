'''配置文件'''
import os


'''游戏界面一些数值'''
SCREENWIDTH = 640
SCREENHEIGHT = 480
BRICKWIDTH = 10
BRICKHEIGHT = 10
PADDLEWIDTH = 60
PADDLEHEIGHT = 12
BALLRADIUS = 8
'''游戏素材路径'''
FONTPATH = os.path.join(os.getcwd(), 'resources/font/font.TTF')
HITSOUNDPATH = os.path.join(os.getcwd(), 'resources/audios/hit.wav')
BGMPATH = os.path.join(os.getcwd(), 'resources/audios/bgm.mp3')
LEVELROOTPATH = os.path.join(os.getcwd(), 'resources/levels')
LEVELPATHS = [os.path.join(LEVELROOTPATH, '%s.level' % str(i+1)) for i in range(len(os.listdir(LEVELROOTPATH)))]
'''一些颜色'''
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (212, 149, 174) 
PURPLE = (168, 152, 191)
YELLOW = (245, 237, 162)
BLUE  = (51, 170, 230)
AQUA = (182, 225, 225)