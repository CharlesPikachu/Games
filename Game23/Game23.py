'''
Function:
    2048小游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import cfg
import sys
import pygame
from modules import *


'''主程序'''
def main(cfg):
    # 游戏初始化
    pygame.init()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('2048 —— Charles的皮卡丘')
    # 播放背景音乐
    pygame.mixer.music.load(cfg.BGMPATH)
    pygame.mixer.music.play(-1)
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
                pygame.quit()
                sys.exit()
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
    return endInterface(screen, cfg)


'''run'''
if __name__ == '__main__':
    while True:
        if not main(cfg):
            break