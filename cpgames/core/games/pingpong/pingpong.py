'''
Function:
    乒乓球小游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import pygame
from ...utils import QuitGame
from ..base import PygameBaseGame
from .modules import Ball, Racket


'''配置类'''
class Config():
    # 根目录
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # FPS
    FPS = 10
    FPS_GAMING = 100
    # 屏幕大小
    SCREENSIZE = (500, 500)
    # 一些颜色
    WHITE = (255, 255, 255)
    # 标题
    TITLE = '乒乓球小游戏 —— Charles的皮卡丘'
    # 背景音乐路径
    BGM_PATH = os.path.join(rootdir, 'resources/audios/bgm.mp3')
    # 游戏声音路径
    SOUND_PATHS_DICT = {
        'goal': os.path.join(rootdir, 'resources/audios/goal.wav'),
        'hit': os.path.join(rootdir, 'resources/audios/hit.wav'),
    }
    # 字体路径
    FONT_PATHS_DICT = {
        'default20': {'name': os.path.join(rootdir.replace('pingpong', 'base'), 'resources/fonts/MaiandraGD.ttf'), 'size': 20},
        'default30': {'name': os.path.join(rootdir.replace('pingpong', 'base'), 'resources/fonts/MaiandraGD.ttf'), 'size': 30},
        'default50': {'name': os.path.join(rootdir.replace('pingpong', 'base'), 'resources/fonts/MaiandraGD.ttf'), 'size': 50},
    }
    # 游戏图片路径
    IMAGE_PATHS_DICT = {
        'ball': os.path.join(rootdir, 'resources/images/ball.png'),
        'racket': os.path.join(rootdir, 'resources/images/racket.png'),
    }


'''乒乓球小游戏'''
class PingpongGame(PygameBaseGame):
    game_type = 'pingpong'
    def __init__(self, **kwargs):
        self.cfg = Config()
        super(PingpongGame, self).__init__(config=self.cfg, **kwargs)
    '''运行游戏'''
    def run(self):
        # 初始化
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
        # 开始游戏
        while True:
            score_left, score_right = self.GamingInterface(screen, resource_loader, cfg)
            self.endInterface(cfg, screen, score_left, score_right)
    '''游戏界面'''
    def GamingInterface(self, screen, resource_loader, cfg):
        # 初始化
        hit_sound = resource_loader.sounds['hit']
        goal_sound = resource_loader.sounds['goal']
        font = resource_loader.fonts['default50']
        resource_loader.playbgm()
        # 开始界面
        game_mode = self.startInterface(screen)
        # 游戏主循环
        # --左边球拍(ws控制, 仅双人模式时可控制)
        score_left = 0
        racket_left = Racket(cfg.IMAGE_PATHS_DICT['racket'], 'LEFT', cfg)
        # --右边球拍(↑↓控制)
        score_right = 0
        racket_right = Racket(cfg.IMAGE_PATHS_DICT['racket'], 'RIGHT', cfg)
        # --球
        ball = Ball(cfg.IMAGE_PATHS_DICT['ball'], cfg)
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
            screen.fill((41, 36, 33))
            # 玩家操作
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_UP]:
                racket_right.move('UP')
            elif pressed_keys[pygame.K_DOWN]:
                racket_right.move('DOWN')
            if game_mode == 2:
                if pressed_keys[pygame.K_w]:
                    racket_left.move('UP')
                elif pressed_keys[pygame.K_s]:
                    racket_left.move('DOWN')
            else:
                racket_left.automove(ball)
            # 球运动
            scores = ball.move(ball, racket_left, racket_right, hit_sound, goal_sound)
            score_left += scores[0]
            score_right += scores[1]
            # 显示
            # --分隔线
            pygame.draw.rect(screen, cfg.WHITE, (247, 0, 6, 500))
            # --球
            ball.draw(screen)
            # --拍
            racket_left.draw(screen)
            racket_right.draw(screen)
            # --得分
            screen.blit(font.render(str(score_left), False, cfg.WHITE), (150, 10))
            screen.blit(font.render(str(score_right), False, cfg.WHITE), (300, 10))
            if score_left == 11 or score_right == 11:
                return score_left, score_right
            clock.tick(cfg.FPS_GAMING)
            pygame.display.update()
    '''定义按钮'''
    def Button(self, screen, position, text, button_size=(200, 50)):
        left, top = position
        bwidth, bheight = button_size
        pygame.draw.line(screen, (150, 150, 150), (left, top), (left+bwidth, top), 5)
        pygame.draw.line(screen, (150, 150, 150), (left, top-2), (left, top+bheight), 5)
        pygame.draw.line(screen, (50, 50, 50), (left, top+bheight), (left+bwidth, top+bheight), 5)
        pygame.draw.line(screen, (50, 50, 50), (left+bwidth, top+bheight), (left+bwidth, top), 5)
        pygame.draw.rect(screen, (100, 100, 100), (left, top, bwidth, bheight))
        font = self.resource_loader.fonts['default30']
        text_render = font.render(text, 1, (255, 235, 205))
        return screen.blit(text_render, (left+50, top+10))
    '''开始界面'''
    def startInterface(self, screen):
        clock = pygame.time.Clock()
        while True:
            screen.fill((41, 36, 33))
            button_1 = self.Button(screen, (150, 175), '1 Player')
            button_2 = self.Button(screen, (150, 275), '2 Player')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_1.collidepoint(pygame.mouse.get_pos()):
                        return 1
                    elif button_2.collidepoint(pygame.mouse.get_pos()):
                        return 2
            clock.tick(self.cfg.FPS)
            pygame.display.update()
    '''结束界面'''
    def endInterface(self, cfg, screen, score_left, score_right):
        clock = pygame.time.Clock()
        font1 = self.resource_loader.fonts['default30']
        font2 = self.resource_loader.fonts['default20']
        msg = 'Player on left won!' if score_left > score_right else 'Player on right won!'
        texts = [
            font1.render(msg, True, cfg.WHITE),
            font2.render('Press ESCAPE to quit.', True, cfg.WHITE),
            font2.render('Press ENTER to continue or play again.', True, cfg.WHITE)
        ]
        positions = [[120, 200], [155, 270], [80, 300]]
        while True:
            screen.fill((41, 36, 33))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return
                    elif event.key == pygame.K_ESCAPE:
                        QuitGame()
            for text, pos in zip(texts, positions):
                screen.blit(text, pos)
            clock.tick(self.cfg.FPS)
            pygame.display.update()