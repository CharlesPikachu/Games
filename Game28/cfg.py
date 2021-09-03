'''配置文件'''
import os


'''屏幕大小'''
BLOCKSIZE = 54
SCREENBLOCKSIZE = (18, 13)
SCREENSIZE = (BLOCKSIZE * SCREENBLOCKSIZE[0], BLOCKSIZE * SCREENBLOCKSIZE[1])
'''FPS'''
FPS = 30
'''字体路径'''
FONTPATH_CN = os.path.join(os.getcwd(), 'resources/fonts/font_cn.TTF')
FONTPATH_EN = os.path.join(os.getcwd(), 'resources/fonts/font_en.TTF')
'''游戏地图路径'''
MAPPATHS = [os.path.join(os.getcwd(), f'resources/levels/{idx}.lvl') for idx in range(len(os.listdir(os.path.join(os.getcwd(), f'resources/levels/'))))]
'''游戏地图元素图片路径'''
MAPELEMENTSPATHS = {}
for filename in os.listdir(os.path.join(os.getcwd(), 'resources/images/map0/')):
    MAPELEMENTSPATHS[filename.split('.')[0]] = [
        os.path.join(os.getcwd(), f'resources/images/map0/{filename}'),
        os.path.join(os.getcwd(), f'resources/images/map1/{filename}'),
    ]
'''游戏背景图片'''
BACKGROUNDPATHS = {
    'battlebg': os.path.join(os.getcwd(), f'resources/images/battlebg.png'),
    'blankbg': os.path.join(os.getcwd(), f'resources/images/blankbg.png'),
    'gamebg': os.path.join(os.getcwd(), f'resources/images/gamebg.png'),
}
'''勇士图片路径'''
HEROPATHS = {}
for filename in os.listdir(os.path.join(os.getcwd(), 'resources/images/player/')):
    HEROPATHS[filename.split('.')[0]] = os.path.join(os.getcwd(), f'resources/images/player/{filename}')