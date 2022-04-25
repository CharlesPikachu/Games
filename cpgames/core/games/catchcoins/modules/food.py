'''
Function:
    定义金币等掉落的物品
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import pygame
import random


'''定义食物类'''
class Food(pygame.sprite.Sprite):
    def __init__(self, images_dict, selected_key, screensize, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.screensize = screensize
        self.image = images_dict[selected_key]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = random.randint(20, screensize[0]-20), -10
        self.speed = random.randrange(5, 10)
        self.score = 1 if selected_key == 'gold' else 5
    '''更新食物位置'''
    def update(self):
        self.rect.bottom += self.speed
        if self.rect.top > self.screensize[1]:
            return True
        return False