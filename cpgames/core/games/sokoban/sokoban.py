'''
Function:
    推箱子
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import pygame
from itertools import chain
from ...utils import QuitGame
from ..base import PygameBaseGame
from .modules import pusherSprite, elementSprite, startInterface, endInterface, switchInterface


'''配置类'''
class Config():
    # 根目录
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # FPS
    FPS = 60
    FPS_GAMING = 100
    # 屏幕大小
    SCREENSIZE = (500, 500)
    # 标题
    TITLE = '推箱子 —— Charles的皮卡丘'
    # block大小
    BLOCKSIZE = 50
    # 背景颜色
    BACKGROUNDCOLOR = (45, 45, 45)
    # levels所在文件夹
    LEVELDIR = os.path.join(rootdir, 'resources/levels')
    # 背景音乐路径
    BGM_PATH = os.path.join(rootdir, 'resources/audios/EineLiebe.mp3')
    # 字体路径
    FONT_PATHS_DICT = {
        'default_15': {'name': os.path.join(rootdir.replace('sokoban', 'base'), 'resources/fonts/simkai.ttf'), 'size': 15},
        'default_30': {'name': os.path.join(rootdir.replace('sokoban', 'base'), 'resources/fonts/simkai.ttf'), 'size': 30},
        'default_50': {'name': os.path.join(rootdir.replace('sokoban', 'base'), 'resources/fonts/simkai.ttf'), 'size': 50},
    }
    # 游戏图片路径
    IMAGE_PATHS_DICT = {
        'box': os.path.join(rootdir, 'resources/images/box.png'),
        'player': os.path.join(rootdir, 'resources/images/player.png'),
        'target': os.path.join(rootdir, 'resources/images/target.png'),
        'wall': os.path.join(rootdir, 'resources/images/wall.png'),
    }


'''游戏地图'''
class GameMap():
    def __init__(self, num_cols, num_rows, cfg, resource_loader):
        self.cfg = cfg
        self.resource_loader = resource_loader
        self.walls = []
        self.boxes = []
        self.targets = []
        self.num_cols = num_cols
        self.num_rows = num_rows
    '''增加游戏元素'''
    def addElement(self, elem_type, col, row):
        if elem_type == 'wall':
            self.walls.append(elementSprite('wall', col, row, self.cfg, self.resource_loader))
        elif elem_type == 'box':
            self.boxes.append(elementSprite('box', col, row, self.cfg, self.resource_loader))
        elif elem_type == 'target':
            self.targets.append(elementSprite('target', col, row, self.cfg, self.resource_loader))
    '''画游戏地图'''
    def draw(self, screen):
        for elem in self.elemsIter():
            elem.draw(screen)
    '''游戏元素迭代器'''
    def elemsIter(self):
        for elem in chain(self.targets, self.walls, self.boxes):
            yield elem
    '''该关卡中所有的箱子是否都在指定位置, 在的话就是通关了'''
    def levelCompleted(self):
        for box in self.boxes:
            is_match = False
            for target in self.targets:
                if box.col == target.col and box.row == target.row:
                    is_match = True
                    break
            if not is_match:
                return False
        return True
    '''某位置是否可到达'''
    def isValidPos(self, col, row):
        if col >= 0 and row >= 0 and col < self.num_cols and row < self.num_rows:
            block_size = self.cfg.BLOCKSIZE
            temp1 = self.walls + self.boxes
            temp2 = pygame.Rect(col * block_size, row * block_size, block_size, block_size)
            return temp2.collidelist(temp1) == -1
        else:
            return False
    '''获得某位置的box'''
    def getBox(self, col, row):
        for box in self.boxes:
            if box.col == col and box.row == row:
                return box
        return None


'''游戏界面'''
class GameInterface():
    def __init__(self, screen, cfg, resource_loader):
        self.cfg = cfg
        self.resource_loader = resource_loader
        self.screen = screen
        self.levels_path = cfg.LEVELDIR
        self.initGame()
    '''导入关卡地图'''
    def loadLevel(self, game_level):
        with open(os.path.join(self.levels_path, game_level), 'r') as f:
            lines = f.readlines()
        # 游戏地图
        self.game_map = GameMap(max([len(line) for line in lines]) - 1, len(lines), self.cfg, self.resource_loader)
        # 游戏surface
        height = self.cfg.BLOCKSIZE * self.game_map.num_rows
        width = self.cfg.BLOCKSIZE * self.game_map.num_cols
        self.game_surface = pygame.Surface((width, height))
        self.game_surface.fill(self.cfg.BACKGROUNDCOLOR)
        self.game_surface_blank = self.game_surface.copy()
        for row, elems in enumerate(lines):
            for col, elem in enumerate(elems):
                if elem == 'p':
                    self.player = pusherSprite(col, row, self.cfg, self.resource_loader)
                elif elem == '*':
                    self.game_map.addElement('wall', col, row)
                elif elem == '#':
                    self.game_map.addElement('box', col, row)
                elif elem == 'o':
                    self.game_map.addElement('target', col, row)
    '''游戏初始化'''
    def initGame(self):
        self.scroll_x = 0
        self.scroll_y = 0
    '''将游戏界面画出来'''
    def draw(self, *elems):
        self.scroll()
        self.game_surface.blit(self.game_surface_blank, dest=(0, 0))
        for elem in elems:
            elem.draw(self.game_surface)
        self.screen.blit(self.game_surface, dest=(self.scroll_x, self.scroll_y))
    '''因为游戏界面面积>游戏窗口界面, 所以需要根据人物位置滚动'''
    def scroll(self):
        x, y = self.player.rect.center
        width = self.game_surface.get_rect().w
        height = self.game_surface.get_rect().h
        if (x + self.cfg.SCREENSIZE[0] // 2) > self.cfg.SCREENSIZE[0]:
            if -1 * self.scroll_x + self.cfg.SCREENSIZE[0] < width:
                self.scroll_x -= 2
        elif (x + self.cfg.SCREENSIZE[0] // 2) > 0:
            if self.scroll_x < 0:
                self.scroll_x += 2
        if (y + self.cfg.SCREENSIZE[1] // 2) > self.cfg.SCREENSIZE[1]:
            if -1 * self.scroll_y + self.cfg.SCREENSIZE[1] < height:
                self.scroll_y -= 2
        elif (y + 250) > 0:
            if self.scroll_y < 0:
                self.scroll_y += 2


'''推箱子'''
class SokobanGame(PygameBaseGame):
    game_type = 'sokoban'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(SokobanGame, self).__init__(config=self.cfg, **kwargs)
    '''运行游戏'''
    def run(self):
        # 初始化
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
        # 播放背景音乐
        resource_loader.playbgm()
        # 游戏开始界面
        startInterface(screen, cfg, resource_loader)
        # 游戏界面
        for level_name in sorted(os.listdir(cfg.LEVELDIR)):
            self.runlevel(screen, level_name)
            switchInterface(screen, cfg, resource_loader)
        # 游戏结束界面
        endInterface(screen, cfg, resource_loader)
    '''某一关卡的游戏主循环'''
    def runlevel(self, screen, game_level):
        clock = pygame.time.Clock()
        game_interface = GameInterface(screen, self.cfg, self.resource_loader)
        game_interface.loadLevel(game_level)
        text = '按R键重新开始本关'
        font = self.resource_loader.fonts['default_15']
        text_render = font.render(text, 1, (255, 255, 255))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        next_pos = game_interface.player.move('left', is_test=True)
                        if game_interface.game_map.isValidPos(*next_pos):
                            game_interface.player.move('left')
                        else:
                            box = game_interface.game_map.getBox(*next_pos)
                            if box:
                                next_pos = box.move('left', is_test=True)
                                if game_interface.game_map.isValidPos(*next_pos):
                                    game_interface.player.move('left')
                                    box.move('left')
                        break
                    if event.key == pygame.K_RIGHT:
                        next_pos = game_interface.player.move('right', is_test=True)
                        if game_interface.game_map.isValidPos(*next_pos):
                            game_interface.player.move('right')
                        else:
                            box = game_interface.game_map.getBox(*next_pos)
                            if box:
                                next_pos = box.move('right', is_test=True)
                                if game_interface.game_map.isValidPos(*next_pos):
                                    game_interface.player.move('right')
                                    box.move('right')
                        break
                    if event.key == pygame.K_DOWN:
                        next_pos = game_interface.player.move('down', is_test=True)
                        if game_interface.game_map.isValidPos(*next_pos):
                            game_interface.player.move('down')
                        else:
                            box = game_interface.game_map.getBox(*next_pos)
                            if box:
                                next_pos = box.move('down', is_test=True)
                                if game_interface.game_map.isValidPos(*next_pos):
                                    game_interface.player.move('down')
                                    box.move('down')
                        break
                    if event.key == pygame.K_UP:
                        next_pos = game_interface.player.move('up', is_test=True)
                        if game_interface.game_map.isValidPos(*next_pos):
                            game_interface.player.move('up')
                        else:
                            box = game_interface.game_map.getBox(*next_pos)
                            if box:
                                next_pos = box.move('up', is_test=True)
                                if game_interface.game_map.isValidPos(*next_pos):
                                    game_interface.player.move('up')
                                    box.move('up')
                        break
                    if event.key == pygame.K_r:
                        game_interface.initGame()
                        game_interface.loadLevel(game_level)
            game_interface.draw(game_interface.player, game_interface.game_map)
            if game_interface.game_map.levelCompleted():
                return
            screen.blit(text_render, (5, 5))
            pygame.display.flip()
            clock.tick(self.cfg.FPS_GAMING)