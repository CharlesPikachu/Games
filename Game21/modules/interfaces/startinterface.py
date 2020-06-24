'''
Function:
    定义游戏开始界面
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import pygame


'''游戏开始界面'''
def startInterface(screen, begin_image_paths):
    begin_images = [pygame.image.load(begin_image_paths[0]), pygame.image.load(begin_image_paths[1])]
    begin_image = begin_images[0]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] in list(range(419, 574)) and mouse_pos[1] in list(range(374, 416)):
                    begin_image = begin_images[1]
                else:
                    begin_image = begin_images[0]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1 and mouse_pos[0] in list(range(419, 574)) and mouse_pos[1] in list(range(374, 416)):
                    return True
        screen.blit(begin_image, (0, 0))
        pygame.display.update()