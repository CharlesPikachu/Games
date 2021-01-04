'''
Function:
    游戏结束界面
作者:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import pygame


'''游戏结束主界面'''
class MainInterface(pygame.sprite.Sprite):
    def __init__(self, cfg):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(cfg.IMAGEPATHS['end']['gameover']).convert()
        self.rect = self.image.get_rect()
        self.rect.center = cfg.SCREENSIZE[0] / 2, cfg.SCREENSIZE[1] / 2
    '''更新函数'''
    def update(self):
        pass


'''继续游戏按钮'''
class ContinueButton(pygame.sprite.Sprite):
    def __init__(self, cfg, position=(400, 409)):
        pygame.sprite.Sprite.__init__(self)
        self.image_1 = pygame.image.load(cfg.IMAGEPATHS['end']['continue_black']).convert()
        self.image_2 = pygame.image.load(cfg.IMAGEPATHS['end']['continue_red']).convert()
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


'''游戏结束类'''
class EndInterface():
    def __init__(self, cfg):
        self.main_interface = MainInterface(cfg)
        self.continue_btn = ContinueButton(cfg)
        self.components = pygame.sprite.LayeredUpdates(self.main_interface, self.continue_btn)
    '''外部调用'''
    def update(self, screen):
        clock = pygame.time.Clock()
        background = pygame.Surface(screen.get_size())
        count = 0
        flag = True
        while True:
            count += 1
            clock.tick(60)
            self.components.clear(screen, background)
            self.components.update()
            if count % 10 == 0:
                count = 0
                flag = not flag
            if flag:
                self.components.draw(screen)
            else:
                screen.blit(self.main_interface.image, self.main_interface.rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.continue_btn.rect.collidepoint(mouse_pos):
                            return True