'''
Function:
    塔防游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import cfg
import pygame
from modules import *


'''主函数'''
def main():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(cfg.AUDIOPATHS['bgm'])
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.25)
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption("塔防游戏 —— Charles的皮卡丘")
    # 调用游戏开始界面
    start_interface = StartInterface(cfg)
    is_play = start_interface.update(screen)
    if not is_play:
        return
    # 调用游戏界面
    while True:
        choice_interface = ChoiceInterface(cfg)
        map_choice, difficulty_choice = choice_interface.update(screen)
        game_interface = GamingInterface(cfg)
        game_interface.start(screen, map_path=cfg.MAPPATHS[str(map_choice)], difficulty_path=cfg.DIFFICULTYPATHS[str(difficulty_choice)])
        end_interface = EndInterface(cfg)
        end_interface.update(screen)


'''run'''
if __name__ == '__main__':
    main()