'''
Function:
    定义游戏结束界面
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import pygame


'''结束界面'''
def endInterface(screen, end_image_path, again_image_paths, score_info, font_path, font_colors, screensize):
    end_image = pygame.image.load(end_image_path)
    again_images = [pygame.image.load(again_image_paths[0]), pygame.image.load(again_image_paths[1])]
    again_image = again_images[0]
    font = pygame.font.Font(font_path, 50)
    your_score_text = font.render('Your Score: %s' % score_info['your_score'], True, font_colors[0])
    your_score_rect = your_score_text.get_rect()
    your_score_rect.left, your_score_rect.top = (screensize[0] - your_score_rect.width) / 2, 215
    best_score_text = font.render('Best Score: %s' % score_info['best_score'], True, font_colors[1])
    best_score_rect = best_score_text.get_rect()
    best_score_rect.left, best_score_rect.top = (screensize[0] - best_score_rect.width) / 2, 275
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] in list(range(419, 574)) and mouse_pos[1] in list(range(374, 416)):
                    again_image = again_images[1]
                else:
                    again_image = again_images[0]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1 and mouse_pos[0] in list(range(419, 574)) and mouse_pos[1] in list(range(374, 416)):
                    return True
        screen.blit(end_image, (0, 0))
        screen.blit(again_image, (416, 370))
        screen.blit(your_score_text, your_score_rect)
        screen.blit(best_score_text, best_score_rect)
        pygame.display.update()