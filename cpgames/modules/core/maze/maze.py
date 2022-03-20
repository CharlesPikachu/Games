'''
Function:
    走迷宫小游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import pygame
from ...utils import QuitGame
from ..base import PygameBaseGame
from .modules import showText, Button, Interface, Block, RandomMaze, Hero


'''配置类'''
class Config():
    # 根目录
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # FPS
    FPS = 20
    # 屏幕大小
    SCREENSIZE = (800, 625)
    # 标题
    TITLE = '走迷宫小游戏 —— Charles的皮卡丘'
    # 块大小
    BLOCKSIZE = 15
    MAZESIZE = (35, 50) # num_rows * num_cols
    BORDERSIZE = (25, 50) # 25 * 2 + 50 * 15 = 800, 50 * 2 + 35 * 15 = 625
    # 背景音乐路径
    BGM_PATH = os.path.join(rootdir, 'resources/audios/bgm.mp3')
    # 游戏图片路径
    IMAGE_PATHS_DICT = {
        'hero': os.path.join(rootdir, 'resources/images/hero.png'),
    }


'''走迷宫小游戏'''
class MazeGame(PygameBaseGame):
    game_type = 'maze'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(MazeGame, self).__init__(config=self.cfg, **kwargs)
    '''运行游戏'''
    def run(self):
        # 初始化
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
        font = pygame.font.SysFont('Consolas', 15)
        # 播放背景音乐
        resource_loader.playbgm()
        # 开始界面
        Interface(screen, cfg, 'game_start')
        # 记录关卡数
        num_levels = 0
        # 记录最少用了多少步通关
        best_scores = 'None'
        # 关卡循环切换
        while True:
            num_levels += 1
            clock = pygame.time.Clock()
            screen = pygame.display.set_mode(cfg.SCREENSIZE)
            # --随机生成关卡地图
            maze_now = RandomMaze(cfg.MAZESIZE, cfg.BLOCKSIZE, cfg.BORDERSIZE)
            # --生成hero
            hero_now = Hero(resource_loader.images['hero'], [0, 0], cfg.BLOCKSIZE, cfg.BORDERSIZE)
            # --统计步数
            num_steps = 0
            # --关卡内主循环
            while True:
                dt = clock.tick(cfg.FPS)
                screen.fill((255, 255, 255))
                is_move = False
                # ----↑↓←→控制hero
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        QuitGame()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            is_move = hero_now.move('up', maze_now)
                        elif event.key == pygame.K_DOWN:
                            is_move = hero_now.move('down', maze_now)
                        elif event.key == pygame.K_LEFT:
                            is_move = hero_now.move('left', maze_now)
                        elif event.key == pygame.K_RIGHT:
                            is_move = hero_now.move('right', maze_now)
                num_steps += int(is_move)
                hero_now.draw(screen)
                maze_now.draw(screen)
                # ----显示一些信息
                showText(screen, font, 'LEVELDONE: %d' % num_levels, (255, 0, 0), (10, 10))
                showText(screen, font, 'BESTSCORE: %s' % best_scores, (255, 0, 0), (210, 10))
                showText(screen, font, 'USEDSTEPS: %s' % num_steps, (255, 0, 0), (410, 10))
                showText(screen, font, 'S: your starting point    D: your destination', (255, 0, 0), (10, 600))
                # ----判断游戏是否胜利
                if (hero_now.coordinate[0] == cfg.MAZESIZE[1] - 1) and (hero_now.coordinate[1] == cfg.MAZESIZE[0] - 1):
                    break
                pygame.display.update()
            # --更新最优成绩
            if best_scores == 'None':
                best_scores = num_steps
            else:
                if best_scores > num_steps:
                    best_scores = num_steps
            # --关卡切换
            Interface(screen, cfg, mode='game_switch')