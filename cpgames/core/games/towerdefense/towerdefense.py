'''
Function:
    塔防游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import pygame
from ..base import PygameBaseGame
from .modules import StartInterface, EndInterface, GamingInterface, PauseInterface, ChoiceInterface


'''配置类'''
class Config():
    # 根目录
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # FPS
    FPS = 60
    # 屏幕大小
    SCREENSIZE = (800, 600)
    # 标题
    TITLE = '塔防游戏 —— Charles的皮卡丘'
    # 游戏图片路径
    IMAGE_PATHS_DICT = {
        'choice': {
            'load_game': os.path.join(rootdir, 'resources/images/choice/load_game.png'),
            'map1': os.path.join(rootdir, 'resources/images/choice/map1.png'),
            'map1_black': os.path.join(rootdir, 'resources/images/choice/map1_black.png'),
            'map1_red': os.path.join(rootdir, 'resources/images/choice/map1_red.png'),
            'map2': os.path.join(rootdir, 'resources/images/choice/map2.png'),
            'map2_black': os.path.join(rootdir, 'resources/images/choice/map2_black.png'),
            'map2_red': os.path.join(rootdir, 'resources/images/choice/map2_red.png'),
            'map3': os.path.join(rootdir, 'resources/images/choice/map3.png'),
            'map3_black': os.path.join(rootdir, 'resources/images/choice/map3_black.png'),
            'map3_red': os.path.join(rootdir, 'resources/images/choice/map3_red.png'),
        },
        'end': {
            'gameover': os.path.join(rootdir, 'resources/images/end/gameover.png'),
            'continue_red': os.path.join(rootdir, 'resources/images/end/continue_red.png'),
            'continue_black': os.path.join(rootdir, 'resources/images/end/continue_black.png'),
        },
        'game': {
            'arrow1': os.path.join(rootdir, 'resources/images/game/arrow1.png'), 
            'arrow2': os.path.join(rootdir, 'resources/images/game/arrow2.png'), 
            'arrow3': os.path.join(rootdir, 'resources/images/game/arrow3.png'), 
            'basic_tower': os.path.join(rootdir, 'resources/images/game/basic_tower.png'), 
            'boulder': os.path.join(rootdir, 'resources/images/game/boulder.png'), 
            'bush': os.path.join(rootdir, 'resources/images/game/bush.png'), 
            'cave': os.path.join(rootdir, 'resources/images/game/cave.png'), 
            'dirt': os.path.join(rootdir, 'resources/images/game/dirt.png'), 
            'enemy_blue': os.path.join(rootdir, 'resources/images/game/enemy_blue.png'), 
            'enemy_pink': os.path.join(rootdir, 'resources/images/game/enemy_pink.png'), 
            'enemy_red': os.path.join(rootdir, 'resources/images/game/enemy_red.png'), 
            'enemy_yellow': os.path.join(rootdir, 'resources/images/game/enemy_yellow.png'), 
            'godark': os.path.join(rootdir, 'resources/images/game/godark.png'), 
            'golight': os.path.join(rootdir, 'resources/images/game/golight.png'), 
            'grass': os.path.join(rootdir, 'resources/images/game/grass.png'), 
            'healthfont': os.path.join(rootdir, 'resources/images/game/healthfont.png'), 
            'heavy_tower': os.path.join(rootdir, 'resources/images/game/heavy_tower.png'), 
            'med_tower': os.path.join(rootdir, 'resources/images/game/med_tower.png'), 
            'nexus': os.path.join(rootdir, 'resources/images/game/nexus.png'), 
            'othergrass': os.path.join(rootdir, 'resources/images/game/othergrass.png'), 
            'path': os.path.join(rootdir, 'resources/images/game/path.png'), 
            'rock': os.path.join(rootdir, 'resources/images/game/rock.png'), 
            'tiles': os.path.join(rootdir, 'resources/images/game/tiles.png'), 
            'unitfont': os.path.join(rootdir, 'resources/images/game/unitfont.png'), 
            'water': os.path.join(rootdir, 'resources/images/game/water.png'), 
            'x': os.path.join(rootdir, 'resources/images/game/x.png'), 
        },
        'pause': {
            'gamepaused': os.path.join(rootdir, 'resources/images/pause/gamepaused.png'), 
            'resume_black': os.path.join(rootdir, 'resources/images/pause/resume_black.png'), 
            'resume_red': os.path.join(rootdir, 'resources/images/pause/resume_red.png'), 
        },
        'start': {
            'play_black': os.path.join(rootdir, 'resources/images/start/play_black.png'), 
            'play_red': os.path.join(rootdir, 'resources/images/start/play_red.png'), 
            'quit_black': os.path.join(rootdir, 'resources/images/start/quit_black.png'), 
            'quit_red': os.path.join(rootdir, 'resources/images/start/quit_red.png'), 
            'start_interface': os.path.join(rootdir, 'resources/images/start/start_interface.png'), 
        },
    }
    # 背景音乐路径
    BGM_PATH = os.path.join(rootdir.replace('towerdefense', 'base'), 'resources/audios/liuyuedeyu.mp3')
    # 不同难度的settings
    DIFFICULTY_PATHS_DICT = {
        'easy': os.path.join(rootdir, 'resources/difficulties/easy.json'),
        'hard': os.path.join(rootdir, 'resources/difficulties/hard.json'),
        'medium': os.path.join(rootdir, 'resources/difficulties/medium.json'),
    }
    # 地图路径
    MAP_PATHS_DICT = {
        '1': os.path.join(rootdir, 'resources/maps/1.map'),
        '2': os.path.join(rootdir, 'resources/maps/2.map'),
        '3': os.path.join(rootdir, 'resources/maps/3.map'),
    }
    # 字体路径
    FONT_PATHS_DICT = {
        'm04': {'name': os.path.join(rootdir, 'resources/fonts/m04.ttf'), 'size': 42},
        'Calibri_s': {'name': os.path.join(rootdir, 'resources/fonts/Calibri.ttf'), 'size': 14},
        'Calibri_l': {'name': os.path.join(rootdir, 'resources/fonts/Calibri.ttf'), 'size': 20},
    }
    

'''塔防游戏'''
class TowerDefenseGame(PygameBaseGame):
    game_type = 'towerdefense'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(TowerDefenseGame, self).__init__(config=self.cfg, **kwargs)
    '''运行游戏'''
    def run(self):
        # 初始化
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
        # 播放背景音乐
        resource_loader.playbgm()
        # 调用游戏开始界面
        start_interface = StartInterface(cfg, resource_loader)
        is_play = start_interface.update(screen)
        if not is_play: return
        # 调用游戏界面
        while True:
            choice_interface = ChoiceInterface(cfg, resource_loader)
            map_choice, difficulty_choice = choice_interface.update(screen)
            game_interface = GamingInterface(cfg, resource_loader)
            game_interface.start(screen, map_path=cfg.MAP_PATHS_DICT[str(map_choice)], difficulty_path=cfg.DIFFICULTY_PATHS_DICT[str(difficulty_choice)])
            end_interface = EndInterface(cfg, resource_loader)
            end_interface.update(screen)