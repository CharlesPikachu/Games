'''
Function:
    扫雷小游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import cfg
import sys
import time
import pygame
from modules import *


'''主函数'''
def main():
    # 游戏初始化
    pygame.init()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('mine sweeper —— Charles的皮卡丘')
    # 导入所有图片
    images = {}
    for key, value in cfg.IMAGE_PATHS.items():
        if key in ['face_fail', 'face_normal', 'face_success']:
            image = pygame.image.load(value)
            images[key] = pygame.transform.smoothscale(image, (int(cfg.GRIDSIZE*1.25), int(cfg.GRIDSIZE*1.25)))
        else:
            image = pygame.image.load(value).convert()
            images[key] = pygame.transform.smoothscale(image, (cfg.GRIDSIZE, cfg.GRIDSIZE))
    # 载入字体
    font = pygame.font.Font(cfg.FONT_PATH, cfg.FONT_SIZE)
    # 导入并播放背景音乐
    pygame.mixer.music.load(cfg.BGM_PATH)
    pygame.mixer.music.play(-1)
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
                pygame.quit()
                sys.exit()
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


'''run'''
if __name__ == '__main__':
    main()