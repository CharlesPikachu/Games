'''
Function:
    愤怒的小鸟小游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import cfg
import pygame
from modules import *


'''游戏主程序'''
def main(cfg):
    # 初始化
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(cfg.BGMPATH)
    pygame.mixer.music.play(-1, 0.0)
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('Angry Birds —— Charles的皮卡丘')
    # 开始游戏
    def startgame():
        game_levels = GameLevels(cfg, screen)
        game_levels.start()
    # 退出游戏
    def quitgame():
        pygame.quit()
        sys.exit()
    # 开始界面
    components = pygame.sprite.Group()
    title_label = Label(screen, 700, 100, 400, 200)
    title_label.addtext('ANGRY BIRDS', 80, cfg.FONTPATH['arfmoochikncheez'], (236, 240, 241))
    components.add(title_label)
    start_btn = Button(screen, 500, 400, 300, 100, startgame, (244, 208, 63), (247, 220, 111))
    start_btn.addtext('START GAME', 60, cfg.FONTPATH['arfmoochikncheez'], cfg.BACKGROUND_COLOR)
    components.add(start_btn)
    quit_btn = Button(screen, 1000, 400, 300, 100, quitgame, (241, 148, 138), (245, 183, 177))
    quit_btn.addtext('QUIT', 60, cfg.FONTPATH['arfmoochikncheez'], cfg.BACKGROUND_COLOR)
    components.add(quit_btn)
    charles_label = Label(screen, cfg.SCREENSIZE[0] - 300, cfg.SCREENSIZE[1] - 80, 300, 100)
    charles_label.addtext('CHARLES', 60, cfg.FONTPATH['arfmoochikncheez'], (41, 41, 41))
    components.add(charles_label)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quitgame()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.selected():
                    start_btn.action()
                elif quit_btn.selected():
                    quit_btn.action()
        screen.fill(cfg.BACKGROUND_COLOR)
        for component in components: component.draw()
        pygame.display.update()
        clock.tick(cfg.FPS)


'''run'''
if __name__ == '__main__':
    main(cfg)