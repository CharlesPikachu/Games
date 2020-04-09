'''配置文件'''
import os


'''FPS'''
FPS = 60
'''背景颜色'''
BG_COLOR = '#92877d'
'''屏幕大小'''
SCREENSIZE = (650, 370)
'''保存当前最高分的文件'''
MAX_SCORE_FILEPATH = 'score'
'''字体路径'''
FONTPATH = os.path.join(os.getcwd(), 'resources/font/Gabriola.ttf')
'''背景音乐路径'''
BGMPATH = os.path.join(os.getcwd(), 'resources/audio/bgm.mp3')
'''其他一些必要的常量'''
MARGIN_SIZE = 10
BLOCK_SIZE = 80
GAME_MATRIX_SIZE = (4, 4)