'''
Function:
    游戏地图解析类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import pygame


'''游戏地图解析类'''
class MapParser():
    def __init__(self, blocksize, filepath, element_images, offset=(0, 0), **kwargs):
        self.count = 0
        self.switch_times = 15
        self.image_pointer = 0
        self.offset = offset
        self.blocksize = blocksize
        self.element_images = element_images
        self.map_matrix = self.parse(filepath)
        self.map_size = (len(self.map_matrix), len(self.map_matrix[0]))
        # 地图上所有怪物的属性: 名字, 生命值, 攻击力, 防御力, 金币, 经验
        self.monsters_dict = {
            '40': ('绿头怪', 50, 20, 1, 1, 1),
            '41': ('红头怪', 70, 15, 2, 2, 2),
            '42': ('小蝙蝠', 100, 20, 5, 3, 3),
            '43': ('青头怪', 200, 35, 10, 5, 5),
            '44': ('骷髅人', 110, 25, 5, 5, 4),
            '45': ('骷髅士兵', 150, 40, 20, 8, 6),
            '46': ('兽面人', 300, 75, 45, 13, 10),
            '47': ('初级卫兵', 450, 150, 90, 22, 19),
            '48': ('大蝙蝠', 150, 65, 30, 10, 8),
            '49': ('红蝙蝠', 550, 160, 90, 25, 20),
            '50': ('白衣武士', 1300, 300, 150, 40, 35),
            '51': ('怪王', 700, 250, 125, 32, 30),
            '52': ('红衣法师', 500, 400, 260, 47, 45),
            '53': ('红衣魔王', 15000, 1000, 1000, 100, 100),
            '54': ('金甲卫士', 850, 350, 200, 45, 40),
            '55': ('金甲队长', 900, 750, 650, 77, 70),
            '56': ('骷髅队长', 400, 90, 50, 15, 12),
            '57': ('灵法师', 1500, 830, 730, 80, 70),
            '58': ('灵武士', 1200, 980, 900, 88, 75),
            '59': ('冥灵魔王', 30000, 1700, 1500, 250, 220),
            '60': ('麻衣法师', 250, 120, 70, 20, 17),
            '61': ('冥战士', 2000, 680, 590, 70, 65),
            '62': ('冥队长', 2500, 900, 850, 84, 75),
            '63': ('初级法师', 125, 50, 25, 10, 7),
            '64': ('高级法师', 100, 200, 110, 30, 25),
            '65': ('石头怪人', 500, 115, 65, 15, 15),
            '66': ('兽面战士', 900, 450, 330, 50, 50),
            '67': ('双手剑士', 1200, 620, 520, 65, 75),
            '68': ('冥卫兵', 1250, 500, 400, 55, 55),
            '69': ('高级卫兵', 1500, 560, 460, 60, 60),
            '70': ('影子战士', 3100, 1150, 1050, 92, 80),
            '188': ('血影', 99999, 5000, 4000, 0, 0),
            '198': ('魔龙', 99999, 9999, 5000, 0, 0),
        }
    '''解析'''
    def parse(self, filepath):
        map_matrix = []
        with open(filepath, 'r') as fp:
            for line in fp.readlines():
                line = line.strip()
                if not line: continue
                map_matrix.append([c.strip() for c in line.split(',')])
        return map_matrix
    '''获得所有怪物信息'''
    def getallmonsters(self):
        monsters = []
        for row_idx, row in enumerate(self.map_matrix):
            for col_idx, elem in enumerate(row):
                if elem in self.monsters_dict:
                    monster = list(self.monsters_dict[elem])
                    monster.append(elem)
                    monsters.append(tuple(monster))
        return list(set(monsters))
    '''获得英雄的位置'''
    def getheroposition(self, pos_type='block'):
        assert pos_type in ['pixel', 'block']
        for row_idx, row in enumerate(self.map_matrix):
            for col_idx, elem in enumerate(row):
                position = col_idx * self.blocksize + self.offset[0], row_idx * self.blocksize + self.offset[1]
                if elem == 'hero':
                    if pos_type == 'pixel': return position
                    else: return (col_idx, row_idx)
        return None
    '''将游戏地图画到屏幕上'''
    def draw(self, screen):
        self.count += 1
        if self.count == self.switch_times:
            self.count = 0
            self.image_pointer = int(not self.image_pointer)
        for row_idx, row in enumerate(self.map_matrix):
            for col_idx, elem in enumerate(row):
                position = col_idx * self.blocksize + self.offset[0], row_idx * self.blocksize + self.offset[1]
                if elem in self.element_images:
                    image = self.element_images[elem][self.image_pointer]
                    image = pygame.transform.scale(image, (self.blocksize, self.blocksize))
                    screen.blit(image, position)
                elif elem in ['00', 'hero']:
                    image = self.element_images['0'][self.image_pointer]
                    image = pygame.transform.scale(image, (self.blocksize, self.blocksize))
                    screen.blit(image, position)