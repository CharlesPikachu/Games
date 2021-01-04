'''
Function:
    定义开始和结束界面
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import pygame


'''定义按钮'''
def Button(screen, position, text, cfg):
    bwidth = 310
    bheight = 65
    left, top = position
    pygame.draw.line(screen, (150, 150, 150), (left, top), (left+bwidth, top), 5)
    pygame.draw.line(screen, (150, 150, 150), (left, top - 2), (left, top + bheight), 5)
    pygame.draw.line(screen, (50, 50, 50), (left, top + bheight), (left + bwidth, top + bheight), 5)
    pygame.draw.line(screen, (50, 50, 50), (left + bwidth, top + bheight), (left + bwidth, top), 5)
    pygame.draw.rect(screen, (100, 100, 100), (left, top, bwidth, bheight))
    font = pygame.font.Font(cfg.FONTPATH, 50)
    text_render = font.render(text, 1, (255, 0, 0))
    return screen.blit(text_render, (left + 50, top + 10))


'''开始界面'''
def StartInterface(screen, cfg):
    clock = pygame.time.Clock()
    while True:
        button_1 = Button(screen, (330, 190), '单人模式', cfg)
        button_2 = Button(screen, (330, 305), '双人模式', cfg)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_1.collidepoint(pygame.mouse.get_pos()):
                    return 1
                elif button_2.collidepoint(pygame.mouse.get_pos()):
                    return 2
        clock.tick(60)
        pygame.display.update()


'''结束界面'''
def EndInterface(screen, cfg):
    clock = pygame.time.Clock()
    while True:
        button_1 = Button(screen, (330, 190), '重新开始', cfg)
        button_2 = Button(screen, (330, 305), '退出游戏', cfg)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_1.collidepoint(pygame.mouse.get_pos()):
                    return
                elif button_2.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
        clock.tick(60)
        pygame.display.update()