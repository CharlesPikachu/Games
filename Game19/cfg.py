'''配置文件'''
import os


'''屏幕大小'''
SCREENSIZE = (640, 480)
'''块大小'''
BLOCKSIZE = 30
'''FPS'''
FPS = 30
'''游戏地图路径'''
GAMEMAPPATHS = [os.path.join(os.getcwd(), path) for path in \
    ['resources/maps/1.map', 'resources/maps/2.map']]
'''墙路径'''
WALLPATHS = [os.path.join(os.getcwd(), path) for path in \
    ['resources/images/misc/wall0.png', 'resources/images/misc/wall1.png', 'resources/images/misc/wall2.png']]
'''英雄路径'''
HERODKPATHS = [os.path.join(os.getcwd(), path) for path in \
    ['resources/images/dk/left.png', 'resources/images/dk/right.png', 'resources/images/dk/up.png', 'resources/images/dk/down.png']]
HEROZELDAPATHS = [os.path.join(os.getcwd(), path) for path in \
    ['resources/images/zelda/left.png', 'resources/images/zelda/right.png', 'resources/images/zelda/up.png', 'resources/images/zelda/down.png']]
HEROBATMANPATHS = [os.path.join(os.getcwd(), path) for path in \
    ['resources/images/batman/left.png', 'resources/images/batman/right.png', 'resources/images/batman/up.png', 'resources/images/batman/down.png']]
'''水果路径'''
FRUITPATHS = [os.path.join(os.getcwd(), path) for path in \
    ['resources/images/misc/banana.png', 'resources/images/misc/cherry.png']]
'''背景路径'''
BACKGROUNDPATHS = [os.path.join(os.getcwd(), path) for path in \
    ['resources/images/misc/bg0.png', 'resources/images/misc/bg1.png', 'resources/images/misc/bg2.png']]
'''爆炸和发射路径'''
BOMBPATH = os.path.join(os.getcwd(), 'resources/images/misc/bomb.png')
FIREPATH = os.path.join(os.getcwd(), 'resources/images/misc/fire.png')
'''背景音乐'''
BGMPATH = os.path.join(os.getcwd(), 'resources/audio/bgm.mp3')
'''一些颜色'''
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)