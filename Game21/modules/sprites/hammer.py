'''
Function:
    定义锤子
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import pygame


'''锤子类'''
class Hammer(pygame.sprite.Sprite):
    def __init__(self, image_paths, position, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(image_paths[0]), pygame.image.load(image_paths[1])]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.images[1])
        self.rect.left, self.rect.top = position
        # 用于显示锤击时的特效
        self.hammer_count = 0
        self.hammer_last_time = 4
        self.is_hammering = False
    '''设置位置'''
    def setPosition(self, pos):
        self.rect.centerx, self.rect.centery = pos
    '''设置hammering'''
    def setHammering(self):
        self.is_hammering = True
    '''显示在屏幕上'''
    def draw(self, screen):
        if self.is_hammering:
            self.image = self.images[1]
            self.hammer_count += 1
            if self.hammer_count > self.hammer_last_time:
                self.is_hammering = False
                self.hammer_count = 0
        else:
            self.image = self.images[0]
        screen.blit(self.image, self.rect)