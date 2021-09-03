'''
Function:
    魔塔小游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import cfg
import pygame
from modules import *


'''游戏主程序'''
def main(cfg):
    # 初始化
    pygame.init()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('魔塔 —— Charles的皮卡丘')
    # 开始界面
    sg_interface = StartGameInterface(cfg)
    sg_interface.run(screen)
    # 游戏进行中界面
    game_client = GameLevels(cfg)
    game_client.run(screen)


'''run'''
if __name__ == '__main__':
    main(cfg)