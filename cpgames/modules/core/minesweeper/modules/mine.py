'''
Function:
    定义单个雷
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import pygame


'''雷'''
class Mine(pygame.sprite.Sprite):
    def __init__(self, images, position, status_code=0, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        # 导入图片
        self.images = images
        self.image = self.images['blank']
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        # 雷当前的状态
        self.status_code = status_code
        # 真雷还是假雷(默认是假雷)
        self.is_mine_flag = False
        # 周围雷的数目
        self.num_mines_around = -1
    '''设置当前的状态码'''
    def setstatus(self, status_code):
        self.status_code = status_code
    '''埋雷'''
    def burymine(self):
        self.is_mine_flag = True
    '''设置周围雷的数目'''
    def setnumminesaround(self, num_mines_around):
        self.num_mines_around = num_mines_around
    '''画到屏幕上'''
    def draw(self, screen):
        # 状态码为0, 代表该雷未被点击
        if self.status_code == 0:
            self.image = self.images['blank']
        # 状态码为1, 代表该雷已被点开
        elif self.status_code == 1:
            self.image = self.images['mine'] if self.is_mine_flag else self.images[str(self.num_mines_around)]
        # 状态码为2, 代表该雷被玩家标记为雷
        elif self.status_code == 2:
            self.image = self.images['flag']
        # 状态码为3, 代表该雷被玩家标记为问号
        elif self.status_code == 3:
            self.image = self.images['ask']
        # 状态码为4, 代表该雷正在被鼠标左右键双击
        elif self.status_code == 4:
            assert not self.is_mine_flag
            self.image = self.images[str(self.num_mines_around)]
        # 状态码为5, 代表该雷在被鼠标左右键双击的雷的周围
        elif self.status_code == 5:
            self.image = self.images['0']
        # 状态码为6, 代表该雷被踩中
        elif self.status_code == 6:
            assert self.is_mine_flag
            self.image = self.images['blood']
        # 状态码为7, 代表该雷被误标
        elif self.status_code == 7:
            assert not self.is_mine_flag
            self.image = self.images['error']
        # 绑定图片到屏幕
        screen.blit(self.image, self.rect)
    @property
    def opened(self):
        return self.status_code == 1