'''
Function:
    定义游戏开始/结束界面
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import pygame
from ....utils import QuitGame


'''定义按钮'''
def Button(screen, position, text, cfg, resource_loader):
    bwidth = 310
    bheight = 65
    left, top = position
    pygame.draw.line(screen, (150, 150, 150), (left, top), (left + bwidth, top), 5)
    pygame.draw.line(screen, (150, 150, 150), (left, top - 2), (left, top + bheight), 5)
    pygame.draw.line(screen, (50, 50, 50), (left, top + bheight), (left + bwidth, top + bheight), 5)
    pygame.draw.line(screen, (50, 50, 50), (left + bwidth, top + bheight), [left + bwidth, top], 5)
    pygame.draw.rect(screen, (100, 100, 100), (left, top, bwidth, bheight))
    font = resource_loader.fonts['default_50']
    text_render = font.render(text, 1, (255, 0, 0))
    return screen.blit(text_render, (left + 50, top + 10))


'''开始界面'''
def startInterface(screen, cfg, resource_loader):
    screen.fill(cfg.BACKGROUNDCOLOR)
    clock = pygame.time.Clock()
    while True:
        button_1 = Button(screen, (95, 150), '开始游戏', cfg, resource_loader)
        button_2 = Button(screen, (95, 305), '退出游戏', cfg, resource_loader)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_1.collidepoint(pygame.mouse.get_pos()):
                    return
                elif button_2.collidepoint(pygame.mouse.get_pos()):
                    QuitGame()
        clock.tick(cfg.FPS)
        pygame.display.update()


'''结束界面'''
def endInterface(screen, cfg, resource_loader):
    screen.fill(cfg.BACKGROUNDCOLOR)
    clock = pygame.time.Clock()
    text = '机智如你~恭喜通关!'
    font = resource_loader.fonts['default_30']
    text_render = font.render(text, 1, (255, 255, 255))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
        screen.blit(text_render, (120, 200))
        clock.tick(cfg.FPS)
        pygame.display.update()


'''关卡切换界面'''
def switchInterface(screen, cfg, resource_loader):
    screen.fill(cfg.BACKGROUNDCOLOR)
    clock = pygame.time.Clock()
    while True:
        button_1 = Button(screen, (95, 150), '进入下关', cfg, resource_loader)
        button_2 = Button(screen, (95, 305), '退出游戏', cfg, resource_loader)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_1.collidepoint(pygame.mouse.get_pos()):
                    return
                elif button_2.collidepoint(pygame.mouse.get_pos()):
                    QuitGame()
        clock.tick(cfg.FPS)
        pygame.display.update()