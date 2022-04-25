'''
Function:
    定义足球类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import math
import pygame


'''定义足球类'''
class Ball(pygame.sprite.Sprite):
    def __init__(self, images, position):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = position
        self.mask = pygame.mask.from_surface(self.image)
        # 球的速度
        self.speed = 0
        # 球的方向
        self.direction = [0, 0]
        # 控制球的球员
        self.taken_by_player = None
        # 用于切换球动作的变量
        self.action_pointer = 0
        self.count = 0
        self.switch_frequency = 3
        # 是否在运动状态
        self.is_moving = False
    '''更新'''
    def update(self, screen_size):
        # 静止状态
        if not self.is_moving: return
        # 切换球动作实现动画效果
        self.count += 1
        if self.count == self.switch_frequency:
            self.count = 0
            self.action_pointer = (self.action_pointer + 1) % len(self.images)
            self.image = self.images[self.action_pointer]
        # 如果球是被球员控制的
        if self.taken_by_player is not None:
            self.setdirection(self.taken_by_player.direction)
            if self.taken_by_player.direction[0] < 0:
                self.rect.left, self.rect.top = self.taken_by_player.rect.left - 15, self.taken_by_player.rect.top + 30
            elif self.taken_by_player.direction[0] > 0:
                self.rect.left, self.rect.top = self.taken_by_player.rect.left + 30, self.taken_by_player.rect.top + 30
            elif self.taken_by_player.direction[1] < 0:
                self.rect.left, self.rect.top = self.taken_by_player.rect.left + 15, self.taken_by_player.rect.top - 15
            elif self.taken_by_player.direction[1] > 0:
                self.rect.left, self.rect.top = self.taken_by_player.rect.left + 10, self.taken_by_player.rect.top + 50
            return
        # 根据方向移动球
        ori_position = self.rect.left, self.rect.right, self.rect.top, self.rect.bottom
        self.speed = max(self.speed - 1.7 * 0.05, 0.0)
        if self.speed == 0.0: self.is_moving = False
        vector = [self.speed * self.direction[0], self.speed * self.direction[1]]
        vector[0] = vector[0] / math.pow(self.direction[0] ** 2 + self.direction[1] ** 2, 0.5)
        vector[1] = vector[1] / math.pow(self.direction[0] ** 2 + self.direction[1] ** 2, 0.5)
        self.rect.left = min(max(0, self.rect.left + vector[0]), screen_size[0] - 48)
        if self.rect.left == 0 or self.rect.left == screen_size[0] - 48: 
            self.direction = self.direction[0] * -0.8, self.direction[1]
        self.rect.top = min(max(0, self.rect.top + vector[1]), screen_size[1] - 48)
        if ori_position[1] > 1121 or ori_position[0] < 75:
            if self.rect.bottom > 305 and self.rect.top < 505:
                if self.direction[1] > 0:
                    self.rect.bottom = 305
                    self.direction = self.direction[0], self.direction[1] * -0.8
                elif self.direction[1] < 0:
                    self.rect.top = 505
                    self.direction = self.direction[0], self.direction[1] * -0.8
        if self.rect.top == 0 or self.rect.top == screen_size[1] - 48:
            self.direction = self.direction[0], self.direction[1] * -0.8
    '''设置方向'''
    def setdirection(self, direction):
        self.is_moving = True
        self.direction = direction
    '''踢球'''
    def kick(self, direction):
        self.speed = 12
        self.direction = direction
        self.taken_by_player = None
        self.is_moving = True
    '''在屏幕上显示'''
    def draw(self, screen):
        screen.blit(self.image, self.rect)