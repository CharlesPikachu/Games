'''
Function:
    其他工具函数
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import pygame


'''退出程序'''
def QuitGame(use_pygame=True):
    if use_pygame: pygame.quit()
    sys.exit()