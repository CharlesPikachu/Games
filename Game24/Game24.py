'''
Function:
    贪吃蛇小游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import cfg
import sys
import pygame
from modules import *


'''主函数'''
def main(cfg):
    # 游戏初始化
    pygame.init()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('Greedy Snake —— Charles的皮卡丘')
    clock = pygame.time.Clock()
    # 播放背景音乐
    pygame.mixer.music.load(cfg.BGMPATH)
    pygame.mixer.music.play(-1)
    # 游戏主循环
    snake = Snake(cfg)
    apple = Apple(cfg, snake.coords)
    score = 0
    while True:
        screen.fill(cfg.BLACK)
        # --按键检测
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    snake.setDirection({pygame.K_UP: 'up', pygame.K_DOWN: 'down', pygame.K_LEFT: 'left', pygame.K_RIGHT: 'right'}[event.key])
        # --更新贪吃蛇和食物
        if snake.update(apple):
            apple = Apple(cfg, snake.coords)
            score += 1
        # --判断游戏是否结束
        if snake.isgameover: break
        # --显示游戏里必要的元素
        drawGameGrid(cfg, screen)
        snake.draw(screen)
        apple.draw(screen)
        showScore(cfg, score, screen)
        # --屏幕更新
        pygame.display.update()
        clock.tick(cfg.FPS)
    return endInterface(screen, cfg)


'''run'''
if __name__ == '__main__':
    while True:
        if not main(cfg):
            break