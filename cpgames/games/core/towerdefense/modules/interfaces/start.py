'''
Function:
    游戏开始界面
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import pygame
from .....utils import QuitGame


'''游戏开始主界面'''
class MainInterface(pygame.sprite.Sprite):
    def __init__(self, cfg, resource_loader):
        pygame.sprite.Sprite.__init__(self)
        self.image = resource_loader.images['start']['start_interface'].convert()
        self.rect = self.image.get_rect()
        self.rect.center = cfg.SCREENSIZE[0] / 2, cfg.SCREENSIZE[1] / 2
    '''更新函数'''
    def update(self):
        pass


'''开始游戏按钮'''
class PlayButton(pygame.sprite.Sprite):
    def __init__(self, cfg, resource_loader, position=(220, 415)):
        pygame.sprite.Sprite.__init__(self)
        self.image_1 = resource_loader.images['start']['play_black'].convert()
        self.image_2 = resource_loader.images['start']['play_red'].convert()
        self.image = self.image_1
        self.rect = self.image.get_rect()
        self.rect.center = position
    '''更新函数: 不断地更新检测鼠标是否在按钮上'''
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.image = self.image_2
        else:
            self.image = self.image_1


'''结束游戏按钮'''
class QuitButton(pygame.sprite.Sprite):
    def __init__(self, cfg, resource_loader, position=(580, 415)):
        pygame.sprite.Sprite.__init__(self)
        self.image_1 = resource_loader.images['start']['quit_black'].convert()
        self.image_2 = resource_loader.images['start']['quit_red'].convert()
        self.image = self.image_1
        self.rect = self.image.get_rect()
        self.rect.center = position
    '''更新函数: 不断地更新检测鼠标是否在按钮上'''
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.image = self.image_2
        else:
            self.image = self.image_1


'''游戏开始界面'''
class StartInterface():
    def __init__(self, cfg, resource_loader):
        self.cfg = cfg
        self.main_interface = MainInterface(cfg, resource_loader)
        self.play_btn = PlayButton(cfg, resource_loader)
        self.quit_btn = QuitButton(cfg, resource_loader)
        self.components = pygame.sprite.LayeredUpdates(self.main_interface, self.play_btn, self.quit_btn)
    '''外部调用'''
    def update(self, screen):
        clock = pygame.time.Clock()
        while True:
            clock.tick(self.cfg.FPS)
            self.components.update()
            self.components.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.play_btn.rect.collidepoint(mouse_pos):
                            return True
                        elif self.quit_btn.rect.collidepoint(mouse_pos):
                            return False