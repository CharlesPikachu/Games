'''
Function:
    定义一些游戏精灵
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import random
import pygame


'''板子'''
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, SCREENWIDTH, SCREENHEIGHT, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.init_state = [x, y, width, height]
        self.rect = pygame.Rect(x, y, width, height)
        self.base_speed = 10
        self.SCREENWIDTH = SCREENWIDTH
        self.SCREENHEIGHT = SCREENHEIGHT
    '''移动板子'''
    def move(self, direction):
        if direction == 'left':
            self.rect.left = max(0, self.rect.left-self.base_speed)
        elif direction == 'right':
            self.rect.right = min(self.SCREENWIDTH, self.rect.right+self.base_speed)
        else:
            raise ValueError('Paddle.move.direction unsupport %s...' % direction)
        return True
    '''绑定到屏幕上'''
    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)
        return True
    '''重置'''
    def reset(self):
        self.rect = pygame.Rect(self.init_state[0], self.init_state[1], self.init_state[2], self.init_state[3])
        return True


'''球'''
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, SCREENWIDTH, SCREENHEIGHT, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.init_state = [x, y, radius*2, radius*2]
        self.rect = pygame.Rect(x, y, radius*2, radius*2)
        self.base_speed = [5, 5]
        self.direction = [random.choice([1, -1]), -1]
        self.radius = radius
        self.SCREENWIDTH = SCREENWIDTH
        self.SCREENHEIGHT = SCREENHEIGHT
    '''移动球'''
    def move(self):
        self.rect.left += self.direction[0] * self.base_speed[0]
        self.rect.top += self.direction[1] * self.base_speed[1]
        if self.rect.left <= 0:
            self.rect.left = 0
            self.direction[0] = -self.direction[0]
        elif self.rect.right >= self.SCREENWIDTH:
            self.rect.right = self.SCREENWIDTH
            self.direction[0] = -self.direction[0]
        if self.rect.top <= 0:
            self.rect.top = 0
            self.direction[1] = -self.direction[1]
        elif self.rect.bottom >= self.SCREENHEIGHT:
            return False
        return True
    '''改变运动速度和方向(与拍相撞时)'''
    def change(self):
        self.base_speed = [random.choice([4, 5, 6]), random.choice([4, 5, 6])]
        self.direction = [random.choice([1, -1]), -1]
        return True
    '''绑定到屏幕上'''
    def draw(self, screen, color):
        pygame.draw.circle(screen, color, (self.rect.left+self.radius, self.rect.top+self.radius), self.radius)
        return True
    '''重置'''
    def reset(self):
        self.rect = pygame.Rect(self.init_state[0], self.init_state[1], self.init_state[2], self.init_state[3])
        return True


'''砖块'''
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.init_state = [x, y, width, height]
        self.rect = pygame.Rect(x, y, width, height)
    '''绑定到屏幕上'''
    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)
        return True
    '''重置'''
    def reset(self):
        self.rect = pygame.Rect(self.init_state[0], self.init_state[1], self.init_state[2], self.init_state[3])
        return True