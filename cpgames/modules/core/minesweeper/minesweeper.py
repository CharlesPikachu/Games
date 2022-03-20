'''
Function:
    扫雷小游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import time
import pygame
from ...utils import QuitGame
from ..base import PygameBaseGame
from .modules import Mine, TextBoard, MinesweeperMap, EmojiButton


'''配置类'''
class Config():
    # 根目录
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # 定义一些颜色
    BACKGROUND_COLOR = (225, 225, 225)
    RED = (200, 0, 0)
    # FPS
    FPS = 60
    # 屏幕大小
    GRIDSIZE = 20
    NUM_MINES = 99
    GAME_MATRIX_SIZE = (30, 16)
    BORDERSIZE = 5
    SCREENSIZE = (GAME_MATRIX_SIZE[0] * GRIDSIZE + BORDERSIZE * 2, (GAME_MATRIX_SIZE[1] + 2) * GRIDSIZE + BORDERSIZE)
    # 标题
    TITLE = '扫雷小游戏 —— Charles的皮卡丘'
    # 背景音乐路径
    BGM_PATH = os.path.join(rootdir, 'resources/audios/bgm.mp3')
    # 字体路径
    FONT_PATHS_DICT = {
        'default': {'name': os.path.join(rootdir, 'resources/fonts/font.ttf'), 'size': 40},
    }
    # 游戏图片路径
    IMAGE_PATHS_DICT = {
        '0': os.path.join(rootdir, 'resources/images/0.bmp'),
        '1': os.path.join(rootdir, 'resources/images/1.bmp'),
        '2': os.path.join(rootdir, 'resources/images/2.bmp'),
        '3': os.path.join(rootdir, 'resources/images/3.bmp'),
        '4': os.path.join(rootdir, 'resources/images/4.bmp'),
        '5': os.path.join(rootdir, 'resources/images/5.bmp'),
        '6': os.path.join(rootdir, 'resources/images/6.bmp'),
        '7': os.path.join(rootdir, 'resources/images/7.bmp'),
        '8': os.path.join(rootdir, 'resources/images/8.bmp'),
        'ask': os.path.join(rootdir, 'resources/images/ask.bmp'),
        'blank': os.path.join(rootdir, 'resources/images/blank.bmp'),
        'blood': os.path.join(rootdir, 'resources/images/blood.bmp'),
        'error': os.path.join(rootdir, 'resources/images/error.bmp'),
        'face_fail': os.path.join(rootdir, 'resources/images/face_fail.png'),
        'face_normal': os.path.join(rootdir, 'resources/images/face_normal.png'),
        'face_success': os.path.join(rootdir, 'resources/images/face_success.png'),
        'flag': os.path.join(rootdir, 'resources/images/flag.bmp'),
        'mine': os.path.join(rootdir, 'resources/images/mine.bmp')
    }


'''扫雷小游戏'''
class MineSweeperGame(PygameBaseGame):
    game_type = 'minesweeper'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(MineSweeperGame, self).__init__(config=self.cfg, **kwargs)
    '''运行游戏'''
    def run(self):
        # 初始化
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
        # 所有图片
        images = resource_loader.images
        for key, image in images.items():
            if key in ['face_fail', 'face_normal', 'face_success']:
                images[key] = pygame.transform.smoothscale(image, (int(cfg.GRIDSIZE*1.25), int(cfg.GRIDSIZE*1.25)))
            else:
                image = image.convert()
                images[key] = pygame.transform.smoothscale(image, (cfg.GRIDSIZE, cfg.GRIDSIZE))
        # 字体
        font = resource_loader.fonts['default']
        # 播放背景音乐
        resource_loader.playbgm()
        # 实例化游戏地图
        minesweeper_map = MinesweeperMap(cfg, images)
        position = (cfg.SCREENSIZE[0] - int(cfg.GRIDSIZE * 1.25)) // 2, (cfg.GRIDSIZE * 2 - int(cfg.GRIDSIZE * 1.25)) // 2
        emoji_button = EmojiButton(images, position=position)
        fontsize = font.size(str(cfg.NUM_MINES))
        remaining_mine_board = TextBoard(str(cfg.NUM_MINES), font, (30, (cfg.GRIDSIZE*2-fontsize[1])//2-2), cfg.RED)
        fontsize = font.size('000')
        time_board = TextBoard('000', font, (cfg.SCREENSIZE[0]-30-fontsize[0], (cfg.GRIDSIZE*2-fontsize[1])//2-2), cfg.RED)
        time_board.is_start = False
        # 游戏主循环
        clock = pygame.time.Clock()
        while True:
            screen.fill(cfg.BACKGROUND_COLOR)
            # --按键检测
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    mouse_pressed = pygame.mouse.get_pressed()
                    minesweeper_map.update(mouse_pressed=mouse_pressed, mouse_pos=mouse_pos, type_='down')
                elif event.type == pygame.MOUSEBUTTONUP:
                    minesweeper_map.update(type_='up')
                    if emoji_button.rect.collidepoint(pygame.mouse.get_pos()):
                        minesweeper_map = MinesweeperMap(cfg, images)
                        time_board.update('000')
                        time_board.is_start = False
                        remaining_mine_board.update(str(cfg.NUM_MINES))
                        emoji_button.setstatus(status_code=0)
            # --更新时间显示
            if minesweeper_map.gaming:
                if not time_board.is_start:
                    start_time = time.time()
                    time_board.is_start = True
                time_board.update(str(int(time.time() - start_time)).zfill(3))
            # --更新剩余雷的数目显示
            remianing_mines = max(cfg.NUM_MINES - minesweeper_map.flags, 0)
            remaining_mine_board.update(str(remianing_mines).zfill(2))
            # --更新表情
            if minesweeper_map.status_code == 1:
                emoji_button.setstatus(status_code=1)
            if minesweeper_map.openeds + minesweeper_map.flags == cfg.GAME_MATRIX_SIZE[0] * cfg.GAME_MATRIX_SIZE[1]:
                minesweeper_map.status_code = 1
                emoji_button.setstatus(status_code=2)
            # --显示当前的游戏状态地图
            minesweeper_map.draw(screen)
            emoji_button.draw(screen)
            remaining_mine_board.draw(screen)
            time_board.draw(screen)
            # --更新屏幕
            pygame.display.update()
            clock.tick(cfg.FPS)