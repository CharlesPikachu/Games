'''
Function:
    魔塔小游戏主要逻辑实现
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import pygame
from .sprites import Hero
from .maps import MapParser


'''魔塔小游戏主要逻辑实现'''
class GameLevels():
    def __init__(self, cfg):
        self.cfg = cfg
        # 加载游戏地图中的所有图片
        self.map_element_images = {}
        for key, value in self.cfg.MAPELEMENTSPATHS.items():
            self.map_element_images[key] = [
                pygame.image.load(value[0]),
                pygame.image.load(value[1]),
            ]
        # 加载游戏背景图片
        self.background_images = {}
        for key, value in cfg.BACKGROUNDPATHS.items():
            self.background_images[key] = pygame.transform.scale(pygame.image.load(value), cfg.SCREENSIZE)
        # 游戏地图解析类
        self.map_level_pointer = 0
        self.loadmap()
        # 英雄类
        self.hero = Hero(
            imagepaths=cfg.HEROPATHS,
            blocksize=cfg.BLOCKSIZE,
            block_position=self.map_parser.getheroposition(),
            offset=(325, 55),
            fontpath=cfg.FONTPATH_CN,
        )
    '''导入地图'''
    def loadmap(self):
        self.map_parser = MapParser(
            blocksize=self.cfg.BLOCKSIZE, 
            filepath=self.cfg.MAPPATHS[self.map_level_pointer], 
            element_images=self.map_element_images,
            offset=(325, 55),
        )
    '''运行'''
    def run(self, screen):
        # 游戏主循环
        clock = pygame.time.Clock()
        is_running = True
        while is_running:
            screen.fill((0, 0, 0))
            screen.blit(self.background_images['gamebg'], (0, 0))
            # --按键检测
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            key_pressed = pygame.key.get_pressed()
            move_events = []
            if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
                move_events = self.hero.move('up', self.map_parser)
            elif key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
                move_events = self.hero.move('down', self.map_parser)
            elif key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
                move_events = self.hero.move('left', self.map_parser)
            elif key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
                move_events = self.hero.move('right', self.map_parser)
            if not move_events: move_events = []
            # --画游戏地图
            self.map_parser.draw(screen)
            # --画英雄
            self.hero.draw(screen)
            # --触发游戏事件
            for event in move_events:
                if event == 'upstairs':
                    self.map_level_pointer += 1
                    self.loadmap()
                    self.hero.placenexttostairs(self.map_parser, 'down')
                elif event == 'downstairs':
                    self.map_level_pointer -= 1
                    self.loadmap()
                    self.hero.placenexttostairs(self.map_parser, 'up')
            # --刷新
            pygame.display.flip()
            clock.tick(self.cfg.FPS)