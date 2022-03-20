'''
Function:
    定义游戏精灵类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import math
import pygame


'''定义兔子类'''
class BunnySprite(pygame.sprite.Sprite):
    def __init__(self, image, position, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 5
        self.rotated_position = position
    '''移动兔子'''
    def move(self, screensize, direction):
        if direction == 'left':
            self.rect.left = max(self.rect.left-self.speed, 0)
        elif direction == 'right':
            self.rect.left = min(self.rect.left+self.speed, screensize[0])
        elif direction == 'up':
            self.rect.top = max(self.rect.top-self.speed, 0)
        elif direction == 'down':
            self.rect.top = min(self.rect.top+self.speed, screensize[1])
    '''画到屏幕上'''
    def draw(self, screen, mouse_pos):
        angle = math.atan2(mouse_pos[1]-(self.rect.top+32), mouse_pos[0]-(self.rect.left+26))
        image_rotate = pygame.transform.rotate(self.image, 360-angle*57.29)
        bunny_pos = (self.rect.left-image_rotate.get_rect().width/2, self.rect.top-image_rotate.get_rect().height/2)
        self.rotated_position = bunny_pos
        screen.blit(image_rotate, bunny_pos)


'''定义弓箭类'''
class ArrowSprite(pygame.sprite.Sprite):
    def __init__(self, image, position, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.angle = position[0]
        self.image = pygame.transform.rotate(image, 360-position[0]*57.29)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = position[1:]
        self.speed = 10
    '''更新弓箭'''
    def update(self, screensize):
        velx = math.cos(self.angle) * self.speed
        vely = math.sin(self.angle) * self.speed
        self.rect.left += velx
        self.rect.top += vely
        if self.rect.right < 0 or self.rect.left > screensize[0] or self.rect.top > screensize[1] or self.rect.bottom < 0:
            return True
        return False


'''定义獾类'''
class BadguySprite(pygame.sprite.Sprite):
    def __init__(self, image, position, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = position
        self.speed = 7
    '''更新獾'''
    def update(self):
        self.rect.left -= self.speed
        if self.rect.left < 64:
            return True
        return False