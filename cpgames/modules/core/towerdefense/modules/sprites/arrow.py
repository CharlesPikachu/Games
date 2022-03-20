'''
Function:
    箭类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import math
import random
import pygame


'''箭类'''
class Arrow(pygame.sprite.Sprite):
    def __init__(self, arrow_type, cfg, resource_loader):
        assert arrow_type in range(3)
        pygame.sprite.Sprite.__init__(self)
        self.arrow_type = arrow_type
        self.images = [resource_loader.images['game']['arrow1'], resource_loader.images['game']['arrow2'], resource_loader.images['game']['arrow3']]
        self.image = self.images[arrow_type]
        self.rect = self.image.get_rect()
        self.position = 0, 0
        self.rect.left, self.rect.top = self.position
        # 与水平向左的直线所成的夹角, 顺时针为正
        self.angle = 0
        if arrow_type == 0:
            self.speed = 4
            self.attack_power = 5
        elif arrow_type == 1:
            self.speed = 5
            self.attack_power = 10
        elif arrow_type == 2:
            self.speed = 7
            self.attack_power = 15
    '''不停移动'''
    def move(self):
        self.position = self.position[0] - self.speed * math.cos(self.angle), self.position[1] - self.speed * math.sin(self.angle)
        self.rect.left, self.rect.top = self.position
    '''重置箭的位置'''
    def reset(self, position, angle=None):
        if angle is None:
            angle = random.random() * math.pi * 2
        self.position = position
        self.angle = angle
        self.image = pygame.transform.rotate(self.image, -(self.angle / math.pi) * 180 + 90)
        self.rect = self.image.get_rect()