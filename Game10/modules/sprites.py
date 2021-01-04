'''
Function:
    定义一些游戏精灵类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import pygame
import random


'''子弹'''
class Bullet(pygame.sprite.Sprite):
    def __init__(self, idx, position, cfg):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(cfg.IMAGEPATHS['bullet']).convert_alpha()
        self.image = pygame.transform.scale(self.image, (10, 10))
        # 位置
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.position = position
        # 速度
        self.speed = 8
        # 玩家编号
        self.player_idx = idx
    '''移动子弹'''
    def move(self):
        self.position = self.position[0], self.position[1] - self.speed
        self.rect.left, self.rect.top = self.position
    '''画子弹'''
    def draw(self, screen):
        screen.blit(self.image, self.rect)


'''小行星'''
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, cfg):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(cfg.IMAGEPATHS['asteroid']).convert_alpha()
        # 位置
        self.rect = self.image.get_rect()
        self.position = (random.randrange(20, cfg.SCREENSIZE[0] - 20), -64)
        self.rect.left, self.rect.top = self.position
        # 速度
        self.speed = random.randrange(3, 9)
        self.angle = 0
        self.angular_velocity = random.randrange(1, 5)
        self.rotate_ticks = 3
    '''移动小行星'''
    def move(self):
        self.position = self.position[0], self.position[1] + self.speed
        self.rect.left, self.rect.top = self.position
    '''转动小行星'''
    def rotate(self):
        self.rotate_ticks -= 1
        if self.rotate_ticks == 0:
            self.angle = (self.angle + self.angular_velocity) % 360
            orig_rect = self.image.get_rect()
            rot_image = pygame.transform.rotate(self.image, self.angle)
            rot_rect = orig_rect.copy()
            rot_rect.center = rot_image.get_rect().center
            rot_image = rot_image.subsurface(rot_rect).copy()
            self.image = rot_image
            self.rotate_ticks = 3
    '''画小行星'''
    def draw(self, screen):
        screen.blit(self.image, self.rect)


'''飞船'''
class Ship(pygame.sprite.Sprite):
    def __init__(self, idx, cfg):
        pygame.sprite.Sprite.__init__(self)
        self.cfg = cfg
        self.image = pygame.image.load(cfg.IMAGEPATHS['ship']).convert_alpha()
        self.explode_image = pygame.image.load(cfg.IMAGEPATHS['ship_exploded']).convert_alpha()
        # 位置
        self.position = {'x': random.randrange(-10, 918), 'y': random.randrange(-10, 520)}
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = self.position['x'], self.position['y']
        # 速度
        self.speed = {'x': 10, 'y': 5}
        # 玩家编号
        self.player_idx = idx
        # 子弹冷却时间
        self.cooling_time = 0
        # 爆炸用
        self.explode_step = 0
    '''飞船爆炸'''
    def explode(self, screen):
        img = self.explode_image.subsurface((48 * (self.explode_step - 1), 0), (48, 48))
        screen.blit(img, (self.position['x'], self.position['y']))
        self.explode_step += 1
    '''移动飞船'''
    def move(self, direction):
        if direction == 'left':
            self.position['x'] = max(-self.speed['x'] + self.position['x'], -10)
        elif direction == 'right':
            self.position['x'] = min(self.speed['x'] + self.position['x'], 918)
        elif direction == 'up':
            self.position['y'] = max(-self.speed['y'] + self.position['y'], -10)
        elif direction == 'down':
            self.position['y'] = min(self.speed['y'] + self.position['y'], 520)
        self.rect.left, self.rect.top = self.position['x'], self.position['y']
    '''画飞船'''
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    '''射击'''
    def shot(self):
        return Bullet(self.player_idx, (self.rect.center[0] - 5, self.position['y'] - 5), self.cfg)