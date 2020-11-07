'''
Function:
    定义接金币的小人
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import pygame


'''定义hero类'''
class Hero(pygame.sprite.Sprite):
    def __init__(self, images, position=(375, 520), **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.images_right = images[:5]
        self.images_left = images[5:]
        self.images = self.images_right.copy()
        self.image = self.images[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.diretion = 'right'
        self.speed = 8
        self.switch_frame_count = 0
        self.switch_frame_freq = 1
        self.frame_index = 0
    '''左右移动hero'''
    def move(self, screensize, direction):
        assert direction in ['left', 'right']
        if direction != self.diretion:
            self.images = self.images_left.copy() if direction == 'left' else self.images_right.copy()
            self.image = self.images[0]
            self.diretion = direction
            self.switch_frame_count = 0
        self.switch_frame_count += 1
        if self.switch_frame_count % self.switch_frame_freq == 0:
            self.switch_frame_count = 0
            self.frame_index = (self.frame_index + 1) % len(self.images)
            self.image = self.images[self.frame_index]
        if direction == 'left':
            self.rect.left = max(self.rect.left-self.speed, 0)
        else:
            self.rect.left = min(self.rect.left+self.speed, screensize[0])
    '''画到屏幕上'''
    def draw(self, screen):
        screen.blit(self.image, self.rect)