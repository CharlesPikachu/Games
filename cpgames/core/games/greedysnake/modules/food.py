'''
Function:
    定义食物类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import random
import pygame


'''食物类'''
class Apple(pygame.sprite.Sprite):
    def __init__(self, cfg, snake_coords, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.cfg = cfg
        while True:
            self.coord = [random.randint(0, cfg.GAME_MATRIX_SIZE[0]-1), random.randint(0, cfg.GAME_MATRIX_SIZE[1]-1)]
            if self.coord not in snake_coords:
                break
        self.color = (255, 0, 0)
    '''画到屏幕上'''
    def draw(self, screen):
        cx, cy = int((self.coord[0] + 0.5) * self.cfg.BLOCK_SIZE), int((self.coord[1] + 0.5) * self.cfg.BLOCK_SIZE)
        pygame.draw.circle(screen, self.color, (cx, cy), self.cfg.BLOCK_SIZE//2-2)