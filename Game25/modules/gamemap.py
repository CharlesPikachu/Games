'''
Function:
    定义游戏地图
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import random
from .mine import Mine


'''扫雷地图'''
'''Mine map'''
class MinesweeperMap():
    def __init__(self, cfg, images, **kwargs):
        self.cfg = cfg
        # 雷型矩阵
        self.mines_matrix = []
        for j in range(cfg.GAME_MATRIX_SIZE[1]):
            mines_line = []
            for i in range(cfg.GAME_MATRIX_SIZE[0]):
                position = i * cfg.GRIDSIZE + cfg.BORDERSIZE, (j + 2) * cfg.GRIDSIZE
                mines_line.append(Mine(images=images, position=position))
            self.mines_matrix.append(mines_line)
        # 随机埋雷
        for i in random.sample(range(cfg.GAME_MATRIX_SIZE[0]*cfg.GAME_MATRIX_SIZE[1]), cfg.NUM_MINES):
            self.mines_matrix[i//cfg.GAME_MATRIX_SIZE[0]][i%cfg.GAME_MATRIX_SIZE[0]].burymine()
        count = 0
        for item in self.mines_matrix:
            for i in item:
                count += int(i.is_mine_flag)
        # 游戏当前的状态
        self.status_code = -1
        # 记录鼠标按下时的位置和按的键
        self.mouse_pos = None
        self.mouse_pressed = None
    '''画出当前的游戏状态图'''
    '''Draw a picture of the current state of the game'''
    def draw(self, screen):
        for row in self.mines_matrix:
            for item in row: item.draw(screen)
    '''设置当前的游戏状态'''
    '''Set the current state of the game'''
    def setstatus(self, status_code):
        # 0: 正在进行游戏, 1: 游戏结束, -1: 游戏还没开始
        self.status_code = status_code
    '''根据玩家的鼠标操作情况更新当前的游戏状态地图'''
    '''Updates the current game state map based on the player's mouse movements'''
    def update(self, mouse_pressed=None, mouse_pos=None, type_='down'):
        assert type_ in ['down', 'up']
        # 记录鼠标按下时的位置和按的键
        if type_ == 'down' and mouse_pos is not None and mouse_pressed is not None:
            self.mouse_pos = mouse_pos
            self.mouse_pressed = mouse_pressed
        # 鼠标点击的范围不在游戏地图内, 无响应
        if self.mouse_pos[0] < self.cfg.BORDERSIZE or self.mouse_pos[0] > self.cfg.SCREENSIZE[0] - self.cfg.BORDERSIZE or \
           self.mouse_pos[1] < self.cfg.GRIDSIZE * 2 or self.mouse_pos[1] > self.cfg.SCREENSIZE[1] - self.cfg.BORDERSIZE:
            return
        # 鼠标点击在游戏地图内, 代表开始游戏(即可以开始计时了)
        if self.status_code == -1:
            self.status_code = 0
        # 如果不是正在游戏中, 按鼠标是没有用的
        if self.status_code != 0:
            return
        # 鼠标位置转矩阵索引
        coord_x = (self.mouse_pos[0] - self.cfg.BORDERSIZE) // self.cfg.GRIDSIZE
        coord_y = self.mouse_pos[1] // self.cfg.GRIDSIZE - 2
        mine_clicked = self.mines_matrix[coord_y][coord_x]
        # 鼠标按下
        if type_ == 'down':
            # --鼠标左右键同时按下
            if self.mouse_pressed[0] and self.mouse_pressed[2]:
                if mine_clicked.opened and mine_clicked.num_mines_around > 0:
                    mine_clicked.setstatus(status_code=4)
                    num_flags = 0
                    coords_around = self.getaround(coord_y, coord_x)
                    for (j, i) in coords_around:
                        if self.mines_matrix[j][i].status_code == 2:
                            num_flags += 1
                    if num_flags == mine_clicked.num_mines_around:
                        for (j, i) in coords_around:
                            if self.mines_matrix[j][i].status_code == 0:
                                self.openmine(i, j)
                    else:
                        for (j, i) in coords_around:
                            if self.mines_matrix[j][i].status_code == 0:
                                self.mines_matrix[j][i].setstatus(status_code=5)
        # 鼠标释放
        else:
            # --鼠标左键
            if self.mouse_pressed[0] and not self.mouse_pressed[2]:
                if not (mine_clicked.status_code == 2 or mine_clicked.status_code == 3):
                    if self.openmine(coord_x, coord_y):
                        self.setstatus(status_code=1)
            # --鼠标右键
            elif self.mouse_pressed[2] and not self.mouse_pressed[0]:
                if mine_clicked.status_code == 0:
                    mine_clicked.setstatus(status_code=2)
                elif mine_clicked.status_code == 2:
                    mine_clicked.setstatus(status_code=3)
                elif mine_clicked.status_code == 3:
                    mine_clicked.setstatus(status_code=0)
            # --鼠标左右键同时按下
            elif self.mouse_pressed[0] and self.mouse_pressed[2]:
                mine_clicked.setstatus(status_code=1)
                coords_around = self.getaround(coord_y, coord_x)
                for (j, i) in coords_around:
                    if self.mines_matrix[j][i].status_code == 5:
                        self.mines_matrix[j][i].setstatus(status_code=0)
    '''打开雷'''
    ''' Open mine '''
    def openmine(self, x, y):
        mine_clicked = self.mines_matrix[y][x]
        if mine_clicked.is_mine_flag:
            for row in self.mines_matrix:
                for item in row:
                    if not item.is_mine_flag and item.status_code == 2:
                        item.setstatus(status_code=7)
                    elif item.is_mine_flag and item.status_code == 0:
                        item.setstatus(status_code=1)
            mine_clicked.setstatus(status_code=6)
            return True
        mine_clicked.setstatus(status_code=1)
        coords_around = self.getaround(y, x)
        num_mines = 0
        for (j, i) in coords_around:
            num_mines += int(self.mines_matrix[j][i].is_mine_flag)
        mine_clicked.setnumminesaround(num_mines)
        if num_mines == 0:
            for (j, i) in coords_around:
                if self.mines_matrix[j][i].num_mines_around == -1:
                    self.openmine(i, j)
        return False
    '''获得坐标点的周围坐标点'''
    ''' get around '''
    def getaround(self, row, col):
        coords = []
        for j in range(max(0, row-1), min(row+1, self.cfg.GAME_MATRIX_SIZE[1]-1)+1):
            for i in range(max(0, col-1), min(col+1, self.cfg.GAME_MATRIX_SIZE[0]-1)+1):
                if j == row and i == col:
                    continue
                coords.append((j, i))
        return coords
    '''是否正在游戏中'''
    ''' Whether it is in the game '''
    @property
    def gaming(self):
        return self.status_code == 0
    '''被标记为雷的雷数目'''
    ''' Number of mines marked as mines '''
    @property
    def flags(self):
        num_flags = 0
        for row in self.mines_matrix:
            for item in row: num_flags += int(item.status_code == 2)
        return num_flags
    '''已经打开的雷的数目'''
    '''Number of mines that have been opened'''
    @property
    def openeds(self):
        num_openeds = 0
        for row in self.mines_matrix:
            for item in row: num_openeds += int(item.opened)
        return num_openeds