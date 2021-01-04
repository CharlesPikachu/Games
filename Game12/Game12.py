'''
Function:
    推箱子小游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import sys
import cfg
import pygame
from modules import *
from itertools import chain


'''游戏地图'''
class gameMap():
    def __init__(self, num_cols, num_rows):
        self.walls = []
        self.boxes = []
        self.targets = []
        self.num_cols = num_cols
        self.num_rows = num_rows
    '''增加游戏元素'''
    def addElement(self, elem_type, col, row):
        if elem_type == 'wall':
            self.walls.append(elementSprite('wall.png', col, row, cfg))
        elif elem_type == 'box':
            self.boxes.append(elementSprite('box.png', col, row, cfg))
        elif elem_type == 'target':
            self.targets.append(elementSprite('target.png', col, row, cfg))
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
            block_size = cfg.BLOCKSIZE
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
class gameInterface():
    def __init__(self, screen):
        self.screen = screen
        self.levels_path = cfg.LEVELDIR
        self.initGame()
    '''导入关卡地图'''
    def loadLevel(self, game_level):
        with open(os.path.join(self.levels_path, game_level), 'r') as f:
            lines = f.readlines()
        # 游戏地图
        self.game_map = gameMap(max([len(line) for line in lines]) - 1, len(lines))
        # 游戏surface
        height = cfg.BLOCKSIZE * self.game_map.num_rows
        width = cfg.BLOCKSIZE * self.game_map.num_cols
        self.game_surface = pygame.Surface((width, height))
        self.game_surface.fill(cfg.BACKGROUNDCOLOR)
        self.game_surface_blank = self.game_surface.copy()
        for row, elems in enumerate(lines):
            for col, elem in enumerate(elems):
                if elem == 'p':
                    self.player = pusherSprite(col, row, cfg)
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
        if (x + cfg.SCREENSIZE[0] // 2) > cfg.SCREENSIZE[0]:
            if -1 * self.scroll_x + cfg.SCREENSIZE[0] < width:
                self.scroll_x -= 2
        elif (x + cfg.SCREENSIZE[0] // 2) > 0:
            if self.scroll_x < 0:
                self.scroll_x += 2
        if (y + cfg.SCREENSIZE[1] // 2) > cfg.SCREENSIZE[1]:
            if -1 * self.scroll_y + cfg.SCREENSIZE[1] < height:
                self.scroll_y -= 2
        elif (y + 250) > 0:
            if self.scroll_y < 0:
                self.scroll_y += 2


'''某一关卡的游戏主循环'''
def runGame(screen, game_level):
    clock = pygame.time.Clock()
    game_interface = gameInterface(screen)
    game_interface.loadLevel(game_level)
    font_path = os.path.join(cfg.FONTDIR, 'simkai.ttf')
    text = '按R键重新开始本关'
    font = pygame.font.Font(font_path, 15)
    text_render = font.render(text, 1, (255, 255, 255))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
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
        clock.tick(100)


'''主函数'''
def main():
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption('推箱子 —— Charles的皮卡丘')
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.mixer.init()
    audio_path = os.path.join(cfg.AUDIODIR, 'EineLiebe.mp3')
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    startInterface(screen, cfg)
    for level_name in sorted(os.listdir(cfg.LEVELDIR)):
        runGame(screen, level_name)
        switchInterface(screen, cfg)
    endInterface(screen, cfg)


'''run'''
if __name__ == '__main__':
    main()