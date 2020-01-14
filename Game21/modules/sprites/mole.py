'''
Function:
    地鼠
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import pygame


'''地鼠'''
class Mole(pygame.sprite.Sprite):
    def __init__(self, image_paths, position, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.transform.scale(pygame.image.load(image_paths[0]), (101, 103)), 
                       pygame.transform.scale(pygame.image.load(image_paths[-1]), (101, 103))]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.setPosition(position)
        self.is_hammer = False
    '''设置位置'''
    def setPosition(self, pos):
        self.rect.left, self.rect.top = pos
    '''设置被击中'''
    def setBeHammered(self):
        self.is_hammer = True
    '''显示在屏幕上'''
    def draw(self, screen):
        if self.is_hammer: self.image = self.images[1]
        screen.blit(self.image, self.rect)
    '''重置'''
    def reset(self):
        self.image = self.images[0]
        self.is_hammer = False