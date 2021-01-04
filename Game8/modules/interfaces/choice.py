'''
Function:
    游戏模式选择界面
作者:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import pygame


'''游戏选择主界面'''
class MainInterface(pygame.sprite.Sprite):
    def __init__(self, cfg):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(cfg.IMAGEPATHS['choice']['load_game']).convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
    '''更新函数'''
    def update(self):
        pass


'''地图1'''
class MapButton1(pygame.sprite.Sprite):
    def __init__(self, cfg, position=(175, 240)):
        pygame.sprite.Sprite.__init__(self)
        self.image_1 = pygame.image.load(cfg.IMAGEPATHS['choice']['map1_black']).convert()
        self.image_2 = pygame.image.load(cfg.IMAGEPATHS['choice']['map1_red']).convert()
        self.image_3 = pygame.image.load(cfg.IMAGEPATHS['choice']['map1']).convert()
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


'''地图2'''
class MapButton2(pygame.sprite.Sprite):
    def __init__(self, cfg, position=(400, 240)):
        pygame.sprite.Sprite.__init__(self)
        self.image_1 = pygame.image.load(cfg.IMAGEPATHS['choice']['map2_black']).convert()
        self.image_2 = pygame.image.load(cfg.IMAGEPATHS['choice']['map2_red']).convert()
        self.image_3 = pygame.image.load(cfg.IMAGEPATHS['choice']['map2']).convert()
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


'''地图3'''
class MapButton3(pygame.sprite.Sprite):
    def __init__(self, cfg, position=(625, 240)):
        pygame.sprite.Sprite.__init__(self)
        self.image_1 = pygame.image.load(cfg.IMAGEPATHS['choice']['map3_black']).convert()
        self.image_2 = pygame.image.load(cfg.IMAGEPATHS['choice']['map3_red']).convert()
        self.image_3 = pygame.image.load(cfg.IMAGEPATHS['choice']['map3']).convert()
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


'''信息显示框'''
class InfoBox(pygame.sprite.Sprite):
    def __init__(self, position=(400, 475)):
        pygame.sprite.Sprite.__init__(self)
        self.ori_image = pygame.Surface((625, 200))
        self.ori_image.fill((255, 255, 255))
        self.ori_image_front = pygame.Surface((621, 196))
        self.ori_image_front.fill((0, 0, 0))
        self.ori_image.blit(self.ori_image_front, (2, 2))
        self.rect = self.ori_image.get_rect()
        self.rect.center = position
    '''更新函数'''
    def update(self, btns):
        self.image = self.ori_image
        mouse_pos = pygame.mouse.get_pos()
        for btn in btns:
            if btn.rect.collidepoint(mouse_pos):
                self.image.blit(btn.image_3, (225, 25))
                break


'''简单难度按钮'''
class EasyButton(pygame.sprite.Sprite):
    def __init__(self, cfg, position=(400, 150)):
        pygame.sprite.Sprite.__init__(self)
        self.image_1 = pygame.Surface((285, 100))
        self.image_1_front = pygame.Surface((281, 96))
        self.image_1.fill((255, 255, 255))
        self.image_1_front.fill((0, 0, 0))
        self.image_1.blit(self.image_1_front, (2, 2))
        self.image_2 = pygame.Surface((285, 100))
        self.image_2_front = pygame.Surface((281, 96))
        self.image_2.fill((255, 255, 255))
        self.image_2_front.fill((24, 196, 40))
        self.image_2.blit(self.image_2_front, (2, 2))
        self.text = 'easy'
        self.font = pygame.font.Font(cfg.FONTPATHS['m04'], 42)
        self.text_render = self.font.render(self.text, 1, (255, 255, 255))
        self.image_1.blit(self.text_render, (60, 29))
        self.image_2.blit(self.text_render, (60, 29))
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


'''中等难度按钮'''
class MediumButton(pygame.sprite.Sprite):
    def __init__(self, cfg, position=(400, 300)):
        pygame.sprite.Sprite.__init__(self)
        self.image_1 = pygame.Surface((285, 100))
        self.image_1_front = pygame.Surface((281, 96))
        self.image_1.fill((255, 255, 255))
        self.image_1_front.fill((0, 0, 0))
        self.image_1.blit(self.image_1_front, (2, 2))
        self.image_2 = pygame.Surface((285, 100))
        self.image_2_front = pygame.Surface((281, 96))
        self.image_2.fill((255, 255, 255))
        self.image_2_front.fill((24, 30, 196))
        self.image_2.blit(self.image_2_front, (2, 2))
        self.text = 'medium'
        self.font = pygame.font.Font(cfg.FONTPATHS['m04'], 42)
        self.text_render = self.font.render(self.text, 1, (255, 255, 255))
        self.image_1.blit(self.text_render, (15, 29))
        self.image_2.blit(self.text_render, (15, 29))
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


'''困难难度按钮'''
class HardButton(pygame.sprite.Sprite):
    def __init__(self, cfg, position=(400, 450)):
        pygame.sprite.Sprite.__init__(self)
        self.image_1 = pygame.Surface((285, 100))
        self.image_1_front = pygame.Surface((281, 96))
        self.image_1.fill((255, 255, 255))
        self.image_1_front.fill((0, 0, 0))
        self.image_1.blit(self.image_1_front, (2, 2))
        self.image_2 = pygame.Surface((285, 100))
        self.image_2_front = pygame.Surface((281, 96))
        self.image_2.fill((255, 255, 255))
        self.image_2_front.fill((196, 24, 24))
        self.image_2.blit(self.image_2_front, (2, 2))
        self.text = 'hard'
        self.font = pygame.font.Font(cfg.FONTPATHS['m04'], 42)
        self.text_render = self.font.render(self.text, 1, (255, 255, 255))
        self.image_1.blit(self.text_render, (60, 29))
        self.image_2.blit(self.text_render, (60, 29))
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


'''游戏地图和困难选择界面'''
class ChoiceInterface():
    def __init__(self, cfg):
        # part1
        self.main_interface = MainInterface(cfg)
        self.map_btn1 = MapButton1(cfg)
        self.map_btn2 = MapButton2(cfg)
        self.map_btn3 = MapButton3(cfg)
        self.info_box = InfoBox()
        # part2
        self.easy_btn = EasyButton(cfg)
        self.medium_btn = MediumButton(cfg)
        self.hard_btn = HardButton(cfg)
    '''外部调用'''
    def update(self, screen):
        clock = pygame.time.Clock()
        # part1
        self.map_btns = pygame.sprite.Group(self.map_btn1, self.map_btn2, self.map_btn3)
        map_choice, difficulty_choice = None, None
        while True:
            clock.tick(60)
            self.main_interface.update()
            self.map_btns.update()
            self.info_box.update(self.map_btns)
            screen.blit(self.main_interface.image, self.main_interface.rect)
            self.map_btns.draw(screen)
            screen.blit(self.info_box.image, self.info_box.rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        idx = 0
                        for btn in self.map_btns:
                            idx += 1
                            if btn.rect.collidepoint(mouse_pos):
                                map_choice = idx
            if map_choice:
                break
        # part2
        self.difficulty_btns = pygame.sprite.Group(self.easy_btn, self.medium_btn, self.hard_btn)
        while True:
            clock.tick(60)
            screen.fill((0, 0, 0))
            self.difficulty_btns.update()
            self.difficulty_btns.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        idx = 0
                        for btn in self.difficulty_btns:
                            idx += 1
                            if btn.rect.collidepoint(mouse_pos):
                                difficulty_choice = btn.text
            if difficulty_choice:
                break
        return map_choice, difficulty_choice