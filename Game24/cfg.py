'''配置文件'''
import os


'''游戏素材路径'''
BGMPATH = os.path.join(os.getcwd(), 'resources/music/bgm.mp3')
FONTPATH = os.path.join(os.getcwd(), 'resources/font/Gabriola.ttf')
'''屏幕大小'''
SCREENSIZE = (800, 500)
'''FPS'''
FPS = 5
'''一些常量'''
BLOCK_SIZE = 20
BLACK = (0, 0, 0)
GAME_MATRIX_SIZE = (int(SCREENSIZE[0]/BLOCK_SIZE), int(SCREENSIZE[1]/BLOCK_SIZE))