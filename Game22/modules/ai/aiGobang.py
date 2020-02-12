'''
Function:
    实现五子棋AI算法
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import random
from itertools import product


class aiGobang():
    def __init__(self, ai_color, player_color, search_depth=1, **kwargs):
        assert search_depth % 2, 'search_depth must be odd number'
        self.ai_color = ai_color
        self.player_color = player_color
        self.search_depth = search_depth
        self.score_model = [(50, (0, 1, 1, 0, 0)), (50, (0, 0, 1, 1, 0)), (200, (1, 1, 0, 1, 0)),
                            (500, (0, 0, 1, 1, 1)), (500, (1, 1, 1, 0, 0)), (5000, (0, 1, 1, 1, 0)),
                            (5000, (0, 1, 0, 1, 1, 0)), (5000, (0, 1, 1, 0, 1, 0)), (5000, (1, 1, 1, 0, 1)),
                            (5000, (1, 1, 0, 1, 1)), (5000, (1, 0, 1, 1, 1)), (5000, (1, 1, 1, 1, 0)),
                            (5000, (0, 1, 1, 1, 1)), (50000, (0, 1, 1, 1, 1, 0)), (99999999, (1, 1, 1, 1, 1))]
        self.alpha = -99999999
        self.beta = 99999999
        self.all_list = [(i, j) for i, j in product(range(19), range(19))]
    '''外部调用'''
    def act(self, history_record):
        self.ai_list = []
        self.player_list = []
        self.aiplayer_list = []
        for item in history_record:
            self.aiplayer_list.append((item[0], item[1]))
            if item[-1] == self.ai_color:
                self.ai_list.append((item[0], item[1]))
            elif item[-1] == self.player_color:
                self.player_list.append((item[0], item[1]))
        while True:
            self.next_point = random.choice(range(19)), random.choice(range(19))
            if self.next_point not in self.aiplayer_list:
                break
        self.__doSearch(True, self.search_depth, self.alpha, self.beta)
        return self.next_point
    '''负极大值搜索, alpha+beta剪枝'''
    def __doSearch(self, is_ai_round, depth, alpha, beta):
        if self.__isgameover(self.ai_list) or self.__isgameover(self.player_list) or depth == 0:
            return self.__evaluation(is_ai_round)
        blank_list = list(set(self.all_list).difference(set(self.aiplayer_list)))
        blank_list = self.__rearrange(blank_list)
        for next_step in blank_list:
            if not self.__hasNeighbor(next_step):
                continue
            if is_ai_round:
                self.ai_list.append(next_step)
            else:
                self.player_list.append(next_step)
            self.aiplayer_list.append(next_step)
            value = -self.__doSearch(not is_ai_round, depth-1, -beta, -alpha)
            if is_ai_round:
                self.ai_list.remove(next_step)
            else:
                self.player_list.remove(next_step)
            self.aiplayer_list.remove(next_step)
            if value > alpha:
                if depth == self.search_depth:
                    self.next_point = next_step
                if value >= beta:
                    return beta
                alpha = value
        return alpha
    '''游戏是否结束了'''
    def __isgameover(self, oneslist):
        for i, j in product(range(19), range(19)):
            if i < 15 and (i, j) in oneslist and (i+1, j) in oneslist and (i+2, j) in oneslist and (i+3, j) in oneslist and (i+4, j) in oneslist:
                return True
            elif j < 15 and (i, j) in oneslist and (i, j+1) in oneslist and (i, j+2) in oneslist and (i, j+3) in oneslist and (i, j+4) in oneslist:
                return True
            elif i < 15 and j < 15 and (i, j) in oneslist and (i+1, j+1) in oneslist and (i+2, j+2) in oneslist and (i+3, j+3) in oneslist and (i+4, j+4) in oneslist:
                return True
            elif i > 3 and j < 15 and (i, j) in oneslist and (i-1, j+1) in oneslist and (i-2, j+2) in oneslist and (i-3, j+3) in oneslist and (i-4, j+4) in oneslist:
                return True
        return False
    '''重新排列未落子位置'''
    def __rearrange(self, blank_list):
        last_step = self.aiplayer_list[-1]
        for item in blank_list:
            for i, j in product(range(-1, 2), range(-1, 2)):
                if i == 0 and j == 0:
                    continue
                next_step = (last_step[0]+i, last_step[1]+j)
                if next_step in blank_list:
                    blank_list.remove(next_step)
                    blank_list.insert(0, next_step)
        return blank_list
    '''是否存在近邻'''
    def __hasNeighbor(self, next_step):
        for i, j in product(range(-1, 2), range(-1, 2)):
            if i == 0 and j == 0:
                continue
            if (next_step[0]+i, next_step[1]+j) in self.aiplayer_list:
                return True
        return False
    '''计算得分'''
    def __calcScore(self, i, j, x_direction, y_direction, list1, list2, all_scores):
        add_score = 0
        max_score = (0, None)
        for each in all_scores:
            for item in each[1]:
                if i == item[0] and j == item[1] and x_direction == each[2][0] and y_direction == each[2][1]:
                    return 0, all_scores
        for noffset in range(-5, 1):
            position = []
            for poffset in range(6):
                x, y = i + (poffset + noffset) * x_direction, j + (poffset + noffset) * y_direction
                if (x, y) in list2:
                    position.append(2)
                elif (x, y) in list1:
                    position.append(1)
                else:
                    position.append(0)
            shape_len5 = tuple(position[0: -1])
            shape_len6 = tuple(position)
            for score, shape in self.score_model:
                if shape_len5 == shape or shape_len6 == shape:
                    if score > max_score[0]:
                        max_score = (score, ((i + (0 + noffset) * x_direction, j + (0 + noffset) * y_direction),
                                             (i + (1 + noffset) * x_direction, j + (1 + noffset) * y_direction),
                                             (i + (2 + noffset) * x_direction, j + (2 + noffset) * y_direction),
                                             (i + (3 + noffset) * x_direction, j + (3 + noffset) * y_direction),
                                             (i + (4 + noffset) * x_direction, j + (4 + noffset) * y_direction)), (x_direction, y_direction))
        if max_score[1] is not None:
            for each in all_scores:
                for p1 in each[1]:
                    for p2 in max_score[1]:
                        if p1 == p2 and max_score[0] > 10 and each[0] > 10:
                            add_score += max_score[0] + each[0]
            all_scores.append(max_score)
        return add_score+max_score[0], all_scores
    '''评估函数'''
    def __evaluation(self, is_ai_round):
        if is_ai_round:
            list1 = self.ai_list
            list2 = self.player_list
        else:
            list2 = self.ai_list
            list1 = self.player_list
        active_all_scores = []
        active_score = 0
        for item in list1:
            score, active_all_scores = self.__calcScore(item[0], item[1], 0, 1, list1, list2, active_all_scores)
            active_score += score
            score, active_all_scores = self.__calcScore(item[0], item[1], 1, 0, list1, list2, active_all_scores)
            active_score += score
            score, active_all_scores = self.__calcScore(item[0], item[1], 1, 1, list1, list2, active_all_scores)
            active_score += score
            score, active_all_scores = self.__calcScore(item[0], item[1], -1, 1, list1, list2, active_all_scores)
            active_score += score
        passive_all_scores = []
        passive_score = 0
        for item in list2:
            score, passive_all_scores = self.__calcScore(item[0], item[1], 0, 1, list2, list1, passive_all_scores)
            passive_score += score
            score, passive_all_scores = self.__calcScore(item[0], item[1], 1, 0, list2, list1, passive_all_scores)
            passive_score += score
            score, passive_all_scores = self.__calcScore(item[0], item[1], 1, 1, list2, list1, passive_all_scores)
            passive_score += score
            score, passive_all_scores = self.__calcScore(item[0], item[1], -1, 1, list2, list1, passive_all_scores)
            passive_score += score
        total_score = active_score - passive_score * 0.1
        return total_score