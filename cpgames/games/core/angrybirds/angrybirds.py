'''
Function:
    愤怒的小鸟
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import pygame
from ...utils import QuitGame
from ..base import PygameBaseGame
from .modules import GameLevels, Pig, Bird, Block, Slingshot, Slab, Button, Label


'''配置类'''
class Config():
    # 根目录
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # FPS
    FPS = 60
    # 屏幕大小
    SCREENSIZE = (1800, 700)
    # 标题
    TITLE = '愤怒的小鸟 —— Charles的皮卡丘'
    # 一些颜色定义
    BACKGROUND_COLOR = (51, 51, 51)
    # 背景音乐路径
    BGM_PATH = os.path.join(rootdir, 'resources/audios/bgm.ogg')
    # 游戏图片路径
    IMAGE_PATHS_DICT = {
        'pig': [
            os.path.join(rootdir, 'resources/images/pig_1.png'),
            os.path.join(rootdir, 'resources/images/pig_2.png'),
            os.path.join(rootdir, 'resources/images/pig_damaged.png'),
        ],
        'bird': [
            os.path.join(rootdir, 'resources/images/bird.png'),
        ],
        'wall': [
            os.path.join(rootdir, 'resources/images/wall_horizontal.png'),
            os.path.join(rootdir, 'resources/images/wall_vertical.png'),
        ],
        'block': [
            os.path.join(rootdir, 'resources/images/block.png'),
            os.path.join(rootdir, 'resources/images/block_destroyed.png'),
        ]
    }
    # 字体路径
    FONT_PATHS_DICT_NOINIT = {
        'Comic_Kings': os.path.join(rootdir, 'resources/fonts/Comic_Kings.ttf'),
        'arfmoochikncheez': os.path.join(rootdir, 'resources/fonts/arfmoochikncheez.ttf'),
    }


'''愤怒的小鸟'''
class AngryBirdsGame(PygameBaseGame):
    game_type = 'angrybirds'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(AngryBirdsGame, self).__init__(config=self.cfg, **kwargs)
    '''运行游戏'''
    def run(self):
        # 初始化
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
        # 播放背景音乐
        resource_loader.playbgm()
        # 开始游戏
        def startgame():
            game_levels = GameLevels(cfg, resource_loader, screen)
            game_levels.start()
        # 开始界面
        components = pygame.sprite.Group()
        title_label = Label(screen, 700, 100, 400, 200)
        title_label.addtext('ANGRY BIRDS', 80, cfg.FONT_PATHS_DICT_NOINIT['arfmoochikncheez'], (236, 240, 241))
        components.add(title_label)
        start_btn = Button(screen, 500, 400, 300, 100, startgame, (244, 208, 63), (247, 220, 111))
        start_btn.addtext('START GAME', 60, cfg.FONT_PATHS_DICT_NOINIT['arfmoochikncheez'], cfg.BACKGROUND_COLOR)
        components.add(start_btn)
        quit_btn = Button(screen, 1000, 400, 300, 100, QuitGame, (241, 148, 138), (245, 183, 177))
        quit_btn.addtext('QUIT', 60, cfg.FONT_PATHS_DICT_NOINIT['arfmoochikncheez'], cfg.BACKGROUND_COLOR)
        components.add(quit_btn)
        charles_label = Label(screen, cfg.SCREENSIZE[0] - 300, cfg.SCREENSIZE[1] - 80, 300, 100)
        charles_label.addtext('CHARLES', 60, cfg.FONT_PATHS_DICT_NOINIT['arfmoochikncheez'], (41, 41, 41))
        components.add(charles_label)
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        QuitGame()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_btn.selected():
                        start_btn.action()
                    elif quit_btn.selected():
                        quit_btn.action()
            screen.fill(cfg.BACKGROUND_COLOR)
            for component in components: component.draw()
            pygame.display.update()
            clock.tick(cfg.FPS)