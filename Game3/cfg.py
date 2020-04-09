'''配置文件'''
import os


'''屏幕大小'''
SCREENSIZE = (640, 640)
'''图片素材根目录'''
PICTURE_ROOT_DIR = os.path.join(os.getcwd(), 'resources/pictures')
'''字体路径'''
FONTPATH = os.path.join(os.getcwd(), 'resources/font/FZSTK.TTF')
'''定义一些颜色'''
BACKGROUNDCOLOR = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
'''FPS'''
FPS = 40
'''随机打乱拼图次数'''
NUMRANDOM = 100