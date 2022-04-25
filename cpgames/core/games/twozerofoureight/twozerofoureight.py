'''
Function:
    2048小游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import pygame
from ...utils import QuitGame
from ..base import PygameBaseGame
from .modules import getColorByNumber, drawGameMatrix, drawScore, drawGameIntro, EndInterface, Game2048


'''配置类'''
class Config():
    # 根目录
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # FPS
    FPS = 60
    # 屏幕大小
    SCREENSIZE = (650, 370)
    # 标题
    TITLE = '2048小游戏 —— Charles的皮卡丘'
    # 背景颜色
    BG_COLOR = '#92877d'
    # 保存当前最高分的文件
    MAX_SCORE_FILEPATH = os.path.join(rootdir, 'score')
    # 一些必要的常量
    MARGIN_SIZE = 10
    BLOCK_SIZE = 80
    GAME_MATRIX_SIZE = (4, 4)
    # 背景音乐路径
    BGM_PATH = os.path.join(rootdir, 'resources/audios/bgm.mp3')
    # 字体路径
    FONTPATH = os.path.join(rootdir.replace('twozerofoureight', 'base'), 'resources/fonts/Gabriola.ttf')


'''2048小游戏'''
class TwoZeroFourEightGame(PygameBaseGame):
    game_type = 'twozerofoureight'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(TwoZeroFourEightGame, self).__init__(config=self.cfg, **kwargs)
    '''运行游戏'''
    def run(self):
        # 初始化
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
        while True:
            if not self.GamingInterface(screen, resource_loader, cfg):
                break
    '''游戏运行界面'''
    def GamingInterface(self, screen, resource_loader, cfg):
        # 播放背景音乐
        resource_loader.playbgm()
        # 实例化2048游戏
        game_2048 = Game2048(matrix_size=cfg.GAME_MATRIX_SIZE, max_score_filepath=cfg.MAX_SCORE_FILEPATH)
        # 游戏主循环
        clock = pygame.time.Clock()
        is_running = True
        while is_running:
            screen.fill(pygame.Color(cfg.BG_COLOR))
            # --按键检测
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                        game_2048.setDirection({pygame.K_UP: 'up', pygame.K_DOWN: 'down', pygame.K_LEFT: 'left', pygame.K_RIGHT: 'right'}[event.key])
            # --更新游戏状态
            game_2048.update()
            if game_2048.isgameover:
                game_2048.saveMaxScore()
                is_running = False
            # --将必要的游戏元素画到屏幕上
            drawGameMatrix(screen, game_2048.game_matrix, cfg)
            start_x, start_y = drawScore(screen, game_2048.score, game_2048.max_score, cfg)
            drawGameIntro(screen, start_x, start_y, cfg)
            # --屏幕更新
            pygame.display.update()
            clock.tick(cfg.FPS)
        return EndInterface(screen, cfg)