'''
Function:
    一些必要的精灵类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import random
import pygame
from .utils import *


'''乒乓球'''
class Ball(pygame.sprite.Sprite):
    def __init__(self, imgpath, cfg, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.cfg = cfg
        self.image = loadImage(imgpath)
        self.rect = self.image.get_rect()
        self.reset()
    '''移动'''
    def move(self, ball, racket_left, racket_right, hit_sound, goal_sound):
        self.rect.left = self.rect.left + self.speed * self.direction_x
        self.rect.top = min(max(self.rect.top + self.speed * self.direction_y, 0), self.cfg.HEIGHT - self.rect.height)
        # 撞到球拍
        if pygame.sprite.collide_rect(ball, racket_left) or pygame.sprite.collide_rect(ball, racket_right):
            self.direction_x, self.direction_y = -self.direction_x, random.choice([1, -1])
            self.speed += 1
            scores = [0, 0]
            hit_sound.play()
        # 撞到上侧的墙
        elif self.rect.top == 0:
            self.direction_y = 1
            self.speed += 1
            scores = [0, 0]
        # 撞到下侧的墙
        elif self.rect.top == self.cfg.HEIGHT - self.rect.height:
            self.direction_y = -1
            self.speed += 1
            scores = [0, 0]
        # 撞到左边的墙
        elif self.rect.left < 0:
            self.reset()
            racket_left.reset()
            racket_right.reset()
            scores = [0, 1]
            goal_sound.play()
        # 撞到右边的墙
        elif self.rect.right > self.cfg.WIDTH:
            self.reset()
            racket_left.reset()
            racket_right.reset()
            scores = [1, 0]
            goal_sound.play()
        # 普通情况
        else:
            scores = [0, 0]
        return scores
    '''初始化'''
    def reset(self):
        self.rect.centerx = self.cfg.WIDTH // 2
        self.rect.centery = random.randrange(self.rect.height // 2, self.cfg.HEIGHT - self.rect.height // 2)
        self.direction_x = random.choice([1, -1])
        self.direction_y = random.choice([1, -1])
        self.speed = 1
    '''绑定到屏幕上'''
    def draw(self, screen):
        screen.blit(self.image, self.rect)


'''乒乓球拍'''
class Racket(pygame.sprite.Sprite):
    def __init__(self, imgpath, type_, cfg, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.cfg = cfg
        self.type_ = type_
        self.image = loadImage(imgpath, False)
        self.rect = self.image.get_rect()
        self.reset()
    '''移动'''
    def move(self, direction):
        if direction == 'UP':
            self.rect.top = max(0, self.rect.top - self.speed)
        elif direction == 'DOWN':
            self.rect.bottom = min(self.cfg.HEIGHT, self.rect.bottom + self.speed)
        else:
            raise ValueError('[direction] in Racket.move is %s, expect %s or %s...' % (direction, 'UP', 'DOWN'))
    '''电脑自动移动'''
    def automove(self, ball):
        if ball.rect.centery - 25 > self.rect.centery:
            self.move('DOWN')
        if ball.rect.centery + 25 < self.rect.centery:
            self.move('UP')
    '''初始化'''
    def reset(self):
        # 左/右边的拍
        self.rect.centerx = self.cfg.WIDTH - self.rect.width // 2 if self.type_ == 'RIGHT' else self.rect.width // 2
        self.rect.centery = self.cfg.HEIGHT // 2
        # 速度
        self.speed = 5
    '''绑定到屏幕上'''
    def draw(self, screen):
        screen.blit(self.image, self.rect)