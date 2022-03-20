'''
Function:
    消消乐
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import pygame
from ...utils import QuitGame
from ..base import PygameBaseGame
from .modules import gemSprite, gemGame


'''配置类'''
class Config():
    # 根目录
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # FPS
    FPS = 30
    # 屏幕大小
    SCREENSIZE = (600, 600)
    # 标题
    TITLE = '消消乐 —— Charles的皮卡丘'
    # 游戏元素尺寸
    NUMGRID = 8
    GRIDSIZE = 64
    XMARGIN = (SCREENSIZE[0] - GRIDSIZE * NUMGRID) // 2
    YMARGIN = (SCREENSIZE[1] - GRIDSIZE * NUMGRID) // 2
    # 背景音乐路径
    BGM_PATH = os.path.join(rootdir, 'resources/audios/bg.mp3')
    # 游戏声音路径
    SOUND_PATHS_DICT = {
        'mismatch': os.path.join(rootdir, 'resources/audios/badswap.wav'),
        'match': [
            os.path.join(rootdir, 'resources/audios/match0.wav'),
            os.path.join(rootdir, 'resources/audios/match1.wav'),
            os.path.join(rootdir, 'resources/audios/match2.wav'),
            os.path.join(rootdir, 'resources/audios/match3.wav'),
            os.path.join(rootdir, 'resources/audios/match4.wav'),
            os.path.join(rootdir, 'resources/audios/match5.wav'),
        ],
    }
    # 字体路径
    FONT_PATHS_DICT = {
        'default': {'name': os.path.join(rootdir.replace('gemgem', 'base'), 'resources/fonts/MaiandraGD.ttf'), 'size': 25},
    }
    # 游戏图片路径
    IMAGE_PATHS_DICT = {
        'gem': {
            '1': os.path.join(rootdir, 'resources/images/gem1.png'),
            '2': os.path.join(rootdir, 'resources/images/gem2.png'),
            '3': os.path.join(rootdir, 'resources/images/gem3.png'),
            '4': os.path.join(rootdir, 'resources/images/gem4.png'),
            '5': os.path.join(rootdir, 'resources/images/gem5.png'),
            '6': os.path.join(rootdir, 'resources/images/gem6.png'),
            '7': os.path.join(rootdir, 'resources/images/gem7.png'),
        }
    }


'''消消乐'''
class GemGemGame(PygameBaseGame):
    game_type = 'gemgem'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(GemGemGame, self).__init__(config=self.cfg, **kwargs)
    '''运行游戏'''
    def run(self):
        # 初始化
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
        # 播放背景音乐
        resource_loader.playbgm()
        # 音效
        sounds = resource_loader.sounds
        # 字体
        font = resource_loader.fonts['default']
        # 图片加载
        gem_imgs = resource_loader.images['gem']
        # 主循环
        game = gemGame(screen, sounds, font, gem_imgs, cfg)
        while True:
            score = game.start()
            flag = False
            # 一轮游戏结束后玩家选择重玩或者退出
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                        QuitGame()
                    elif event.type == pygame.KEYUP and event.key == pygame.K_r:
                        flag = True
                if flag:
                    break
                screen.fill((135, 206, 235))
                text0 = 'Final score: %s' % score
                text1 = 'Press <R> to restart the game.'
                text2 = 'Press <Esc> to quit the game.'
                y = 150
                for idx, text in enumerate([text0, text1, text2]):
                    text_render = font.render(text, 1, (85, 65, 0))
                    rect = text_render.get_rect()
                    if idx == 0:
                        rect.left, rect.top = (212, y)
                    elif idx == 1:
                        rect.left, rect.top = (122.5, y)
                    else:
                        rect.left, rect.top = (126.5, y)
                    y += 100
                    screen.blit(text_render, rect)
                pygame.display.update()
            game.reset()