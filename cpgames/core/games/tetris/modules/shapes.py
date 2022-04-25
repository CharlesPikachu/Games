'''
Function:
    定义俄罗斯方块的形状
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
'''定义一个俄罗斯方块的形状'''
class tetrisShape():
    def __init__(self, shape=0):
        # 空块
        self.shape_empty = 0
        # 一字型块
        self.shape_I = 1
        # L型块
        self.shape_L = 2
        # 向左的L型块
        self.shape_J = 3
        # T型块
        self.shape_T = 4
        # 田字型块
        self.shape_O = 5
        # 反向Z型块
        self.shape_S = 6
        # Z型块
        self.shape_Z = 7
        # 每种块包含的四个小方块相对坐标分布
        self.shapes_relative_coords = [
            [[0, 0], [0, 0], [0, 0], [0, 0]],
            [[0, -1], [0, 0], [0, 1], [0, 2]],
            [[0, -1], [0, 0], [0, 1], [1, 1]],
            [[0, -1], [0, 0], [0, 1], [-1, 1]],
            [[0, -1], [0, 0], [0, 1], [1, 0]],
            [[0, 0], [0, -1], [1, 0], [1, -1]],
            [[0, 0], [0, -1], [-1, 0], [1, -1]],
            [[0, 0], [0, -1], [1, 0], [-1, -1]]
        ]
        self.shape = shape
        self.relative_coords = self.shapes_relative_coords[self.shape]
    '''获得该形状当前旋转状态的四个小方块的相对坐标分布'''
    def getRotatedRelativeCoords(self, direction):
        # 初始分布
        if direction == 0 or self.shape == self.shape_O:
            return self.relative_coords
        # 逆时针旋转90度
        if direction == 1:
            return [[-y, x] for x, y in self.relative_coords]
        # 逆时针旋转180度
        if direction == 2:
            if self.shape in [self.shape_I, self.shape_Z, self.shape_S]:
                return self.relative_coords
            else:
                return [[-x, -y] for x, y in self.relative_coords]
        # 逆时针旋转270度
        if direction == 3:
            if self.shape in [self.shape_I, self.shape_Z, self.shape_S]:
                return [[-y, x] for x, y in self.relative_coords]
            else:
                return [[y, -x] for x, y in self.relative_coords]
    '''获得该俄罗斯方块的各个小块绝对坐标'''
    def getAbsoluteCoords(self, direction, x, y):
        return [[x + i, y + j] for i, j in self.getRotatedRelativeCoords(direction)]
    '''获得相对坐标的边界'''
    def getRelativeBoundary(self, direction):
        relative_coords_now = self.getRotatedRelativeCoords(direction)
        xs = [i[0] for i in relative_coords_now]
        ys = [i[1] for i in relative_coords_now]
        return min(xs), max(xs), min(ys), max(ys)