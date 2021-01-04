'''
Function:
    定义工具函数
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import pygame


'''显示字'''
def showText(screen, text, color, font, x, y):
    text = font.render(text, True, color)
    screen.blit(text, (x, y))


'''显示与生命值等数量的飞船(右上角)'''
def showLife(screen, num_life, color):
    cell = [2, 2]
    num_cols = 15
    filled_cells = [7,21,22,23,36,37,38,46,47,48,49,50,51,52,53,54,55,56,57,58,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119]
    for i in range(num_life):
        position = [750 - 35 * i, 8]
        for i in range(0, len(filled_cells)):
            y = filled_cells[i] // num_cols
            x = filled_cells[i] % num_cols
            rect = [x * cell[0] + position[0], y * cell[1] + position[1], cell[0], cell[1]]
            pygame.draw.rect(screen, color, rect)


'''结束界面'''
def endInterface(screen, color, is_win):
    screen.fill(color)
    clock = pygame.time.Clock()
    if is_win:
        text = 'VICTORY'
    else:
        text = 'FAILURE'
    font = pygame.font.SysFont('arial', 30)
    text_render = font.render(text, 1, (255, 255, 255))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame.KEYDOWN) or (event.type == pygame.MOUSEBUTTONDOWN):
                return
        screen.blit(text_render, (350, 300))
        clock.tick(60)
        pygame.display.update()