'''
Function:
    经典坦克大战小游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import pygame
from ..base import PygameBaseGame
from .modules import SwitchLevelIterface, GameEndIterface, GameStartInterface, GameLevel


'''配置类'''
class Config():
    # 根目录
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # FPS
    FPS = 60
    # 屏幕大小
    SCREENSIZE = (630, 630)
    # 标题
    TITLE = '坦克大战 —— Charles的皮卡丘'
    # 屏幕超参数
    BORDER_LEN = 3
    GRID_SIZE = 24
    PANEL_WIDTH = 150
    # 关卡文件
    LEVELFILEDIR = os.path.join(rootdir, 'modules/levels')
    # 字体路径
    FONT_PATHS_DICT = {
        'start': {'name': os.path.join(rootdir.replace('tankwar', 'base'), 'resources/fonts/Gabriola.ttf'), 'size': SCREENSIZE[0] // 12},
        'switch': {'name': os.path.join(rootdir.replace('tankwar', 'base'), 'resources/fonts/Gabriola.ttf'), 'size': SCREENSIZE[0] // 20},
        'end': {'name': os.path.join(rootdir.replace('tankwar', 'base'), 'resources/fonts/Gabriola.ttf'), 'size': SCREENSIZE[0] // 12},
        'gaming': {'name': os.path.join(rootdir.replace('tankwar', 'base'), 'resources/fonts/Gabriola.ttf'), 'size': SCREENSIZE[0] // 30},
    }
    # 游戏声音路径
    SOUND_PATHS_DICT = {
        'add': os.path.join(rootdir, 'resources/audios/add.wav'),
        'bang': os.path.join(rootdir, 'resources/audios/bang.wav'),
        'blast': os.path.join(rootdir, 'resources/audios/blast.wav'),
        'fire': os.path.join(rootdir, 'resources/audios/fire.wav'),
        'Gunfire': os.path.join(rootdir, 'resources/audios/Gunfire.wav'),
        'hit': os.path.join(rootdir, 'resources/audios/hit.wav'),
        'start': os.path.join(rootdir, 'resources/audios/start.wav'),
    }
    # 游戏图片路径
    IMAGE_PATHS_DICT = {
        'bullet': {
            'up': os.path.join(rootdir, 'resources/images/bullet/bullet_up.png'),
            'down': os.path.join(rootdir, 'resources/images/bullet/bullet_down.png'),
            'left': os.path.join(rootdir, 'resources/images/bullet/bullet_left.png'),
            'right': os.path.join(rootdir, 'resources/images/bullet/bullet_right.png'),
        },
        'enemy': {
            '1': [
                os.path.join(rootdir, 'resources/images/enemyTank/enemy_1_0.png'), os.path.join(rootdir, 'resources/images/enemyTank/enemy_1_1.png'),
                os.path.join(rootdir, 'resources/images/enemyTank/enemy_1_2.png'), os.path.join(rootdir, 'resources/images/enemyTank/enemy_1_3.png'),
            ],
            '2': [
                os.path.join(rootdir, 'resources/images/enemyTank/enemy_2_0.png'), os.path.join(rootdir, 'resources/images/enemyTank/enemy_2_1.png'),
                os.path.join(rootdir, 'resources/images/enemyTank/enemy_2_2.png'), os.path.join(rootdir, 'resources/images/enemyTank/enemy_2_3.png'),
            ],
            '3': [
                os.path.join(rootdir, 'resources/images/enemyTank/enemy_3_0.png'), os.path.join(rootdir, 'resources/images/enemyTank/enemy_3_1.png'),
                os.path.join(rootdir, 'resources/images/enemyTank/enemy_3_2.png'), os.path.join(rootdir, 'resources/images/enemyTank/enemy_3_3.png'),
            ],
            '4': [
                os.path.join(rootdir, 'resources/images/enemyTank/enemy_4_0.png'), os.path.join(rootdir, 'resources/images/enemyTank/enemy_4_1.png'),
                os.path.join(rootdir, 'resources/images/enemyTank/enemy_4_2.png'), os.path.join(rootdir, 'resources/images/enemyTank/enemy_4_3.png'),
            ],
        },
        'player': {
            'player1': [
                os.path.join(rootdir, 'resources/images/playerTank/tank_T1_0.png'),
                os.path.join(rootdir, 'resources/images/playerTank/tank_T1_1.png'),
                os.path.join(rootdir, 'resources/images/playerTank/tank_T1_2.png')
            ],
            'player2': [
                os.path.join(rootdir, 'resources/images/playerTank/tank_T2_0.png'),
                os.path.join(rootdir, 'resources/images/playerTank/tank_T2_1.png'),
                os.path.join(rootdir, 'resources/images/playerTank/tank_T2_2.png')
            ]
        },
        'food': {
            'boom': os.path.join(rootdir, 'resources/images/food/food_boom.png'),
            'clock': os.path.join(rootdir, 'resources/images/food/food_clock.png'),
            'gun': os.path.join(rootdir, 'resources/images/food/food_gun.png'),
            'iron': os.path.join(rootdir, 'resources/images/food/food_iron.png'),
            'protect': os.path.join(rootdir, 'resources/images/food/food_protect.png'),
            'star': os.path.join(rootdir, 'resources/images/food/food_star.png'),
            'tank': os.path.join(rootdir, 'resources/images/food/food_tank.png')
        },
        'home': [os.path.join(rootdir, 'resources/images/home/home1.png'), os.path.join(rootdir, 'resources/images/home/home_destroyed.png')],
        'scene': {
            'brick': os.path.join(rootdir, 'resources/images/scene/brick.png'),
            'ice': os.path.join(rootdir, 'resources/images/scene/ice.png'),
            'iron': os.path.join(rootdir, 'resources/images/scene/iron.png'),
            'river1': os.path.join(rootdir, 'resources/images/scene/river1.png'),
            'river2': os.path.join(rootdir, 'resources/images/scene/river2.png'),
            'tree': os.path.join(rootdir, 'resources/images/scene/tree.png')
        },
        'others': {
            'appear': os.path.join(rootdir, 'resources/images/others/appear.png'),
            'background': os.path.join(rootdir, 'resources/images/others/background.png'),
            'boom_dynamic': os.path.join(rootdir, 'resources/images/others/boom_dynamic.png'),
            'boom_static': os.path.join(rootdir, 'resources/images/others/boom_static.png'),
            'gameover': os.path.join(rootdir, 'resources/images/others/gameover.png'),
            'logo': os.path.join(rootdir, 'resources/images/others/logo.png'),
            'mask': os.path.join(rootdir, 'resources/images/others/mask.png'),
            'protect': os.path.join(rootdir, 'resources/images/others/protect.png'),
            'tip': os.path.join(rootdir, 'resources/images/others/tip.png'),
            'gamebar': os.path.join(rootdir, 'resources/images/others/gamebar.png')
        },
    }


'''经典坦克大战小游戏'''
class TankWarGame(PygameBaseGame):
    game_type = 'tankwar'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(TankWarGame, self).__init__(config=self.cfg, **kwargs)
    '''运行游戏'''
    def run(self):
        is_quit_game = False
        while not is_quit_game:
            # 初始化
            screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
            # 开始界面
            is_dual_mode = GameStartInterface(screen, cfg, resource_loader)
            # 关卡数
            levelfilepaths = [os.path.join(cfg.LEVELFILEDIR, filename) for filename in sorted(os.listdir(cfg.LEVELFILEDIR))]
            # 主循环
            for idx, levelfilepath in enumerate(levelfilepaths):
                SwitchLevelIterface(screen, cfg, resource_loader, idx + 1)
                game_level = GameLevel(idx+1, levelfilepath, is_dual_mode, cfg, resource_loader)
                is_win = game_level.start(screen)
                if not is_win: break
            # 结束界面
            is_quit_game = GameEndIterface(screen, cfg, resource_loader, is_win)