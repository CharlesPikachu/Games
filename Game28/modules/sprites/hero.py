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
    def __init__(self, imagepaths, blocksize, block_position, offset=(0, 0), fontpath=None):
        pygame.sprite.Sprite.__init__(self)
        # 设置基础属性
        self.blocksize = blocksize
        self.block_position = block_position
        self.offset = offset
        self.font = pygame.font.Font(fontpath, 40)
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
    def move(self, direction, map_parser):
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
            if map_parser.map_matrix[block_position[1]][block_position[0]] in ['0', '00']:
                self.block_position = block_position
            # --触发事件
            elif map_parser.map_matrix[block_position[1]][block_position[0]] in ['2', '3', '4', '6', '7', '8', '9', '10', '13', '14', '24']:
                flag, events = self.dealcollideevent(
                    elem=map_parser.map_matrix[block_position[1]][block_position[0]],
                    block_position=block_position,
                    map_parser=map_parser,
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
    def dealcollideevent(self, elem, block_position, map_parser):
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
            map_parser.map_matrix[block_position[1]][block_position[0] - 1] = elem
            map_parser.map_matrix[block_position[1]][block_position[0]] = '0'
            return False, []
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