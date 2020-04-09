'''
Function:
    游戏结束界面
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import pygame


'''游戏结束界面'''
def endInterface(screen, cfg):
    font_size_big = 60
    font_size_small = 30
    font_color = (255, 255, 255)
    font_big = pygame.font.Font(cfg.FONTPATH, font_size_big)
    font_small = pygame.font.Font(cfg.FONTPATH, font_size_small)
    surface = screen.convert_alpha()
    surface.fill((127, 255, 212, 2))
    text = font_big.render('Game Over!', True, font_color)
    text_rect = text.get_rect()
    text_rect.centerx, text_rect.centery = cfg.SCREENSIZE[0]/2, cfg.SCREENSIZE[1]/2-50
    surface.blit(text, text_rect)
    button_width, button_height = 100, 40
    button_start_x_left = cfg.SCREENSIZE[0] / 2 - button_width - 20
    button_start_x_right = cfg.SCREENSIZE[0] / 2 + 20
    button_start_y = cfg.SCREENSIZE[1] / 2 - button_height / 2 + 20
    pygame.draw.rect(surface, (0, 255, 255), (button_start_x_left, button_start_y, button_width, button_height))
    text_restart = font_small.render('Restart', True, font_color)
    text_restart_rect = text_restart.get_rect()
    text_restart_rect.centerx, text_restart_rect.centery = button_start_x_left + button_width / 2, button_start_y + button_height / 2
    surface.blit(text_restart, text_restart_rect)
    pygame.draw.rect(surface, (0, 255, 255), (button_start_x_right, button_start_y, button_width, button_height))
    text_quit = font_small.render('Quit', True, font_color)
    text_quit_rect = text_quit.get_rect()
    text_quit_rect.centerx, text_quit_rect.centery = button_start_x_right + button_width / 2, button_start_y + button_height / 2
    surface.blit(text_quit, text_quit_rect)
    while True:
        screen.blit(surface, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button:
                if text_quit_rect.collidepoint(pygame.mouse.get_pos()):
                    return False
                if text_restart_rect.collidepoint(pygame.mouse.get_pos()):
                    return True
        pygame.display.update()