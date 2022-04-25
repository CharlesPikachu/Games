'''
Function:
    定义球员类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import random
import pygame


'''定义球员类'''
class Player(pygame.sprite.Sprite):
    def __init__(self, image, position, direction=(1, 0), auto_control=False, player_type=None, group_id=None):
        pygame.sprite.Sprite.__init__(self)
        self.images_dict = {
            'down': [
                image.subsurface((0, 0, 32, 48)), image.subsurface((32, 0, 32, 48)),
                image.subsurface((64, 0, 32, 48)), image.subsurface((96, 0, 32, 48))
            ],
            'left': [
                image.subsurface((0, 48, 32, 48)), image.subsurface((32, 48, 32, 48)),
                image.subsurface((64, 48, 32, 48)), image.subsurface((96, 48, 32, 48))
            ],
            'right': [
                image.subsurface((0, 96, 32, 48)), image.subsurface((32, 96, 32, 48)),
                image.subsurface((64, 96, 32, 48)), image.subsurface((96, 96, 32, 48))
            ],
            'up': [
                image.subsurface((0, 144, 32, 48)), image.subsurface((32, 144, 32, 48)),
                image.subsurface((64, 144, 32, 48)), image.subsurface((96, 144, 32, 48))
            ],
        }
        self.position = list(position)
        self.auto_control = auto_control
        self.player_type = player_type
        self.group_id = group_id
        # 用于切换人物动作的变量
        self.action_pointer = 0
        self.count = 0
        self.switch_frequency = 3
        # 设置方向
        self.setdirection(direction)
        # 人物速度
        self.speed = 2
        # 是否在运动状态
        self.is_moving = False
        # 准备踢球动作的变量
        self.prepare_for_kicking = False
        self.prepare_for_kicking_count = 0
        self.prepare_for_kicking_freq = 20
        # 保持运动方向的变量
        self.keep_direction_freq = 50
        self.keep_direction_count = 50
    '''更新'''
    def update(self, screen_size, ball):
        # 电脑自动控制
        if self.auto_control:
            self.autoupdate(screen_size, ball)
            return
        # 静止状态
        if not self.is_moving: return
        # 切换人物动作实现动画效果
        self.switch()
        # 根据方向移动人物
        ori_position = self.position.copy()
        speed = self.speed * self.direction[0], self.speed * self.direction[1]
        self.position[0] = min(max(0, self.position[0] + speed[0]), screen_size[0] - 48)
        self.position[1] = min(max(0, self.position[1] + speed[1]), screen_size[1] - 48)
        self.rect.left, self.rect.top = self.position
        if self.rect.bottom > 305 and self.rect.top < 505 and (self.rect.right > 1121 or self.rect.left < 75):
            self.position = ori_position
            self.rect.left, self.rect.top = self.position
        # 设置为静止状态
        self.is_moving = False
    '''自动更新'''
    def autoupdate(self, screen_size, ball):
        # 守门员
        if self.player_type == 'goalkeeper':
            self.speed = 1
            # --沿着门漫步
            def wondering(self):
                self.switch()
                self.position[1] = min(max(305, self.position[1] + self.direction[1] * self.speed), 459)
                self.rect.left, self.rect.top = self.position
                if self.rect.top == 305 or self.rect.top == 459: 
                    self.direction = self.direction[0], -self.direction[1]
                    self.setdirection(self.direction)
            # --有球就随机射球
            if ball.taken_by_player == self:
                if self.group_id == 1:
                    if random.random() > 0.8 or self.prepare_for_kicking:
                        self.prepare_for_kicking = True
                        self.setdirection((1, 0))
                        if self.prepare_for_kicking:
                            self.prepare_for_kicking_count += 1
                            if self.prepare_for_kicking_count > self.prepare_for_kicking_freq:
                                self.prepare_for_kicking_count = 0
                                self.prepare_for_kicking = False
                                ball.kick(self.direction)
                                self.setdirection(random.choice([(0, 1), (0, -1)]))
                    else:
                        wondering(self)
                else:
                    if random.random() > 0.8 or self.prepare_for_kicking:
                        self.prepare_for_kicking = True
                        self.setdirection((-1, 0))
                        if self.prepare_for_kicking:
                            self.prepare_for_kicking_count += 1
                            if self.prepare_for_kicking_count > self.prepare_for_kicking_freq:
                                self.prepare_for_kicking_count = 0
                                self.prepare_for_kicking = False
                                ball.kick(self.direction)
                                self.setdirection(random.choice([(0, 1), (0, -1)]))
                    else:
                        wondering(self)
            # --没球来回走
            else:
                wondering(self)
        # 其他球员跟着球走
        else:
            if ball.taken_by_player == self:
                self.switch()
                if self.group_id == 1:
                    self.direction = min(max(1150 - self.rect.left, -1), 1), min(max(405 - self.rect.top, -1), 1)
                else:
                    self.direction = min(max(350 - self.rect.left, -1), 1), min(max(405 - self.rect.top, -1), 1)
                self.setdirection(self.direction)
                if (random.random() > 0.9 and self.position[0] > 350 and self.position[0] < 1150) or self.prepare_for_kicking:
                    if self.group_id == 1:
                        self.direction = min(max(1190 - self.rect.left, -1), 1), min(max(405 - self.rect.top, -1), 1)
                    else:
                        self.direction = min(max(310 - self.rect.left, -1), 1), min(max(405 - self.rect.top, -1), 1)
                    self.setdirection(self.direction)
                    self.prepare_for_kicking = True
                    if self.prepare_for_kicking:
                        self.prepare_for_kicking_count += 1
                        if self.prepare_for_kicking_count > self.prepare_for_kicking_freq:
                            self.prepare_for_kicking_count = 0
                            self.prepare_for_kicking = False
                            ball.kick(self.direction)
                else:
                    speed = self.speed * self.direction[0], self.speed * self.direction[1]
                    ori_position = self.position.copy()
                    self.position[0] = min(max(0, self.position[0] + speed[0]), screen_size[0] - 48)
                    self.position[1] = min(max(0, self.position[1] + speed[1]), screen_size[1] - 48)
                    self.rect.left, self.rect.top = self.position
                    if self.rect.bottom > 305 and self.rect.top < 505 and (self.rect.right > 1121 or self.rect.left < 75):
                        self.position = ori_position
                        self.rect.left, self.rect.top = self.position
            else:
                self.switch()
                if (ball.rect.centery > 400 and self.player_type == 'bottomhalf') or (ball.rect.centery <= 400 and self.player_type == 'upperhalf') or self.player_type == 'common':
                    self.direction = min(max(ball.rect.left - self.rect.left, -1), 1), min(max(ball.rect.top - self.rect.top, -1), 1)
                    self.direction = self.direction[0] * random.random(), self.direction[1] * random.random()
                else:
                    if self.keep_direction_count >= self.keep_direction_freq:
                        self.direction = random.choice([-1, 0, 1]), random.choice([-1, 0, 1])
                        self.keep_direction_count = 0
                    else:
                        self.keep_direction_count += 1
                self.setdirection(self.direction)
                speed = self.speed * self.direction[0], self.speed * self.direction[1]
                ori_position = self.position.copy()
                self.position[0] = min(max(0, self.position[0] + speed[0]), screen_size[0] - 48)
                self.position[1] = min(max(0, self.position[1] + speed[1]), screen_size[1] - 48)
                self.rect.left, self.rect.top = self.position
                if self.rect.bottom > 305 and self.rect.top < 505 and (self.rect.right > 1121 or self.rect.left < 75):
                    self.position = ori_position
                    self.rect.left, self.rect.top = self.position
    '''切换人物动作实现动画效果'''
    def switch(self):
        self.count += 1
        if self.count == self.switch_frequency:
            self.count = 0
            self.action_pointer = (self.action_pointer + 1) % len(self.images)
            self.image = self.images[self.action_pointer]
    '''设置方向'''
    def setdirection(self, direction):
        self.direction = direction
        self.is_moving = True
        self.images = self.fetchimages(direction)
        self.image = self.images[self.action_pointer]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = self.position
        self.mask = pygame.mask.from_surface(self.image)
    '''根据方向获得图片'''
    def fetchimages(self, direction):
        if direction[0] > 0: return self.images_dict['right']
        elif direction[0] < 0: return self.images_dict['left']
        elif direction[1] > 0: return self.images_dict['down']
        elif direction[1] < 0: return self.images_dict['up']
        else: return self.images
    '''在屏幕上显示'''
    def draw(self, screen):
        screen.blit(self.image, self.rect)