'''
Function:
    定义我们的主角勇士
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import pygame


'''定义我们的主角勇士'''
class Hero(pygame.sprite.Sprite):
    def __init__(self, imagepaths, blocksize, block_position, offset=(0, 0), fontpath=None, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        # 设置基础属性
        self.blocksize = blocksize
        self.block_position = block_position
        self.offset = offset
        self.font = pygame.font.Font(fontpath, 40)
        for key, value in kwargs.items():
            setattr(self, key, value)
        # 加载对应的图片
        self.images = {}
        for key, value in imagepaths.items():
            self.images[key] = pygame.transform.scale(pygame.image.load(value), (blocksize, blocksize))
        self.image = self.images['down']
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = block_position[0] * blocksize + offset[0], block_position[1] * blocksize + offset[1]
        # 设置等级等信息
        self.level = 1
        self.life_value = 1000
        self.attack_power = 10
        self.defense_power = 10
        self.num_coins = 0
        self.experience = 0
        self.num_yellow_keys = 1
        self.num_purple_keys = 1
        self.num_red_keys = 1
        # 行动冷却
        self.move_cooling_count = 0
        self.move_cooling_time = 5
        self.freeze_move_flag = False
    '''行动'''
    def move(self, direction, map_parser, screen):
        # 判断是否冷冻行动
        if self.freeze_move_flag: return
        assert direction in self.images
        self.image = self.images[direction]
        # 移动勇士
        move_vector = {'left': (-1, 0), 'right': (1, 0), 'up': (0, -1), 'down': (0, 1)}[direction]
        block_position = self.block_position[0] + move_vector[0], self.block_position[1] + move_vector[1]
        # 判断该移动是否合法, 并触发对应的事件
        events = []
        if block_position[0] >= 0 and block_position[0] < map_parser.map_size[1] and \
             block_position[1] >= 0 and block_position[1] < map_parser.map_size[0]:
            # --合法移动
            if map_parser.map_matrix[block_position[1]][block_position[0]] in ['0', '00', 'hero']:
                self.block_position = block_position
            # --触发事件
            elif map_parser.map_matrix[block_position[1]][block_position[0]] in ['2', '3', '4', '6', '7', '8', '9', '10', '13', '14', '24'] + list(map_parser.monsters_dict.keys()):
                flag, events = self.dealcollideevent(
                    elem=map_parser.map_matrix[block_position[1]][block_position[0]],
                    block_position=block_position,
                    map_parser=map_parser,
                    screen=screen,
                )
                if flag: self.block_position = block_position
        # 重新设置勇士位置
        self.rect.left, self.rect.top = self.block_position[0] * self.blocksize + self.offset[0], self.block_position[1] * self.blocksize + self.offset[1]
        # 冷冻行动
        self.freeze_move_flag = True
        # 返回需要在主循环里触发的事件
        return events
    '''放置到上/下楼梯口旁'''
    def placenexttostairs(self, map_parser, stairs_type='up'):
        assert stairs_type in ['up', 'down']
        for row_idx, row in enumerate(map_parser.map_matrix):
            for col_idx, elem in enumerate(row):
                if (stairs_type == 'up' and elem == '13') or (stairs_type == 'down' and elem == '14'):
                    if row_idx > 0 and map_parser.map_matrix[row_idx - 1][col_idx] == '00':
                        self.block_position = col_idx, row_idx - 1
                    elif row_idx < map_parser.map_size[0] - 1 and map_parser.map_matrix[row_idx + 1][col_idx] == '00':
                        self.block_position = col_idx, row_idx + 1
                    elif col_idx > 0 and map_parser.map_matrix[row_idx][col_idx - 1] == '00':
                        self.block_position = col_idx - 1, row_idx
                    elif col_idx < map_parser.map_size[1] - 1 and map_parser.map_matrix[row_idx][col_idx + 1] == '00':
                        self.block_position = col_idx + 1, row_idx
        self.rect.left, self.rect.top = self.block_position[0] * self.blocksize + self.offset[0], self.block_position[1] * self.blocksize + self.offset[1]
    '''处理撞击事件'''
    def dealcollideevent(self, elem, block_position, map_parser, screen):
        # 遇到不同颜色的门, 有钥匙则打开, 否则无法前进
        if elem in ['2', '3', '4']:
            flag = False
            if elem == '2' and self.num_yellow_keys > 0:
                self.num_yellow_keys -= 1
                flag = True
            elif elem == '3' and self.num_purple_keys > 0:
                self.num_purple_keys -= 1
                flag = True
            elif elem == '4' and self.num_red_keys > 0:
                self.num_red_keys -= 1
                flag = True
            if flag: map_parser.map_matrix[block_position[1]][block_position[0]] = '0'
            return flag, []
        # 捡到不同颜色的钥匙
        elif elem in ['6', '7', '8']:
            if elem == '6': self.num_yellow_keys += 1
            elif elem == '7': self.num_purple_keys += 1
            elif elem == '8': self.num_red_keys += 1
            map_parser.map_matrix[block_position[1]][block_position[0]] = '0'
            return True, []
        # 捡到宝石
        elif elem in ['9', '10']:
            if elem == '9': self.defense_power += 3
            elif elem == '10': self.attack_power += 3
            map_parser.map_matrix[block_position[1]][block_position[0]] = '0'
            return True, []
        # 上下楼梯
        elif elem in ['13', '14']:
            if elem == '13': events = ['upstairs']
            elif elem == '14': events = ['downstairs']
            return True, events
        # 遇到仙女, 进行对话, 并左移一格
        elif elem in ['24']:
            if map_parser.map_matrix[block_position[1]][block_position[0] - 1] == '0':
                map_parser.map_matrix[block_position[1]][block_position[0] - 1] = elem
                map_parser.map_matrix[block_position[1]][block_position[0]] = '0'
            return False, ['conversation_hero_and_fairy']
        # 遇到怪物
        elif elem in map_parser.monsters_dict:
            monster = map_parser.monsters_dict[elem]
            if self.winmonster(monster):
                self.battle(monster, map_parser.element_images[elem][0], map_parser, screen)
                map_parser.map_matrix[block_position[1]][block_position[0]] = '0'
                return True, []
            else:
                return False, []
    '''判断勇士是否可以打赢怪物'''
    def winmonster(self, monster):
        # 如果攻击力低于怪物防御力, monster: [名字, 生命值, 攻击力, 防御力]
        if self.attack_power <= monster[3]: return False
        # 如果防御力高于怪物攻击力
        if self.defense_power >= monster[2]: return True
        # 我方打怪物一次扣多少血
        diff_our = self.attack_power - monster[3]
        # 怪物打我方一次扣多少血
        diff_monster = monster[2] - self.defense_power
        # 计算谁可以win
        if round(monster[1] / diff_our) <= round(self.life_value / diff_monster):
            return True
        return False
    '''将勇士绑定到屏幕上'''
    def draw(self, screen):
        if self.freeze_move_flag:
            self.move_cooling_count += 1
            if self.move_cooling_count > self.move_cooling_time:
                self.move_cooling_count = 0
                self.freeze_move_flag = False
        screen.blit(self.image, self.rect)
        font_renders = [
            self.font.render(str(self.level), True, (255, 255, 255)),
            self.font.render(str(self.life_value), True, (255, 255, 255)),
            self.font.render(str(self.attack_power), True, (255, 255, 255)),
            self.font.render(str(self.defense_power), True, (255, 255, 255)),
            self.font.render(str(self.num_coins), True, (255, 255, 255)),
            self.font.render(str(self.experience), True, (255, 255, 255)),
            self.font.render(str(self.num_yellow_keys), True, (255, 255, 255)),
            self.font.render(str(self.num_purple_keys), True, (255, 255, 255)),
            self.font.render(str(self.num_red_keys), True, (255, 255, 255)),
        ]
        rects = [fr.get_rect() for fr in font_renders]
        rects[0].topleft = (160, 80)
        for idx in range(1, 6):
            rects[idx].topleft = 160, 127 + 42 * (idx - 1)
        for idx in range(6, 9):
            rects[idx].topleft = 160, 364 + 55 * (idx - 6)
        for fr, rect in zip(font_renders, rects):
            screen.blit(fr, rect)
    '''战斗画面'''
    def battle(self, monster, monster_image, map_parser, screen):
        monster = list(monster).copy()
        # 我方打怪物一次扣多少血
        diff_our = self.attack_power - monster[3]
        # 怪物打我方一次扣多少血
        diff_monster = monster[2] - self.defense_power
        # 更新战斗面板的频率
        update_count, update_interval, update_hero = 0, 5, False
        # 主循环
        clock = pygame.time.Clock()
        font = pygame.font.Font(self.cfg.FONTPATH_CN, 40)
        while True:
            screen.fill((0, 0, 0))
            screen.blit(self.background_images['gamebg'], (0, 0))
            map_parser.draw(screen)
            for scene in self.cur_scenes:
                screen.blit(scene[0], scene[1])
            self.draw(screen)
            # --按键检测
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # --更新战斗面板
            update_count += 1
            if update_count > update_interval:
                update_count = 0
                if update_hero:
                    self.life_value = self.life_value - (monster[2] - self.defense_power)
                else:
                    monster[1] = max(monster[1] - (self.attack_power - monster[3]), 0)
                update_hero = not update_hero
                if monster[1] <= 0: return
            screen.blit(self.background_images['battlebg'], (20, 40))
            screen.blit(monster_image, (90, 140))
            font_renders = [
                font.render(str(monster[1]), True, (255, 255, 255)),
                font.render(str(monster[2]), True, (255, 255, 255)),
                font.render(str(monster[3]), True, (255, 255, 255)),
                font.render(str(self.life_value), True, (255, 255, 255)),
                font.render(str(self.attack_power), True, (255, 255, 255)),
                font.render(str(self.defense_power), True, (255, 255, 255)),
            ]
            rects = [fr.get_rect() for fr in font_renders]
            for idx in range(3):
                rects[idx].top, rects[idx].left = 78 + idx * 95, 320
            for idx in range(3, 6):
                rects[idx].top, rects[idx].right = 78 + (idx - 3) * 95, 655
            for fr, rect in zip(font_renders, rects):
                screen.blit(fr, rect)
            # --刷新
            pygame.display.flip()
            clock.tick(self.cfg.FPS)