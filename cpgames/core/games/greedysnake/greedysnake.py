'''
Function:
    贪吃蛇小游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import pygame
from ...utils import QuitGame
from ..base import PygameBaseGame
from .modules import drawGameGrid, showScore, EndInterface, Apple, Snake


'''配置类'''
class Config():
    # 根目录
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # FPS
    FPS = 5
    # 屏幕大小
    SCREENSIZE = (800, 500)
    # 标题
    TITLE = '贪吃蛇小游戏 —— Charles的皮卡丘'
    # 一些常量
    BLOCK_SIZE = 20
    BLACK = (0, 0, 0)
    GAME_MATRIX_SIZE = (int(SCREENSIZE[0]/BLOCK_SIZE), int(SCREENSIZE[1]/BLOCK_SIZE))
    # 背景音乐路径
    BGM_PATH = os.path.join(rootdir, 'resources/audios/bgm.mp3')
    # 字体路径
    FONT_PATHS_DICT = {
        'default30': {'name': os.path.join(rootdir.replace('greedysnake', 'base'), 'resources/fonts/Gabriola.ttf'), 'size': 30},
        'default60': {'name': os.path.join(rootdir.replace('greedysnake', 'base'), 'resources/fonts/Gabriola.ttf'), 'size': 60},
    }


'''贪吃蛇小游戏'''
class GreedySnakeGame(PygameBaseGame):
    game_type = 'greedysnake'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(GreedySnakeGame, self).__init__(config=self.cfg, **kwargs)
    '''运行游戏'''
    def run(self):
        # 初始化
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
        # 游戏主循环
        while True:
            if not self.GamingInterface(screen, resource_loader, cfg):
                break
    '''游戏运行界面'''
    def GamingInterface(self, screen, resource_loader, cfg):
        # 播放背景音乐
        resource_loader.playbgm()
        # 游戏主循环
        snake = Snake(cfg)
        apple = Apple(cfg, snake.coords)
        score = 0
        clock = pygame.time.Clock()
        while True:
            screen.fill(cfg.BLACK)
            # --按键检测
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                        snake.setDirection({pygame.K_UP: 'up', pygame.K_DOWN: 'down', pygame.K_LEFT: 'left', pygame.K_RIGHT: 'right'}[event.key])
            # --更新贪吃蛇和食物
            if snake.update(apple):
                apple = Apple(cfg, snake.coords)
                score += 1
            # --判断游戏是否结束
            if snake.isgameover: break
            # --显示游戏里必要的元素
            drawGameGrid(cfg, screen)
            snake.draw(screen)
            apple.draw(screen)
            showScore(cfg, score, screen, resource_loader)
            # --屏幕更新
            pygame.display.update()
            clock.tick(cfg.FPS)
        return EndInterface(screen, cfg, resource_loader)