'''
Function:
    游戏结束界面
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import pygame
from .....utils import QuitGame


'''游戏结束界面'''
def GameEndInterface(screen, cfg, resource_loader):
    replay_image = resource_loader.images['replay']
    replay_image = pygame.transform.scale(replay_image, (35, 31))
    replay_image_rect = replay_image.get_rect()
    replay_image_rect.centerx = cfg.SCREENSIZE[0] / 2
    replay_image_rect.top = cfg.SCREENSIZE[1] * 0.52
    gameover_image = resource_loader.images['gameover']
    gameover_image = pygame.transform.scale(gameover_image, (190, 11))
    gameover_image_rect = gameover_image.get_rect()
    gameover_image_rect.centerx = cfg.SCREENSIZE[0] / 2
    gameover_image_rect.centery = cfg.SCREENSIZE[1] * 0.35
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                QuitGame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if replay_image_rect.collidepoint(mouse_pos):
                    return True
        screen.blit(replay_image, replay_image_rect)
        screen.blit(gameover_image, gameover_image_rect)
        pygame.display.update()
        clock.tick(cfg.FPS)