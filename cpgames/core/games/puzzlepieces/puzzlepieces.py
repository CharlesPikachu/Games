'''
Function:
    拼图小游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import random
import pygame
from ...utils import QuitGame
from ..base import PygameBaseGame


'''配置类'''
class Config():
    # 根目录
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # FPS
    FPS = 40
    # 定义一些颜色
    BACKGROUNDCOLOR = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    # 随机打乱拼图次数
    NUMRANDOM = 100
    # 屏幕大小
    SCREENSIZE = (640, 640)
    # 标题
    TITLE = '拼图小游戏 —— Charles的皮卡丘'
    # 游戏图片路径
    IMAGE_PATHS_DICT = {}
    for item in os.listdir(os.path.join(rootdir, 'resources/images')):
        IMAGE_PATHS_DICT[item] = os.path.join(rootdir, f'resources/images/{item}')
    # 字体路径
    FONT_PATHS_DICT = {
        '1/4screenwidth': {'name': os.path.join(rootdir.replace('puzzlepieces', 'base'), 'resources/fonts/simkai.ttf'), 'size': SCREENSIZE[0] // 4},
        '1/15screenwidth': {'name': os.path.join(rootdir.replace('puzzlepieces', 'base'), 'resources/fonts/simkai.ttf'), 'size': SCREENSIZE[0] // 15},
        '1/20screenwidth': {'name': os.path.join(rootdir.replace('puzzlepieces', 'base'), 'resources/fonts/simkai.ttf'), 'size': SCREENSIZE[0] // 20},
    }


'''拼图小游戏'''
class PuzzlePiecesGame(PygameBaseGame):
    game_type = 'puzzlepieces'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(PuzzlePiecesGame, self).__init__(config=self.cfg, **kwargs)
    '''运行游戏'''
    def run(self):
        # 初始化
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
        for key in resource_loader.images:
            resource_loader.images[key] = pygame.transform.scale(resource_loader.images[key], cfg.SCREENSIZE)
        # 游戏开始界面
        size = self.ShowStartInterface(screen)
        assert isinstance(size, int)
        num_rows, num_cols = size, size
        num_cells = size * size
        # 使用的图片
        game_img_used = random.choice(list(resource_loader.images.values()))
        game_img_used_rect = game_img_used.get_rect()
        # 计算Cell大小
        cell_width = game_img_used_rect.width // num_cols
        cell_height = game_img_used_rect.height // num_rows
        # 避免初始化为原图
        while True:
            game_board, blank_cell_idx = self.CreateBoard(num_rows, num_cols, num_cells)
            if not self.isGameOver(game_board, size):
                break
        # 游戏主循环
        is_running = True
        clock = pygame.time.Clock()
        while is_running:
            # --事件捕获
            for event in pygame.event.get():
                # ----退出游戏
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    QuitGame()
                # ----键盘操作
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        blank_cell_idx = self.moveL(game_board, blank_cell_idx, num_cols)
                    elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                        blank_cell_idx = self.moveR(game_board, blank_cell_idx, num_cols)
                    elif event.key == pygame.K_UP or event.key == ord('w'):
                        blank_cell_idx = self.moveU(game_board, blank_cell_idx, num_rows, num_cols)
                    elif event.key == pygame.K_DOWN or event.key == ord('s'):
                        blank_cell_idx = self.moveD(game_board, blank_cell_idx, num_cols)
                # ----鼠标操作
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    x_pos = x // cell_width
                    y_pos = y // cell_height
                    idx = x_pos + y_pos * num_cols
                    if idx == blank_cell_idx-1:
                        blank_cell_idx = self.moveR(game_board, blank_cell_idx, num_cols)
                    elif idx == blank_cell_idx+1:
                        blank_cell_idx = self.moveL(game_board, blank_cell_idx, num_cols)
                    elif idx == blank_cell_idx+num_cols:
                        blank_cell_idx = self.moveU(game_board, blank_cell_idx, num_rows, num_cols)
                    elif idx == blank_cell_idx-num_cols:
                        blank_cell_idx = self.moveD(game_board, blank_cell_idx, num_cols)
            # --判断游戏是否结束
            if self.isGameOver(game_board, size):
                game_board[blank_cell_idx] = num_cells - 1
                is_running = False
            # --更新屏幕
            screen.fill(cfg.BACKGROUNDCOLOR)
            for i in range(num_cells):
                if game_board[i] == -1:
                    continue
                x_pos = i // num_cols
                y_pos = i % num_cols
                rect = pygame.Rect(y_pos*cell_width, x_pos*cell_height, cell_width, cell_height)
                img_area = pygame.Rect((game_board[i]%num_cols)*cell_width, (game_board[i]//num_cols)*cell_height, cell_width, cell_height)
                screen.blit(game_img_used, rect, img_area)
            for i in range(num_cols+1):
                pygame.draw.line(screen, cfg.BLACK, (i*cell_width, 0), (i*cell_width, game_img_used_rect.height))
            for i in range(num_rows+1):
                pygame.draw.line(screen, cfg.BLACK, (0, i*cell_height), (game_img_used_rect.width, i*cell_height))
            pygame.display.update()
            clock.tick(cfg.FPS)
        # 游戏结束界面
        self.ShowEndInterface(screen)
    '''判断游戏是否结束'''
    def isGameOver(self, board, size):
        assert isinstance(size, int)
        num_cells = size * size
        for i in range(num_cells-1):
            if board[i] != i: return False
        return True
    '''将空白Cell左边的Cell右移到空白Cell位置'''
    def moveR(self, board, blank_cell_idx, num_cols):
        if blank_cell_idx % num_cols == 0: return blank_cell_idx
        board[blank_cell_idx-1], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx-1]
        return blank_cell_idx - 1
    '''将空白Cell右边的Cell左移到空白Cell位置'''
    def moveL(self, board, blank_cell_idx, num_cols):
        if (blank_cell_idx+1) % num_cols == 0: return blank_cell_idx
        board[blank_cell_idx+1], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx+1]
        return blank_cell_idx + 1
    '''将空白Cell上边的Cell下移到空白Cell位置'''
    def moveD(self, board, blank_cell_idx, num_cols):
        if blank_cell_idx < num_cols: return blank_cell_idx
        board[blank_cell_idx-num_cols], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx-num_cols]
        return blank_cell_idx - num_cols
    '''将空白Cell下边的Cell上移到空白Cell位置'''
    def moveU(self, board, blank_cell_idx, num_rows, num_cols):
        if blank_cell_idx >= (num_rows-1) * num_cols: return blank_cell_idx
        board[blank_cell_idx+num_cols], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx+num_cols]
        return blank_cell_idx + num_cols
    '''获得打乱的拼图'''
    def CreateBoard(self, num_rows, num_cols, num_cells):
        board = []
        for i in range(num_cells): board.append(i)
        # 去掉右下角那块
        blank_cell_idx = num_cells - 1
        board[blank_cell_idx] = -1
        for i in range(self.cfg.NUMRANDOM):
            # 0: left, 1: right, 2: up, 3: down
            direction = random.randint(0, 3)
            if direction == 0: blank_cell_idx = self.moveL(board, blank_cell_idx, num_cols)
            elif direction == 1: blank_cell_idx = self.moveR(board, blank_cell_idx, num_cols)
            elif direction == 2: blank_cell_idx = self.moveU(board, blank_cell_idx, num_rows, num_cols)
            elif direction == 3: blank_cell_idx = self.moveD(board, blank_cell_idx, num_cols)
        return board, blank_cell_idx
    '''显示游戏结束界面'''
    def ShowEndInterface(self, screen):
        screen.fill(self.cfg.BACKGROUNDCOLOR)
        font = self.resource_loader.fonts['1/15screenwidth']
        title = font.render('恭喜! 你成功完成了拼图!', True, (233, 150, 122))
        rect = title.get_rect()
        rect.midtop = (self.cfg.SCREENSIZE[0] / 2, self.cfg.SCREENSIZE[1] / 2.5)
        screen.blit(title, rect)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    QuitGame()
            pygame.display.update()
    '''显示游戏开始界面'''
    def ShowStartInterface(self, screen):
        screen.fill(self.cfg.BACKGROUNDCOLOR)
        tfont = self.resource_loader.fonts['1/4screenwidth']
        cfont = self.resource_loader.fonts['1/20screenwidth']
        title = tfont.render('拼图游戏', True, self.cfg.RED)
        content1 = cfont.render('按H或M或L键开始游戏', True, self.cfg.BLUE)
        content2 = cfont.render('H为5*5模式, M为4*4模式, L为3*3模式', True, self.cfg.BLUE)
        trect = title.get_rect()
        trect.midtop = (self.cfg.SCREENSIZE[0] / 2, self.cfg.SCREENSIZE[1] / 10)
        crect1 = content1.get_rect()
        crect1.midtop = (self.cfg.SCREENSIZE[0] / 2, self.cfg.SCREENSIZE[1] / 2.2)
        crect2 = content2.get_rect()
        crect2.midtop = (self.cfg.SCREENSIZE[0] / 2, self.cfg.SCREENSIZE[1] / 1.8)
        screen.blit(title, trect)
        screen.blit(content1, crect1)
        screen.blit(content2, crect2)
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    QuitGame()
                elif event.type == pygame.KEYDOWN:
                    if event.key == ord('l'): return 3
                    elif event.key == ord('m'): return 4
                    elif event.key == ord('h'): return 5
            pygame.display.update()