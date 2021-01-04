'''
Function:
    定义bird类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import pygame
import itertools


'''bird类'''
class Bird(pygame.sprite.Sprite):
    def __init__(self, images, idx, position, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = list(images.values())[idx]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = position
        # 竖直方向运动所需变量
        self.is_flapped = False
        self.down_speed = 0
        self.up_speed = 9
        # 切换bird形态
        self.bird_idx = idx
        self.bird_idx_cycle = itertools.cycle([0, 1, 2, 1])
        self.bird_idx_change_count = 0
    '''更新'''
    def update(self, boundary_values, time_passed):
        # 竖直方向的位置更新
        if self.is_flapped:
            self.up_speed -= 60 * time_passed
            self.rect.top -= self.up_speed
            if self.up_speed <= 0:
                self.unsetFlapped()
                self.up_speed = 9
                self.down_speed = 0
        else:
            self.down_speed += 40 * time_passed
            self.rect.bottom += self.down_speed
        # 判断bird是否因为撞到上下边界而挂掉了
        is_dead = False
        if self.rect.bottom > boundary_values[1]:
            is_dead = True
            self.up_speed = 0
            self.down_speed = 0
            self.rect.bottom = boundary_values[1]
        if self.rect.top < boundary_values[0]:
            is_dead = True
            self.up_speed = 0
            self.down_speed = 0
            self.rect.top = boundary_values[0]
        # 切换bird形态模拟以模拟扇翅膀效果
        self.bird_idx_change_count += 1
        if self.bird_idx_change_count % 5 == 0:
            self.bird_idx = next(self.bird_idx_cycle)
            self.image = list(self.images.values())[self.bird_idx]
            self.bird_idx_change_count = 0
        return is_dead
    '''设置为飞行模式'''
    def setFlapped(self):
        if self.is_flapped:
            self.up_speed = max(12, self.up_speed+1)
        else:
            self.is_flapped = True
    '''设置为下落模式'''
    def unsetFlapped(self):
        self.is_flapped = False
    '''绑定到屏幕'''
    def draw(self, screen):
        screen.blit(self.image, self.rect)