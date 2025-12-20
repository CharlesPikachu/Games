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
    GREEN = (0, 255, 0)
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
        '1/25screenwidth': {'name': os.path.join(rootdir.replace('puzzlepieces', 'base'), 'resources/fonts/simkai.ttf'), 'size': SCREENSIZE[0] // 25},
    }
    # 限时模式设置（秒）
    TIME_LIMIT = 300  # 默认5分钟
    # 提示显示时间（毫秒）
    HINT_DURATION = 3000


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
        size, game_img_used = self.ShowStartInterface(screen)
        assert isinstance(size, int)
        num_rows, num_cols = size, size
        num_cells = size * size
        # 如果没有选择自定义图片，随机选择一张
        if not game_img_used:
            game_img_used = random.choice(list(resource_loader.images.values()))
        game_img_used = pygame.transform.scale(game_img_used, cfg.SCREENSIZE)
        game_img_used_rect = game_img_used.get_rect()
        # 计算Cell大小
        cell_width = game_img_used_rect.width // num_cols
        cell_height = game_img_used_rect.height // num_rows
        # 避免初始化为原图
        while True:
            game_board, blank_cell_idx = self.CreateBoard(num_rows, num_cols, num_cells)
            if not self.isGameOver(game_board, size):
                break
        # 游戏状态初始化
        is_running = True
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()  # 开始时间
        time_remaining = cfg.TIME_LIMIT  # 剩余时间
        steps = 0  # 步数统计
        show_hint = False  # 是否显示提示
        hint_start_time = 0  # 提示开始时间
        # 游戏主循环
        while is_running:
            # --事件捕获
            for event in pygame.event.get():
                # ----退出游戏
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    QuitGame()
                # ----键盘操作
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        new_idx = self.moveL(game_board, blank_cell_idx, num_cols)
                        if new_idx != blank_cell_idx:
                            blank_cell_idx = new_idx
                            steps += 1
                    elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                        new_idx = self.moveR(game_board, blank_cell_idx, num_cols)
                        if new_idx != blank_cell_idx:
                            blank_cell_idx = new_idx
                            steps += 1
                    elif event.key == pygame.K_UP or event.key == ord('w'):
                        new_idx = self.moveU(game_board, blank_cell_idx, num_rows, num_cols)
                        if new_idx != blank_cell_idx:
                            blank_cell_idx = new_idx
                            steps += 1
                    elif event.key == pygame.K_DOWN or event.key == ord('s'):
                        new_idx = self.moveD(game_board, blank_cell_idx, num_cols)
                        if new_idx != blank_cell_idx:
                            blank_cell_idx = new_idx
                            steps += 1
                    elif event.key == pygame.K_h:
                        show_hint = True
                        hint_start_time = pygame.time.get_ticks()
                # ----鼠标操作
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    x_pos = x // cell_width
                    y_pos = y // cell_height
                    idx = x_pos + y_pos * num_cols
                    if idx == blank_cell_idx-1:
                        new_idx = self.moveR(game_board, blank_cell_idx, num_cols)
                        if new_idx != blank_cell_idx:
                            blank_cell_idx = new_idx
                            steps += 1
                    elif idx == blank_cell_idx+1:
                        new_idx = self.moveL(game_board, blank_cell_idx, num_cols)
                        if new_idx != blank_cell_idx:
                            blank_cell_idx = new_idx
                            steps += 1
                    elif idx == blank_cell_idx+num_cols:
                        new_idx = self.moveU(game_board, blank_cell_idx, num_rows, num_cols)
                        if new_idx != blank_cell_idx:
                            blank_cell_idx = new_idx
                            steps += 1
                    elif idx == blank_cell_idx-num_cols:
                        new_idx = self.moveD(game_board, blank_cell_idx, num_cols)
                        if new_idx != blank_cell_idx:
                            blank_cell_idx = new_idx
                            steps += 1
            # --倒计时更新
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
            time_remaining = cfg.TIME_LIMIT - elapsed_time
            if time_remaining <= 0:
                # 时间到，游戏失败
                self.ShowGameOverInterface(screen, False)
                is_running = False
            # --提示显示控制
            if show_hint and (pygame.time.get_ticks() - hint_start_time) > cfg.HINT_DURATION:
                show_hint = False
            # --判断游戏是否结束
            if self.isGameOver(game_board, size):
                game_board[blank_cell_idx] = num_cells - 1
                is_running = False
                self.ShowGameOverInterface(screen, True, steps, cfg.TIME_LIMIT - time_remaining)
            # --更新屏幕
            screen.fill(cfg.BACKGROUNDCOLOR)
            # 显示拼图
            for i in range(num_cells):
                if game_board[i] == -1:
                    continue
                x_pos = i // num_cols
                y_pos = i % num_cols
                rect = pygame.Rect(y_pos*cell_width, x_pos*cell_height, cell_width, cell_height)
                img_area = pygame.Rect((game_board[i]%num_cols)*cell_width, (game_board[i]//num_cols)*cell_height, cell_width, cell_height)
                screen.blit(game_img_used, rect, img_area)
            # 显示网格线
            for i in range(num_cols+1):
                pygame.draw.line(screen, cfg.BLACK, (i*cell_width, 0), (i*cell_width, game_img_used_rect.height))
            for i in range(num_rows+1):
                pygame.draw.line(screen, cfg.BLACK, (0, i*cell_height), (game_img_used_rect.width, i*cell_height))
            # 显示游戏信息
            self.ShowGameInfo(screen, time_remaining, steps)
            # 显示提示
            if show_hint:
                self.ShowHint(screen, game_img_used)
            pygame.display.update()
            clock.tick(cfg.FPS)
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
    def ShowGameOverInterface(self, screen, is_win, steps=0, time_used=0):
        screen.fill(self.cfg.BACKGROUNDCOLOR)
        font_title = self.resource_loader.fonts['1/15screenwidth']
        font_content = self.resource_loader.fonts['1/20screenwidth']
        if is_win:
            title = font_title.render('恭喜! 你成功完成了拼图!', True, (233, 150, 122))
            content1 = font_content.render(f'用时: {time_used} 秒', True, self.cfg.BLUE)
            content2 = font_content.render(f'步数: {steps}', True, self.cfg.BLUE)
        else:
            title = font_title.render('时间到! 游戏失败!', True, self.cfg.RED)
            content1 = font_content.render('很遗憾, 你没有在规定时间内完成拼图', True, self.cfg.BLACK)
            content2 = font_content.render('按任意键退出游戏', True, self.cfg.BLACK)
        trect = title.get_rect()
        trect.midtop = (self.cfg.SCREENSIZE[0] / 2, self.cfg.SCREENSIZE[1] / 4)
        screen.blit(title, trect)
        if is_win:
            crect1 = content1.get_rect()
            crect1.midtop = (self.cfg.SCREENSIZE[0] / 2, self.cfg.SCREENSIZE[1] / 2.5)
            screen.blit(content1, crect1)
            crect2 = content2.get_rect()
            crect2.midtop = (self.cfg.SCREENSIZE[0] / 2, self.cfg.SCREENSIZE[1] / 2)
            screen.blit(content2, crect2)
        else:
            crect1 = content1.get_rect()
            crect1.midtop = (self.cfg.SCREENSIZE[0] / 2, self.cfg.SCREENSIZE[1] / 2.5)
            screen.blit(content1, crect1)
            crect2 = content2.get_rect()
            crect2.midtop = (self.cfg.SCREENSIZE[0] / 2, self.cfg.SCREENSIZE[1] / 2)
            screen.blit(content2, crect2)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    QuitGame()
                elif event.type == pygame.KEYDOWN:
                    if not is_win:
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
        content3 = cfont.render('按U键上传自定义图片', True, self.cfg.GREEN)
        trect = title.get_rect()
        trect.midtop = (self.cfg.SCREENSIZE[0] / 2, self.cfg.SCREENSIZE[1] / 10)
        crect1 = content1.get_rect()
        crect1.midtop = (self.cfg.SCREENSIZE[0] / 2, self.cfg.SCREENSIZE[1] / 2.5)
        crect2 = content2.get_rect()
        crect2.midtop = (self.cfg.SCREENSIZE[0] / 2, self.cfg.SCREENSIZE[1] / 2)
        crect3 = content3.get_rect()
        crect3.midtop = (self.cfg.SCREENSIZE[0] / 2, self.cfg.SCREENSIZE[1] / 1.6)
        screen.blit(title, trect)
        screen.blit(content1, crect1)
        screen.blit(content2, crect2)
        screen.blit(content3, crect3)
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    QuitGame()
                elif event.type == pygame.KEYDOWN:
                    if event.key == ord('l'): return 3, None
                    elif event.key == ord('m'): return 4, None
                    elif event.key == ord('h'): return 5, None
                    elif event.key == ord('u') or event.key == ord('U'):
                        import tkinter as tk
                        from tkinter import filedialog
                        root = tk.Tk()
                        root.withdraw()
                        file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.jpg *.jpeg *.png *.bmp')])
                        if file_path:
                            custom_img = pygame.image.load(file_path)
                            size = self.SelectDifficulty(screen)
                            return size, custom_img
            pygame.display.update()
    '''选择难度'''
    def SelectDifficulty(self, screen):
        screen.fill(self.cfg.BACKGROUNDCOLOR)
        tfont = self.resource_loader.fonts['1/4screenwidth']
        cfont = self.resource_loader.fonts['1/20screenwidth']
        title = tfont.render('选择难度', True, self.cfg.RED)
        content1 = cfont.render('按H或M或L键选择', True, self.cfg.BLUE)
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
    '''显示游戏信息'''
    def ShowGameInfo(self, screen, time_remaining, steps):
        font = self.resource_loader.fonts['1/25screenwidth']
        time_text = font.render(f'剩余时间: {time_remaining} 秒', True, self.cfg.RED)
        steps_text = font.render(f'步数: {steps}', True, self.cfg.BLUE)
        hint_text = font.render('按H键显示提示', True, self.cfg.GREEN)
        screen.blit(time_text, (10, 10))
        screen.blit(steps_text, (10, 40))
        screen.blit(hint_text, (10, 70))
    '''显示提示'''
    def ShowHint(self, screen, game_img):
        # 创建半透明表面
        hint_surface = pygame.Surface(self.cfg.SCREENSIZE, pygame.SRCALPHA)
        hint_surface.fill((255, 255, 255, 128))
        screen.blit(hint_surface, (0, 0))
        # 显示原图
        screen.blit(game_img, (0, 0))
        # 添加提示文字
        font = self.resource_loader.fonts['1/15screenwidth']
        hint_text = font.render('提示', True, self.cfg.RED)
        text_rect = hint_text.get_rect(center=(self.cfg.SCREENSIZE[0]/2, self.cfg.SCREENSIZE[1]-50))
        screen.blit(hint_text, text_rect)