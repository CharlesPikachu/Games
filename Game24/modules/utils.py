'''
Function:
    定义一些工具函数
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import pygame


'''画游戏网格'''
def drawGameGrid(cfg, screen):
    color = (40, 40, 40)
    for x in range(0, cfg.SCREENSIZE[0], cfg.BLOCK_SIZE):
        pygame.draw.line(screen, color, (x, 0), (x, cfg.SCREENSIZE[1]))
    for y in range(0, cfg.SCREENSIZE[1], cfg.BLOCK_SIZE):
        pygame.draw.line(screen, color, (0, y), (cfg.SCREENSIZE[0], y))


'''显示得分'''
def showScore(cfg, score, screen):
    color = (255, 255, 255)
    font = pygame.font.Font(cfg.FONTPATH, 30)
    text = font.render('Score: %s' % score, True, color)
    rect = text.get_rect()
    rect.topleft = (10, 10)
    screen.blit(text, rect)