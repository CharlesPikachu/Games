'''
Function:
    游戏进行中界面
作者:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import json
import math
import random
import pygame
from ..sprites import Enemy
from ..sprites import Turret
from .pause import PauseInterface
from collections import namedtuple


'''游戏进行中界面'''
class GamingInterface():
    def __init__(self, cfg):
        self.cfg = cfg
        # 游戏地图大小
        map_w = self.cfg.SCREENSIZE[0]
        map_h = 500
        # 按钮大小和位置
        button_w = 60
        button_h = 60
        button_y = 520
        # 间隙
        gap = 20
        # 按钮放在工具栏, 工具栏两端各有一个信息显示框
        toolbar_w = gap * 7 + button_w * 6
        info_w = (self.cfg.SCREENSIZE[0] - toolbar_w) // 2
        info_h = self.cfg.SCREENSIZE[1] - map_h
        toolbar_h = self.cfg.SCREENSIZE[1] - map_h
        # 界面布置
        self.map_rect = pygame.Rect(0, 0, map_w, map_h)
        self.map_surface = pygame.Surface((map_w, map_h))
        self.leftinfo_rect = pygame.Rect(0, map_h, info_w, info_h)
        self.rightinfo_rect = pygame.Rect(self.cfg.SCREENSIZE[0] - info_w, map_h, info_w, info_h)
        self.toolbar_rect = pygame.Rect(info_w, map_h, toolbar_w, toolbar_h)
        # 草
        self.grass = pygame.image.load(cfg.IMAGEPATHS['game']['grass'])
        # 岩石(铺路用的)
        self.rock = pygame.image.load(cfg.IMAGEPATHS['game']['rock'])
        # 污垢
        self.dirt = pygame.image.load(cfg.IMAGEPATHS['game']['dirt'])
        # 水
        self.water = pygame.image.load(cfg.IMAGEPATHS['game']['water'])
        # 灌木
        self.bush = pygame.image.load(cfg.IMAGEPATHS['game']['bush'])
        # 纽带
        self.nexus = pygame.image.load(cfg.IMAGEPATHS['game']['nexus'])
        # 洞穴
        self.cave = pygame.image.load(cfg.IMAGEPATHS['game']['cave'])
        # 获取地图元素的大小，请保证素材库里组成地图的元素图大小一致
        self.element_size = int(self.grass.get_rect().width)
        # 一些字体
        self.info_font = pygame.font.Font(cfg.FONTPATHS['Calibri'], 14)
        self.button_font = pygame.font.Font(cfg.FONTPATHS['Calibri'], 20)
        # 可以放炮塔的地方
        self.placeable = {0: self.grass}
        # 地图元素字典(数字对应.map文件中的数字)
        self.map_elements = {
            0: self.grass,
            1: self.rock,
            2: self.dirt,
            3: self.water,
            4: self.bush,
            5: self.nexus,
            6: self.cave
        }
        # 用于记录地图中的道路
        self.path_list = []
        # 当前的地图，将地图导入到这里面
        self.current_map = dict()
        # 当前鼠标携带的图标(即选中道具) -> [道具名, 道具]
        self.mouse_carried = []
        # 在地图上建造好了的炮塔
        self.built_turret_group = pygame.sprite.Group()
        # 所有的敌人
        self.enemies_group = pygame.sprite.Group()
        # 所有射出的箭
        self.arrows_group = pygame.sprite.Group()
        # 玩家操作用的按钮
        Button = namedtuple('Button', ['rect', 'text', 'onClick'])
        self.buttons = [
            Button(pygame.Rect((info_w + gap), button_y, button_w, button_h), 'T1', self.takeT1),
            Button(pygame.Rect((info_w + gap * 2 + button_w), button_y, button_w, button_h), 'T2', self.takeT2),
            Button(pygame.Rect((info_w + gap * 3 + button_w * 2), button_y, button_w, button_h), 'T3', self.takeT3),
            Button(pygame.Rect((info_w + gap * 4 + button_w * 3), button_y, button_w, button_h), 'XXX', self.takeXXX),
            Button(pygame.Rect((info_w + gap * 5 + button_w * 4), button_y, button_w, button_h), 'Pause', self.pauseGame),
            Button(pygame.Rect((info_w + gap * 6 + button_w * 5), button_y, button_w, button_h), 'Quit', self.quitGame)
        ]
    '''开始游戏'''
    def start(self, screen, map_path=None, difficulty_path=None):
        # 读取游戏难度对应的参数
        with open(difficulty_path, 'r') as f:
            difficulty_dict = json.load(f)
        self.money = difficulty_dict.get('money')
        self.health = difficulty_dict.get('health')
        self.max_health = difficulty_dict.get('health')
        difficulty_dict = difficulty_dict.get('enemy')
        # 每60s生成一波敌人
        generate_enemies_event = pygame.constants.USEREVENT + 0
        pygame.time.set_timer(generate_enemies_event, 60000)
        # 生成敌人的flag和当前已生成敌人的总次数
        generate_enemies_flag = False
        num_generate_enemies = 0
        # 每0.5秒出一个敌人
        generate_enemy_event = pygame.constants.USEREVENT + 1
        pygame.time.set_timer(generate_enemy_event, 500)
        generate_enemy_flag = False
        # 防止变量未定义
        enemy_range = None
        num_enemy = None
        # 是否手动操作箭塔射击
        manual_shot = False
        has_control = False
        # 游戏主循环
        while True:
            if self.health <= 0:
                return
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitGame()
                if event.type == pygame.MOUSEBUTTONUP:
                    # --左键选物品
                    if event.button == 1:
                        # ----鼠标点击在地图上
                        if self.map_rect.collidepoint(event.pos):
                            if self.mouse_carried:
                                if self.mouse_carried[0] == 'turret':
                                    self.buildTurret(event.pos)
                                elif self.mouse_carried[0] == 'XXX':
                                    self.sellTurret(event.pos)
                        # ----鼠标点击在工具栏
                        elif self.toolbar_rect.collidepoint(event.pos):
                            for button in self.buttons:
                                if button.rect.collidepoint(event.pos):
                                    if button.text == 'T1':
                                        button.onClick()
                                    elif button.text == 'T2':
                                        button.onClick()
                                    elif button.text == 'T3':
                                        button.onClick()
                                    elif button.text == 'XXX':
                                        button.onClick()
                                    elif button.text == 'Pause':
                                        button.onClick(screen)
                                    elif button.text == 'Quit':
                                        button.onClick()
                                    break
                    # --右键释放物品
                    if event.button == 3:
                        self.mouse_carried = []
                    # --按中间键手动控制炮塔射箭方向一次，否则自由射箭
                    if event.button == 2:
                        manual_shot = True
                if event.type == generate_enemies_event:
                    generate_enemies_flag = True
                if event.type == generate_enemy_event:
                    generate_enemy_flag = True
            # --生成敌人, 生成的敌人随当前已生成敌人的总次数的增加而变强变多
            if generate_enemies_flag:
                generate_enemies_flag = False
                num_generate_enemies += 1
                idx = 0
                for key, value in difficulty_dict.items():
                    idx += 1
                    if idx == len(difficulty_dict.keys()):
                        enemy_range = value['enemy_range']
                        num_enemy = value['num_enemy']
                        break
                    if num_generate_enemies <= int(key):
                        enemy_range = value['enemy_range']
                        num_enemy = value['num_enemy']
                        break
            if generate_enemy_flag and num_enemy:
                generate_enemy_flag = False
                num_enemy -= 1
                enemy = Enemy(random.choice(range(enemy_range)), self.cfg)
                self.enemies_group.add(enemy)
            # --射箭
            for turret in self.built_turret_group:
                if not manual_shot:
                    position = turret.position[0] + self.element_size // 2, turret.position[1]
                    arrow = turret.shot(position)
                else:
                    position = turret.position[0] + self.element_size // 2, turret.position[1]
                    mouse_pos = pygame.mouse.get_pos()
                    angle = math.atan((mouse_pos[1] - position[1]) / (mouse_pos[0] - position[0] + 1e-6))
                    arrow = turret.shot(position, angle)
                    has_control = True
                if arrow:
                    self.arrows_group.add(arrow)
                else:
                    has_control = False
            if has_control:
                has_control = False
                manual_shot = False
            # --移动箭和碰撞检测
            for arrow in self.arrows_group:
                arrow.move()
                points = [(arrow.rect.left, arrow.rect.top), (arrow.rect.left, arrow.rect.bottom), (arrow.rect.right, arrow.rect.top), (arrow.rect.right, arrow.rect.bottom)]
                if (not self.map_rect.collidepoint(points[0])) and (not self.map_rect.collidepoint(points[1])) and \
                   (not self.map_rect.collidepoint(points[2])) and (not self.map_rect.collidepoint(points[3])):
                    self.arrows_group.remove(arrow)
                    del arrow
                    continue
                for enemy in self.enemies_group:
                    if pygame.sprite.collide_rect(arrow, enemy):
                        enemy.life_value -= arrow.attack_power
                        self.arrows_group.remove(arrow)
                        del arrow
                        break
            self.draw(screen, map_path)
    '''将场景画到游戏界面上'''
    def draw(self, screen, map_path):
        self.drawToolbar(screen)
        self.loadMap(screen, map_path)
        self.drawMouseCarried(screen)
        self.drawBuiltTurret(screen)
        self.drawEnemies(screen)
        self.drawArrows(screen)
        pygame.display.flip()
    '''画出所有射出的箭'''
    def drawArrows(self, screen):
        for arrow in self.arrows_group:
            screen.blit(arrow.image, arrow.rect)
    '''画敌人'''
    def drawEnemies(self, screen):
        for enemy in self.enemies_group:
            if enemy.life_value <= 0:
                self.money += enemy.reward
                self.enemies_group.remove(enemy)
                del enemy
                continue
            res = enemy.move(self.element_size)
            if res:
                coord = self.find_next_path(enemy)
                if coord:
                    enemy.reached_path.append(enemy.coord)
                    enemy.coord = coord
                    enemy.position = self.coord2pos(coord)
                    enemy.rect.left, enemy.rect.top = enemy.position
                else:
                    self.health -= enemy.damage
                    self.enemies_group.remove(enemy)
                    del enemy
                    continue
            # 画血条
            green_len = max(0, enemy.life_value / enemy.max_life_value) * self.element_size
            if green_len > 0:
                pygame.draw.line(screen, (0, 255, 0), (enemy.position), (enemy.position[0] + green_len, enemy.position[1]), 1)
            if green_len < self.element_size:
                pygame.draw.line(screen, (255, 0, 0), (enemy.position[0] + green_len, enemy.position[1]), (enemy.position[0] + self.element_size, enemy.position[1]), 1)
            screen.blit(enemy.image, enemy.rect)
    '''画已经建造好的炮塔'''
    def drawBuiltTurret(self, screen):
        for turret in self.built_turret_group:
            screen.blit(turret.image, turret.rect)
    '''画鼠标携带物'''
    def drawMouseCarried(self, screen):
        if self.mouse_carried:
            position = pygame.mouse.get_pos()
            coord = self.pos2coord(position)
            position = self.coord2pos(coord)
            # 在地图里再画
            if self.map_rect.collidepoint(position):
                if self.mouse_carried[0] == 'turret':
                    screen.blit(self.mouse_carried[1].image, position)
                    self.mouse_carried[1].coord = coord
                    self.mouse_carried[1].position = position
                    self.mouse_carried[1].rect.left, self.mouse_carried[1].rect.top = position
                else:
                    screen.blit(self.mouse_carried[1], position)
    '''画工具栏'''
    def drawToolbar(self, screen):
        # 信息显示框
        info_color = (120, 20, 50)
        # --左
        pygame.draw.rect(screen, info_color, self.leftinfo_rect)
        left_title = self.info_font.render('Player info:', True, (255, 255, 255))
        money_info = self.info_font.render('Money: ' + str(self.money), True, (255, 255, 255))
        health_info = self.info_font.render('Health: ' + str(self.health), True, (255, 255, 255))
        screen.blit(left_title, (self.leftinfo_rect.left + 5, self.leftinfo_rect.top + 5))
        screen.blit(money_info, (self.leftinfo_rect.left + 5, self.leftinfo_rect.top + 35))
        screen.blit(health_info, (self.leftinfo_rect.left + 5, self.leftinfo_rect.top + 55))
        # --右
        pygame.draw.rect(screen, info_color, self.rightinfo_rect)
        right_title = self.info_font.render('Selected info:', True, (255, 255, 255))
        screen.blit(right_title, (self.rightinfo_rect.left + 5, self.rightinfo_rect.top + 5))
        # 中间部分
        pygame.draw.rect(screen, (127, 127, 127), self.toolbar_rect)
        for button in self.buttons:
            mouse_pos = pygame.mouse.get_pos()
            if button.rect.collidepoint(mouse_pos):
                self.showSelectedInfo(screen, button)
                button_color = (0, 200, 0)
            else:
                button_color = (0, 100, 0)
            pygame.draw.rect(screen, button_color, button.rect)
            button_text = self.button_font.render(button.text, True, (255, 255, 255))
            button_text_rect = button_text.get_rect()
            button_text_rect.center = (button.rect.centerx, button.rect.centery)
            screen.blit(button_text, button_text_rect)
    '''显示被鼠标选中按钮的作用信息'''
    def showSelectedInfo(self, screen, button):
        if button.text in ['T1', 'T2', 'T3']:
            turret = Turret({'T1': 0, 'T2': 1, 'T3': 2}[button.text], self.cfg)
            selected_info1 = self.info_font.render('Cost: ' + str(turret.price), True, (255, 255, 255))
            selected_info2 = self.info_font.render('Damage: ' + str(turret.arrow.attack_power), True, (255, 255, 255))
            selected_info3 = self.info_font.render('Affordable: ' + str(self.money >= turret.price), True, (255, 255, 255))
            screen.blit(selected_info1, (self.rightinfo_rect.left + 5, self.rightinfo_rect.top + 35))
            screen.blit(selected_info2, (self.rightinfo_rect.left + 5, self.rightinfo_rect.top + 55))
            screen.blit(selected_info3, (self.rightinfo_rect.left + 5, self.rightinfo_rect.top + 75))
        elif button.text == 'XXX':
            selected_info = self.info_font.render('Sell a turret', True, (255, 255, 255))
            screen.blit(selected_info, (self.rightinfo_rect.left + 5, self.rightinfo_rect.top + 35))
        elif button.text == 'Pause':
            selected_info = self.info_font.render('Pause game', True, (255, 255, 255))
            screen.blit(selected_info, (self.rightinfo_rect.left + 5, self.rightinfo_rect.top + 35))
        elif button.text == 'Quit':
            selected_info = self.info_font.render('Quit game', True, (255, 255, 255))
            screen.blit(selected_info, (self.rightinfo_rect.left + 5, self.rightinfo_rect.top + 35))
    '''出售炮塔(半价)'''
    def sellTurret(self, position):
        coord = self.pos2coord(position)
        for turret in self.built_turret_group:
            if coord == turret.coord:
                self.built_turret_group.remove(turret)
                self.money += int(turret.price * 0.5)
                del turret
                break
    '''建造炮塔'''
    def buildTurret(self, position):
        turret = self.mouse_carried[1]
        coord = self.pos2coord(position)
        position = self.coord2pos(coord)
        turret.position = position
        turret.coord = coord
        turret.rect.left, turret.rect.top = position
        if self.money - turret.price >= 0:
            if self.current_map.get(turret.coord) in self.placeable.keys():
                self.money -= turret.price
                self.built_turret_group.add(turret)
                if self.mouse_carried[1].turret_type == 0:
                    self.mouse_carried = []
                    self.takeT1()
                elif self.mouse_carried[1].turret_type == 1:
                    self.mouse_carried = []
                    self.takeT2()
                elif self.mouse_carried[1].turret_type == 2:
                    self.mouse_carried = []
                    self.takeT3()
    '''拿炮塔1'''
    def takeT1(self):
        T1 = Turret(0, self.cfg)
        if self.money >= T1.price:
            self.mouse_carried = ['turret', T1]
    '''拿炮塔2'''
    def takeT2(self):
        T2 = Turret(1, self.cfg)
        if self.money >= T2.price:
            self.mouse_carried = ['turret', T2]
    '''拿炮塔3'''
    def takeT3(self):
        T3 = Turret(2, self.cfg)
        if self.money >= T3.price:
            self.mouse_carried = ['turret', T3]
    '''出售炮塔'''
    def takeXXX(self):
        XXX = pygame.image.load(self.cfg.IMAGEPATHS['game']['x'])
        self.mouse_carried = ['XXX', XXX]
    '''找下一个路径单元'''
    def find_next_path(self, enemy):
        x, y = enemy.coord
        # 优先级: 下右左上
        neighbours = [(x, y+1), (x+1, y), (x-1, y), (x, y-1)]
        for neighbour in neighbours:
            if (neighbour in self.path_list) and (neighbour not in enemy.reached_path):
                return neighbour
        return None
    '''将真实坐标转为地图坐标, 20个单位长度的真实坐标=地图坐标'''
    def pos2coord(self, position):
        return (position[0] // self.element_size, position[1] // self.element_size)
    '''将地图坐标转为真实坐标, 20个单位长度的真实坐标=地图坐标'''
    def coord2pos(self, coord):
        return (coord[0] * self.element_size, coord[1] * self.element_size)
    '''导入地图'''
    def loadMap(self, screen, map_path):
        map_file = open(map_path, 'r')
        idx_j = -1
        for line in map_file.readlines():
            line = line.strip()
            if not line:
                continue
            idx_j += 1
            idx_i = -1
            for col in line:
                try:
                    element_type = int(col)
                    element_img = self.map_elements.get(element_type)
                    element_rect = element_img.get_rect()
                    idx_i += 1
                    element_rect.left, element_rect.top = self.element_size * idx_i, self.element_size * idx_j
                    self.map_surface.blit(element_img, element_rect)
                    self.current_map[idx_i, idx_j] = element_type
                    # 把道路记下来
                    if element_type == 1:
                        self.path_list.append((idx_i, idx_j))
                except:
                    continue
        # 放洞穴和大本营
        self.map_surface.blit(self.cave, (0, 0))
        self.map_surface.blit(self.nexus, (740, 400))
        # 大本营的血条
        nexus_width = self.nexus.get_rect().width
        green_len = max(0, self.health / self.max_health) * nexus_width
        if green_len > 0:
            pygame.draw.line(self.map_surface, (0, 255, 0), (740, 400), (740 + green_len, 400), 3)
        if green_len < nexus_width:
            pygame.draw.line(self.map_surface, (255, 0, 0), (740 + green_len, 400), (740 + nexus_width, 400), 3)
        screen.blit(self.map_surface, (0, 0))
        map_file.close()
    '''暂停游戏'''
    def pauseGame(self, screen):
        pause_interface = PauseInterface(self.cfg)
        pause_interface.update(screen)
    '''退出游戏'''
    def quitGame(self):
        pygame.quit()
        sys.exit(0)