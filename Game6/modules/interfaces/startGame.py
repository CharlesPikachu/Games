'''
Function:
    游戏开始界面
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import pygame
import itertools


'''显示开始界面'''
def startGame(screen, sounds, bird_images, other_images, backgroud_image, cfg):
    base_pos = [0, cfg.SCREENHEIGHT*0.79]
    base_diff_bg = other_images['base'].get_width() - backgroud_image.get_width()
    msg_pos = [(cfg.SCREENWIDTH-other_images['message'].get_width())/2, cfg.SCREENHEIGHT*0.12]
    bird_idx = 0
    bird_idx_change_count = 0
    bird_idx_cycle = itertools.cycle([0, 1, 2, 1])
    bird_pos = [cfg.SCREENWIDTH*0.2, (cfg.SCREENHEIGHT-list(bird_images.values())[0].get_height())/2]
    bird_y_shift_count = 0
    bird_y_shift_max = 9
    shift = 1
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    return {'bird_pos': bird_pos, 'base_pos': base_pos, 'bird_idx': bird_idx}
        sounds['wing'].play()
        bird_idx_change_count += 1
        if bird_idx_change_count % 5 == 0:
            bird_idx = next(bird_idx_cycle)
            bird_idx_change_count = 0
        base_pos[0] = -((-base_pos[0] + 4) % base_diff_bg)
        bird_y_shift_count += 1
        if bird_y_shift_count == bird_y_shift_max:
            bird_y_shift_max = 16
            shift = -1 * shift
            bird_y_shift_count = 0
        bird_pos[-1] = bird_pos[-1] + shift
        screen.blit(backgroud_image, (0, 0))
        screen.blit(list(bird_images.values())[bird_idx], bird_pos)
        screen.blit(other_images['message'], msg_pos)
        screen.blit(other_images['base'], base_pos)
        pygame.display.update()
        clock.tick(cfg.FPS)