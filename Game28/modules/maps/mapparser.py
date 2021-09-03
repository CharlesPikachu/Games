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
    '''解析'''
    def parse(self, filepath):
        map_matrix = []
        with open(filepath, 'r') as fp:
            for line in fp.readlines():
                line = line.strip()
                if not line: continue
                map_matrix.append([c.strip() for c in line.split(',')])
        return map_matrix
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