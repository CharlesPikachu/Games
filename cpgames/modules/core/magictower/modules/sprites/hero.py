'''
Function:
    定义我们的主角勇士
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import pygame
from .....utils import QuitGame


'''定义我们的主角勇士'''
class Hero(pygame.sprite.Sprite):
    def __init__(self, images, blocksize, block_position, offset=(0, 0), fontpath=None, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        # 设置基础属性
        self.blocksize = blocksize
        self.block_position = block_position
        self.offset = offset
        self.fontpath = fontpath
        self.font = pygame.font.Font(fontpath, 40)
        for key, value in kwargs.items(): setattr(self, key, value)
        # 对应的图片
        self.images = {}
        for key, value in images.items():
            self.images[key] = pygame.transform.scale(value, (blocksize, blocksize))
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
        # 是否拥有一些宝物
        # --幸运十字架
        self.has_cross = False
        # --圣光徽
        self.has_forecast = False
        # --风之罗盘
        self.has_jump = False
        # --星光神榔
        self.has_hammer = False
        # 行动冷却
        self.move_cooling_count = 0
        self.move_cooling_time = 5
        self.freeze_move_flag = False
        # 获得物品提示
        self.obtain_tips = None
        self.show_obtain_tips_count = 0
        self.max_obtain_tips_count = 20
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
            else:
                flag, events = self.dealcollideevent(
                    elem=map_parser.map_matrix[block_position[1]][block_position[0]],
                    block_position=block_position,
                    map_parser=map_parser,
                    screen=screen,
                )
                if flag:
                    self.block_position = block_position
                    map_parser.map_matrix[block_position[1]][block_position[0]] = '0'
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
            return flag, []
        # 捡到不同颜色的钥匙
        elif elem in ['6', '7', '8']:
            if elem == '6':
                self.num_yellow_keys += 1
                self.obtain_tips = '得到一把黄钥匙'
            elif elem == '7':
                self.num_purple_keys += 1
                self.obtain_tips = '得到一把蓝钥匙'
            elif elem == '8':
                self.num_red_keys += 1
                self.obtain_tips = '得到一把红钥匙'
            return True, []
        # 捡到宝石
        elif elem in ['9', '10']:
            if elem == '9':
                self.defense_power += 3
                self.obtain_tips = '得到一个蓝宝石 防御力加3'
            elif elem == '10':
                self.attack_power += 3
                self.obtain_tips = '得到一个红宝石 攻击力加3'
            return True, []
        # 捡到血瓶
        elif elem in ['11', '12']:
            if elem == '11':
                self.life_value += 200
                self.obtain_tips = '得到一个小血瓶 生命加200'
            elif elem == '12':
                self.life_value += 500
                self.obtain_tips = '得到一个大血瓶 生命加500'
            return True, []
        # 上下楼梯
        elif elem in ['13', '14']:
            if elem == '13': events = ['upstairs']
            elif elem == '14': events = ['downstairs']
            return False, events
        # 商店
        elif elem in ['22', '26', '27']:
            if elem == '22':
                return False, ['buy_from_shop']
            elif elem == '26':
                return False, ['buy_from_oldman']
            elif elem == '27':
                return False, ['buy_from_businessman']
        # 遇到仙女, 进行对话, 并左移一格
        elif elem in ['24']:
            if map_parser.map_matrix[block_position[1]][block_position[0] - 1] == '0':
                map_parser.map_matrix[block_position[1]][block_position[0] - 1] = elem
                map_parser.map_matrix[block_position[1]][block_position[0]] = '0'
            return False, ['conversation_hero_and_fairy']
        # 捡到道具飞羽
        elif elem in ['30', '31']:
            if elem == '30':
                self.level += 1
                self.life_value += 1000
                self.attack_power += 7
                self.defense_power += 7
                self.obtain_tips = '得到小飞羽 等级提升一级'
            elif elem == '31':
                self.level += 3
                self.life_value += 3000
                self.attack_power += 21
                self.defense_power += 21
                self.obtain_tips = '得到大飞羽 等级提升三级'
            return True, []
        # 捡到幸运十字架
        elif elem in ['32']:
            self.has_cross = True
            self.obtain_tips = ['【幸运十字架】把它交给序章中的仙子', '可以将自身的所有能力提升一些(攻击防御和生命值)']
            return True, []
        # 捡到圣水瓶
        elif elem in ['33']:
            self.life_value *= 2
            self.obtain_tips = '【圣水瓶】它可以将你的体质增加一倍'
            return True, []
        # 捡到圣光徽
        elif elem in ['34']:
            self.has_forecast = True
            self.obtain_tips = '【圣光徽】按L键使用 查看怪物的基本情况'
            return True, []
        # 捡到风之罗盘
        elif elem in ['35']:
            self.has_jump = True
            self.obtain_tips = '【风之罗盘】按J键使用 在已经走过的楼层间进行跳跃'
            return True, []
        # 捡到钥匙盒
        elif elem in ['36']:
            self.num_yellow_keys += 1
            self.num_purple_keys += 1
            self.num_red_keys += 1
            self.obtain_tips = '得到钥匙盒 各种钥匙数加1'
            return True, []
        # 捡到星光神榔
        elif elem in ['38']:
            self.has_hammer = True
            self.obtain_tips = ['【星光神榔】把它交给第四层的小偷', '小偷便会用它打开第十八层的隐藏地面']
            return True, []
        # 捡到金块
        elif elem in ['39']:
            self.num_coins += 300
            self.obtain_tips = '得到金块 金币数加300'
            return True, []
        # 遇到怪物
        elif elem in map_parser.monsters_dict:
            monster = map_parser.monsters_dict[elem]
            if self.winmonster(monster)[0]:
                self.battle(monster, map_parser.element_images[elem][0], map_parser, screen)
                self.num_coins += monster[4]
                self.experience += monster[5]
                self.obtain_tips = f'获得金币数{monster[4]} 经验值{monster[5]}'
                return True, []
            else:
                return False, []
        # 得到铁剑
        elif elem in ['71']:
            self.attack_power += 10
            self.obtain_tips = '得到铁剑 攻击力加10'
            return True, []
        # 得到钢剑
        elif elem in ['73']:
            self.attack_power += 30
            self.obtain_tips = '得到钢剑 攻击力加30'
            return True, []
        # 得到圣光剑
        elif elem in ['75']:
            self.attack_power += 120
            self.obtain_tips = '得到圣光剑 攻击力加120'
            return True, []
        # 得到铁盾
        elif elem in ['76']:
            self.defense_power += 10
            self.obtain_tips = '得到铁盾 防御力加10'
            return True, []
        # 得到钢盾
        elif elem in ['78']:
            self.defense_power += 30
            self.obtain_tips = '得到钢盾 防御力加30'
            return True, []
        # 得到星光盾
        elif elem in ['80']:
            self.defense_power += 120
            self.obtain_tips = '得到星光盾 防御力加120'
            return True, []
        # 其他
        else:
            return False, []
    '''游戏事件提示'''
    def showinfo(self, screen):
        if self.obtain_tips is None: return
        self.show_obtain_tips_count += 1
        if self.show_obtain_tips_count > self.max_obtain_tips_count:
            self.show_obtain_tips_count = 0
            self.obtain_tips = None
        # 画框
        left, top = self.cfg.BLOCKSIZE // 2, 100
        width, height = self.cfg.SCREENSIZE[0] // self.cfg.BLOCKSIZE - 1, 2
        pygame.draw.rect(screen, (199, 97, 20), (left - 4, top - 4, self.cfg.BLOCKSIZE * width + 8, self.cfg.BLOCKSIZE * height + 8), 7)
        for col in range(width):
            for row in range(height):
                image = self.resource_loader.images['mapelements']['0'][0]
                image = pygame.transform.scale(image, (self.cfg.BLOCKSIZE, self.cfg.BLOCKSIZE))
                screen.blit(image, (left + col * self.cfg.BLOCKSIZE, top + row * self.cfg.BLOCKSIZE))
        # 文字
        font = pygame.font.Font(self.fontpath, 30)
        if isinstance(self.obtain_tips, list):
            assert len(self.obtain_tips) == 2
            font_render1 = font.render(self.obtain_tips[0], True, (255, 255, 255))
            font_render2 = font.render(self.obtain_tips[1], True, (255, 255, 255))
            rect1 = font_render1.get_rect()
            rect2 = font_render2.get_rect()
            rect1.midtop = left + width * self.cfg.BLOCKSIZE // 2, top + 10
            rect2.midtop = left + width * self.cfg.BLOCKSIZE // 2, top + 10 + self.blocksize
            screen.blit(font_render1, rect1)
            screen.blit(font_render2, rect2)
        else:
            font_render = font.render(self.obtain_tips, True, (255, 255, 255))
            rect = font_render.get_rect()
            rect.midtop = left + width * self.cfg.BLOCKSIZE // 2, top + height * self.cfg.BLOCKSIZE // 2 - 15
            screen.blit(font_render, rect)
    '''判断勇士是否可以打赢怪物'''
    def winmonster(self, monster):
        # 如果攻击力低于怪物防御力, monster: [名字, 生命值, 攻击力, 防御力, 金币, 经验]
        if self.attack_power <= monster[3]: return False, '???'
        # 如果防御力高于怪物攻击力
        if self.defense_power >= monster[2]: return True, '0'
        # 我方打怪物一次扣多少血
        diff_our = self.attack_power - monster[3]
        # 怪物打我方一次扣多少血
        diff_monster = monster[2] - self.defense_power
        # 计算谁可以win
        if round(monster[1] / diff_our) <= round(self.life_value / diff_monster):
            return True, str(diff_monster * round(monster[1] / diff_our))
        return False, '???'
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
        diff_monster = max(monster[2] - self.defense_power, 0)
        # 更新战斗面板的频率
        update_count, update_interval, update_hero = 0, 5, False
        # 主循环
        clock = pygame.time.Clock()
        font = pygame.font.Font(self.fontpath, 40)
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
                    QuitGame()
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