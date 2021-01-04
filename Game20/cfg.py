'''配置文件'''
import os


'''屏幕大小'''
SCREENSIZE = (800, 625)
'''游戏素材'''
BGMPATH = os.path.join(os.getcwd(), 'resources/audios/bgm.mp3')
HEROPICPATH = os.path.join(os.getcwd(), 'resources/images/hero.png')
'''FPS'''
FPS = 20
'''块大小'''
BLOCKSIZE = 15
MAZESIZE = (35, 50) # num_rows * num_cols
BORDERSIZE = (25, 50) # 25 * 2 + 50 * 15 = 800, 50 * 2 + 35 * 15 = 625