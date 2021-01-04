'''
Function:
    一些工具函数
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import pygame


'''根据方格当前的分数获得[方格背景颜色, 方格里的字体颜色]'''
def getColorByNumber(number):
    number2color_dict = {
        2: ['#eee4da', '#776e65'], 4: ['#ede0c8', '#776e65'], 8: ['#f2b179', '#f9f6f2'],
        16: ['#f59563', '#f9f6f2'], 32: ['#f67c5f', '#f9f6f2'], 64: ['#f65e3b', '#f9f6f2'],
        128: ['#edcf72', '#f9f6f2'], 256: ['#edcc61', '#f9f6f2'], 512: ['#edc850', '#f9f6f2'],
        1024: ['#edc53f', '#f9f6f2'], 2048: ['#edc22e', '#f9f6f2'], 4096: ['#eee4da', '#776e65'],
        8192: ['#edc22e', '#f9f6f2'], 16384: ['#f2b179', '#776e65'], 32768: ['#f59563', '#776e65'],
        65536: ['#f67c5f', '#f9f6f2'], 'null': ['#9e948a', None]
    }
    return number2color_dict[number]


'''将2048游戏的当前数字排列画到屏幕上'''
def drawGameMatrix(screen, game_matrix, cfg):
    for i in range(len(game_matrix)):
        for j in range(len(game_matrix[i])):
            number = game_matrix[i][j]
            x = cfg.MARGIN_SIZE * (j + 1) + cfg.BLOCK_SIZE * j
            y = cfg.MARGIN_SIZE * (i + 1) + cfg.BLOCK_SIZE * i
            pygame.draw.rect(screen, pygame.Color(getColorByNumber(number)[0]), (x, y, cfg.BLOCK_SIZE, cfg.BLOCK_SIZE))
            if number != 'null':
                font_color = pygame.Color(getColorByNumber(number)[1])
                font_size = cfg.BLOCK_SIZE - 10 * len(str(number))
                font = pygame.font.Font(cfg.FONTPATH, font_size)
                text = font.render(str(number), True, font_color)
                text_rect = text.get_rect()
                text_rect.centerx, text_rect.centery = x + cfg.BLOCK_SIZE / 2, y + cfg.BLOCK_SIZE / 2
                screen.blit(text, text_rect)


'''将游戏的最高分和当前分数画到屏幕上'''
def drawScore(screen, score, max_score, cfg):
    font_color = (255, 255, 255)
    font_size = 30
    font = pygame.font.Font(cfg.FONTPATH, font_size)
    text_max_score = font.render('Best: %s' % max_score, True, font_color)
    text_score = font.render('Score: %s' % score, True, font_color)
    start_x = cfg.BLOCK_SIZE * cfg.GAME_MATRIX_SIZE[1] + cfg.MARGIN_SIZE * (cfg.GAME_MATRIX_SIZE[1] + 1)
    screen.blit(text_max_score, (start_x+10, 10))
    screen.blit(text_score, (start_x+10, 20+text_score.get_rect().height))
    start_y = 30 + text_score.get_rect().height + text_max_score.get_rect().height
    return (start_x, start_y)


'''游戏介绍'''
def drawGameIntro(screen, start_x, start_y, cfg):
    start_y += 40
    font_color = (255, 255, 255)
    font_size_big = 30
    font_size_small = 20
    font_big = pygame.font.Font(cfg.FONTPATH, font_size_big)
    font_small = pygame.font.Font(cfg.FONTPATH, font_size_small)
    intros = ['TIPS:', 'Use arrow keys to move the number blocks.', 'Adjacent blocks with the same number will', 'be merged. Just try to merge the blocks as', 'many as you can!']
    for idx, intro in enumerate(intros):
        font = font_big if idx == 0 else font_small
        text = font.render(intro, True, font_color)
        screen.blit(text, (start_x+10, start_y))
        start_y += text.get_rect().height + 10