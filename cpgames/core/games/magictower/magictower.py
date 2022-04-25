'''
Function:
    魔塔小游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import pygame
from ..base import PygameBaseGame
from .modules import StartGameInterface, GameLevels


'''配置类'''
class Config():
    # 根目录
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # 屏幕大小
    BLOCKSIZE = 54
    SCREENBLOCKSIZE = (18, 13)
    SCREENSIZE = (BLOCKSIZE * SCREENBLOCKSIZE[0], BLOCKSIZE * SCREENBLOCKSIZE[1])
    # 标题
    TITLE = '魔塔 —— Charles的皮卡丘'
    # FPS
    FPS = 30
    # 字体路径
    FONT_PATHS_NOPRELOAD_DICT = {
        'font_cn': os.path.join(rootdir, 'resources/fonts/font_cn.ttf'),
        'font_en': os.path.join(rootdir, 'resources/fonts/font_en.ttf')
    }
    # 游戏地图路径
    MAPPATHS = [
        os.path.join(os.path.split(os.path.abspath(__file__))[0], f'resources/levels/{idx}.lvl') for idx in range(len(os.listdir(os.path.join(rootdir, f'resources/levels/'))))
    ]
    # 游戏图片路径
    IMAGE_PATHS_DICT = {
        'battlebg': os.path.join(rootdir, f'resources/images/battlebg.png'),
        'blankbg': os.path.join(rootdir, f'resources/images/blankbg.png'),
        'gamebg': os.path.join(rootdir, f'resources/images/gamebg.png'),
        'hero': {},
        'mapelements': {},
    }
    for filename in os.listdir(os.path.join(rootdir, 'resources/images/map0/')):
        IMAGE_PATHS_DICT['mapelements'][filename.split('.')[0]] = [
            os.path.join(rootdir, f'resources/images/map0/{filename}'),
            os.path.join(rootdir, f'resources/images/map1/{filename}'),
        ]
    for filename in os.listdir(os.path.join(rootdir, 'resources/images/player/')):
        IMAGE_PATHS_DICT['hero'][filename.split('.')[0]] = os.path.join(rootdir, f'resources/images/player/{filename}')


'''魔塔小游戏'''
class MagicTowerGame(PygameBaseGame):
    game_type = 'magictower'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(MagicTowerGame, self).__init__(config=self.cfg, **kwargs)
    '''运行游戏'''
    def run(self):
        # 开始界面
        sg_interface = StartGameInterface(self.cfg)
        sg_interface.run(self.screen)
        # 游戏进行中界面
        game_client = GameLevels(self.cfg, self.resource_loader)
        game_client.run(self.screen)