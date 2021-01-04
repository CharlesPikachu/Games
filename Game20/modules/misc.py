'''
Function:
    定义其他必要模块
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import pygame


'''在屏幕指定位置显示文字'''
def showText(screen, font, text, color, position):
    text_render = font.render(text, True, color)
    rect = text_render.get_rect()
    rect.left, rect.top = position
    screen.blit(text_render, rect)
    return rect.right


'''按钮'''
def Button(screen, position, text, font, buttoncolor=(120, 120, 120), linecolor=(20, 20, 20), textcolor=(255, 255, 255), bwidth=200, bheight=50):
    left, top = position
    pygame.draw.line(screen, linecolor, (left, top), (left+bwidth, top), 5)
    pygame.draw.line(screen, linecolor, (left, top-2), (left, top+bheight), 5)
    pygame.draw.line(screen, linecolor, (left, top+bheight), (left+bwidth, top+bheight), 5)
    pygame.draw.line(screen, linecolor, (left+bwidth, top+bheight), (left+bwidth, top), 5)
    pygame.draw.rect(screen, buttoncolor, (left, top, bwidth, bheight))
    text_render = font.render(text, 1, textcolor)
    rect = text_render.get_rect()
    rect.centerx, rect.centery = left + bwidth / 2, top + bheight / 2
    return screen.blit(text_render, rect)


'''游戏开始/关卡切换/游戏结束界面'''
def Interface(screen, cfg, mode='game_start'):
    pygame.display.set_mode(cfg.SCREENSIZE)
    font = pygame.font.SysFont('Consolas', 30)
    if mode == 'game_start':
        clock = pygame.time.Clock()
        while True:
            screen.fill((192, 192, 192))
            button_1 = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//3), 'START', font)
            button_2 = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//2), 'QUIT', font)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(-1)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_1.collidepoint(pygame.mouse.get_pos()):
                        return True
                    elif button_2.collidepoint(pygame.mouse.get_pos()):
                        pygame.quit()
                        sys.exit(-1)
            pygame.display.update()
            clock.tick(cfg.FPS)
    elif mode == 'game_switch':
        clock = pygame.time.Clock()
        while True:
            screen.fill((192, 192, 192))
            button_1 = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//3), 'NEXT', font)
            button_2 = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//2), 'QUIT', font)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(-1)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_1.collidepoint(pygame.mouse.get_pos()):
                        return True
                    elif button_2.collidepoint(pygame.mouse.get_pos()):
                        pygame.quit()
                        sys.exit(-1)
            pygame.display.update()
            clock.tick(cfg.FPS)
    elif mode == 'game_end':
        clock = pygame.time.Clock()
        while True:
            screen.fill((192, 192, 192))
            button_1 = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//3), 'RESTART', font)
            button_2 = Button(screen, ((cfg.SCREENSIZE[0]-200)//2, cfg.SCREENSIZE[1]//2), 'QUIT', font)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(-1)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_1.collidepoint(pygame.mouse.get_pos()):
                        return True
                    elif button_2.collidepoint(pygame.mouse.get_pos()):
                        pygame.quit()
                        sys.exit(-1)
            pygame.display.update()
            clock.tick(cfg.FPS)
    else:
        raise ValueError('Interface.mode unsupport %s...' % mode)