'''
Function:
    定义2048小游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import copy
import random
import pygame


'''2048游戏'''
class Game2048(object):
    def __init__(self, matrix_size=(4, 4), max_score_filepath=None, **kwargs):
        # matrix_size: (num_rows, num_cols)
        self.matrix_size = matrix_size
        # 游戏最高分保存路径
        self.max_score_filepath = max_score_filepath
        # 初始化
        self.initialize()
    '''更新游戏状态'''
    def update(self):
        game_matrix_before = copy.deepcopy(self.game_matrix)
        self.move()
        if game_matrix_before != self.game_matrix: self.randomGenerateNumber()
        if self.score > self.max_score: self.max_score = self.score
    '''根据指定的方向, 移动所有数字块'''
    def move(self):
        # 提取非空数字
        def extract(array):
            array_new = []
            for item in array:
                if item != 'null': array_new.append(item)
            return array_new
        # 合并非空数字
        def merge(array):
            score = 0
            if len(array) < 2: return array, score
            for i in range(len(array)-1):
                if array[i] == 'null':
                    break
                if array[i] == array[i+1]:
                    array[i] *= 2
                    array.pop(i+1)
                    array.append('null')
                    score += array[i]
            return extract(array), score
        # 不需要移动的话直接return
        if self.move_direction is None: return
        # 向上
        if self.move_direction == 'up':
            for j in range(self.matrix_size[1]):
                col = []
                for i in range(self.matrix_size[0]):
                    col.append(self.game_matrix[i][j])
                col = extract(col)
                col.reverse()
                col, score = merge(col)
                self.score += score
                col.reverse()
                col = col + ['null',] * (self.matrix_size[0] - len(col))
                for i in range(self.matrix_size[0]):
                    self.game_matrix[i][j] = col[i]
        # 向下
        elif self.move_direction == 'down':
            for j in range(self.matrix_size[1]):
                col = []
                for i in range(self.matrix_size[0]):
                    col.append(self.game_matrix[i][j])
                col = extract(col)
                col, score = merge(col)
                self.score += score
                col = ['null',] * (self.matrix_size[0] - len(col)) + col
                for i in range(self.matrix_size[0]):
                    self.game_matrix[i][j] = col[i]
        # 向左
        elif self.move_direction == 'left':
            for idx, row in enumerate(copy.deepcopy(self.game_matrix)):
                row = extract(row)
                row.reverse()
                row, score = merge(row)
                self.score += score
                row.reverse()
                row = row + ['null',] * (self.matrix_size[1] - len(row))
                self.game_matrix[idx] = row
        # 向右
        elif self.move_direction == 'right':
            for idx, row in enumerate(copy.deepcopy(self.game_matrix)):
                row = extract(row)
                row, score = merge(row)
                self.score += score
                row = ['null',] * (self.matrix_size[1] - len(row)) + row
                self.game_matrix[idx] = row
        self.move_direction = None
    '''在新的位置随机生成数字'''
    def randomGenerateNumber(self):
        empty_pos = []
        for i in range(self.matrix_size[0]):
            for j in range(self.matrix_size[1]):
                if self.game_matrix[i][j] == 'null': empty_pos.append([i, j])
        i, j = random.choice(empty_pos)
        self.game_matrix[i][j] = 2 if random.random() > 0.1 else 4
    '''初始化'''
    def initialize(self):
        self.game_matrix = [['null' for _ in range(self.matrix_size[1])] for _ in range(self.matrix_size[0])]
        self.score = 0
        self.max_score = self.readMaxScore()
        self.move_direction = None
        self.randomGenerateNumber()
        self.randomGenerateNumber()
    '''设置移动方向'''
    def setDirection(self, direction):
        assert direction in ['up', 'down', 'left', 'right']
        self.move_direction = direction
    '''保存最高分'''
    def saveMaxScore(self):
        f = open(self.max_score_filepath, 'w', encoding='utf-8')
        f.write(str(self.max_score))
        f.close()
    '''读取游戏最高分'''
    def readMaxScore(self):
        try:
            f = open(self.max_score_filepath, 'r', encoding='utf-8')
            score = int(f.read().strip())
            f.close()
            return score
        except:
            return 0
    '''游戏是否结束'''
    @property
    def isgameover(self):
        for i in range(self.matrix_size[0]):
            for j in range(self.matrix_size[1]):
                if self.game_matrix[i][j] == 'null': return False
                if (i == self.matrix_size[0] - 1) and (j == self.matrix_size[1] - 1):
                    continue
                elif (i == self.matrix_size[0] - 1):
                    if (self.game_matrix[i][j] == self.game_matrix[i][j+1]):
                        return False
                elif (j == self.matrix_size[1] - 1):
                    if (self.game_matrix[i][j] == self.game_matrix[i+1][j]):
                        return False
                else:
                    if (self.game_matrix[i][j] == self.game_matrix[i+1][j]) or (self.game_matrix[i][j] == self.game_matrix[i][j+1]):
                        return False
        return True