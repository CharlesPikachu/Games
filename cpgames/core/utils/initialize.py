'''
Function:
    游戏初始化相关的工具
Author: 
    Charles
微信公众号: 
    Charles的皮卡丘
'''
import pygame


'''基于pygame的游戏初始化'''
def InitPygame(screensize, title='微信公众号: Charles的皮卡丘', init_mixer=True):
    pygame.init()
    if init_mixer: pygame.mixer.init()
    screen = pygame.display.set_mode(screensize)
    pygame.display.set_caption(title)
    return screen