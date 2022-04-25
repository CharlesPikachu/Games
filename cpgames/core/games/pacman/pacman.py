'''
Function:
    吃豆人小游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import pygame
from ...utils import QuitGame
from ..base import PygameBaseGame
from .modules import levels as Levels


'''配置类'''
class Config():
    # 根目录
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # FPS
    FPS = 10
    # 屏幕大小
    SCREENSIZE = (606, 606)
    # 标题
    TITLE = '吃豆人小游戏 —— Charles的皮卡丘'
    # 定义一些颜色
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    PURPLE = (255, 0, 255)
    SKYBLUE = (0, 191, 255)
    # 背景音乐路径
    BGM_PATH = os.path.join(rootdir, 'resources/audios/bgm.mp3')
    # 字体路径
    FONT_PATHS_DICT = {
        'default_s': {'name': os.path.join(rootdir, 'resources/fonts/ALGER.ttf'), 'size': 18},
        'default_l': {'name': os.path.join(rootdir, 'resources/fonts/ALGER.ttf'), 'size': 24},
    }
    # 游戏图片路径
    IMAGE_PATHS_DICT = {
        'icon': os.path.join(rootdir, 'resources/images/icon.png'),
        'pacman': os.path.join(rootdir, 'resources/images/pacman.png'),
        'ghost': {
            'Blinky': os.path.join(rootdir, 'resources/images/Blinky.png'),
            'Clyde': os.path.join(rootdir, 'resources/images/Clyde.png'),
            'Inky': os.path.join(rootdir, 'resources/images/Inky.png'),
            'Pinky': os.path.join(rootdir, 'resources/images/Pinky.png'),
        },
    }
        

'''吃豆人小游戏'''
class PacmanGame(PygameBaseGame):
    game_type = 'pacman'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(PacmanGame, self).__init__(config=self.cfg, **kwargs)
    '''运行游戏'''
    def run(self):
        # 初始化
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
        pygame.display.set_icon(resource_loader.images['icon'])
        font_small = resource_loader.fonts['default_s']
        font_big = resource_loader.fonts['default_l']
        # 播放背景音乐
        resource_loader.playbgm()
        # 游戏主循环
        for num_level in range(1, Levels.NUMLEVELS+1):
            level = getattr(Levels, f'Level{num_level}')()
            is_clearance = self.startLevelGame(cfg, resource_loader, level, screen, font_small)
            if num_level == Levels.NUMLEVELS:
                self.showText(cfg, screen, font_big, is_clearance, True)
            else:
                self.showText(cfg, screen, font_big, is_clearance)
    '''开始某一关游戏'''
    def startLevelGame(self, cfg, resource_loader, level, screen, font):
        clock = pygame.time.Clock()
        SCORE = 0
        wall_sprites = level.setupWalls(cfg.SKYBLUE)
        gate_sprites = level.setupGate(cfg.WHITE)
        hero_sprites, ghost_sprites = level.setupPlayers(resource_loader.images['pacman'], resource_loader.images['ghost'])
        food_sprites = level.setupFood(cfg.YELLOW, cfg.WHITE)
        is_clearance = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        for hero in hero_sprites:
                            hero.changeSpeed([-1, 0])
                            hero.is_move = True
                    elif event.key == pygame.K_RIGHT:
                        for hero in hero_sprites:
                            hero.changeSpeed([1, 0])
                            hero.is_move = True
                    elif event.key == pygame.K_UP:
                        for hero in hero_sprites:
                            hero.changeSpeed([0, -1])
                            hero.is_move = True
                    elif event.key == pygame.K_DOWN:
                        for hero in hero_sprites:
                            hero.changeSpeed([0, 1])
                            hero.is_move = True
                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT) or (event.key == pygame.K_UP) or (event.key == pygame.K_DOWN):
                        hero.is_move = False
            screen.fill(cfg.BLACK)
            for hero in hero_sprites:
                hero.update(wall_sprites, gate_sprites)
            hero_sprites.draw(screen)
            for hero in hero_sprites:
                food_eaten = pygame.sprite.spritecollide(hero, food_sprites, True)
            SCORE += len(food_eaten)
            wall_sprites.draw(screen)
            gate_sprites.draw(screen)
            food_sprites.draw(screen)
            for ghost in ghost_sprites:
                # 幽灵随机运动(效果不好且有BUG)
                '''
                res = ghost.update(wall_sprites, None)
                while not res:
                    ghost.changeSpeed(ghost.randomDirection())
                    res = ghost.update(wall_sprites, None)
                '''
                # 指定幽灵运动路径
                if ghost.tracks_loc[1] < ghost.tracks[ghost.tracks_loc[0]][2]:
                    ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
                    ghost.tracks_loc[1] += 1
                else:
                    if ghost.tracks_loc[0] < len(ghost.tracks) - 1:
                        ghost.tracks_loc[0] += 1
                    elif ghost.role_name == 'Clyde':
                        ghost.tracks_loc[0] = 2
                    else:
                        ghost.tracks_loc[0] = 0
                    ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
                    ghost.tracks_loc[1] = 0
                if ghost.tracks_loc[1] < ghost.tracks[ghost.tracks_loc[0]][2]:
                    ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
                else:
                    if ghost.tracks_loc[0] < len(ghost.tracks) - 1:
                        loc0 = ghost.tracks_loc[0] + 1
                    elif ghost.role_name == 'Clyde':
                        loc0 = 2
                    else:
                        loc0 = 0
                    ghost.changeSpeed(ghost.tracks[loc0][0: 2])
                ghost.update(wall_sprites, None)
            ghost_sprites.draw(screen)
            score_text = font.render("Score: %s" % SCORE, True, cfg.RED)
            screen.blit(score_text, [10, 10])
            if len(food_sprites) == 0:
                is_clearance = True
                break
            if pygame.sprite.groupcollide(hero_sprites, ghost_sprites, False, False):
                is_clearance = False
                break
            pygame.display.flip()
            clock.tick(self.cfg.FPS)
        return is_clearance
    '''显示文字'''
    def showText(self, cfg, screen, font, is_clearance, flag=False):
        clock = pygame.time.Clock()
        msg = 'Game Over!' if not is_clearance else 'Congratulations, you won!'
        positions = [[235, 233], [65, 303], [170, 333]] if not is_clearance else [[145, 233], [65, 303], [170, 333]]
        surface = pygame.Surface((400, 200))
        surface.set_alpha(10)
        surface.fill((128, 128, 128))
        screen.blit(surface, (100, 200))
        texts = [font.render(msg, True, cfg.WHITE),
                font.render('Press ENTER to continue or play again.', True, cfg.WHITE),
                font.render('Press ESCAPE to quit.', True, cfg.WHITE)]
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if is_clearance:
                            if not flag:
                                return
                            else:
                                self.run()
                        else:
                            self.run()
                    elif event.key == pygame.K_ESCAPE:
                        QuitGame()
            for idx, (text, position) in enumerate(zip(texts, positions)):
                screen.blit(text, position)
            pygame.display.flip()
            clock.tick(self.cfg.FPS)