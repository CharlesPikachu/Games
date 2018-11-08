'''
Function:
	工具模块
Author:
	Charles
公众号:
	Charles的皮卡丘
'''
import random
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor, QPainter


'''
Function:
	定义一个俄罗斯方块的形状
'''
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
		return [[x+i, y+j] for i, j in self.getRotatedRelativeCoords(direction)]
	'''获得相对坐标的边界'''
	def getRelativeBoundary(self, direction):
		relative_coords_now = self.getRotatedRelativeCoords(direction)
		xs = [i[0] for i in relative_coords_now]
		ys = [i[1] for i in relative_coords_now]
		return min(xs), max(xs), min(ys), max(ys)


'''
Function:
	内部板块
'''
class InnerBoard():
	def __init__(self, width=10, height=22):
		# 宽和长, 单位长度为小方块边长
		self.width = width
		self.height = height
		self.reset()
	'''判断当前俄罗斯方块是否可以移动到某位置'''
	def ableMove(self, coord, direction=None):
		assert len(coord) == 2
		if direction is None:
			direction = self.current_direction
		for x, y in self.current_tetris.getAbsoluteCoords(direction, coord[0], coord[1]):
			# 超出边界
			if x >= self.width or x < 0 or y >= self.height or y < 0:
				return False
			# 该位置有俄罗斯方块了
			if self.getCoordValue([x, y]) > 0:
				return False
		return True
	'''向右移动'''
	def moveRight(self):
		if self.ableMove([self.current_coord[0]+1, self.current_coord[1]]):
			self.current_coord[0] += 1
	'''向左移动'''
	def moveLeft(self):
		if self.ableMove([self.current_coord[0]-1, self.current_coord[1]]):
			self.current_coord[0] -= 1
	'''顺时针转'''
	def rotateClockwise(self):
		if self.ableMove(self.current_coord, (self.current_direction-1) % 4):
			self.current_direction = (self.current_direction-1) % 4
	'''逆时针转'''
	def rotateAnticlockwise(self):
		if self.ableMove(self.current_coord, (self.current_direction+1) % 4):
			self.current_direction = (self.current_direction+1) % 4
	'''向下移动'''
	def moveDown(self):
		removed_lines = 0
		if self.ableMove([self.current_coord[0], self.current_coord[1]+1]):
			self.current_coord[1] += 1
		else:
			x_min, x_max, y_min, y_max = self.current_tetris.getRelativeBoundary(self.current_direction)
			# 简单起见, 有超出屏幕就判定游戏结束
			if self.current_coord[1] + y_min < 0:
				self.is_gameover = True
				return removed_lines
			self.mergeTetris()
			removed_lines = self.removeFullLines()
			self.createNewTetris()
		return removed_lines
	'''坠落'''
	def dropDown(self):
		while self.ableMove([self.current_coord[0], self.current_coord[1]+1]):
			self.current_coord[1] += 1
		x_min, x_max, y_min, y_max = self.current_tetris.getRelativeBoundary(self.current_direction)
		# 简单起见, 有超出屏幕就判定游戏结束
		if self.current_coord[1] + y_min < 0:
			self.is_gameover = True
			return removed_lines
		self.mergeTetris()
		removed_lines = self.removeFullLines()
		self.createNewTetris()
		return removed_lines
	'''合并俄罗斯方块(最下面定型不能再动的那些)'''
	def mergeTetris(self):
		for x, y in self.current_tetris.getAbsoluteCoords(self.current_direction, self.current_coord[0], self.current_coord[1]):
			self.board_data[x + y * self.width] = self.current_tetris.shape
		self.current_coord = [-1, -1]
		self.current_direction = 0
		self.current_tetris = tetrisShape()
	'''移出整行都有小方块的'''
	def removeFullLines(self):
		new_board_data = [0] * self.width * self.height
		new_y = self.height - 1
		removed_lines = 0
		for y in range(self.height-1, -1, -1):
			cell_count = sum([1 if self.board_data[x + y * self.width] > 0 else 0 for x in range(self.width)])
			if cell_count < self.width:
				for x in range(self.width):
					new_board_data[x + new_y * self.width] = self.board_data[x + y * self.width]
				new_y -= 1
			else:
				removed_lines += 1
		self.board_data = new_board_data
		return removed_lines
	'''创建新的俄罗斯方块(即将next_tetris变为current_tetris)'''
	def createNewTetris(self):
		x_min, x_max, y_min, y_max = self.next_tetris.getRelativeBoundary(0)
		# y_min肯定是-1
		if self.ableMove([self.init_x, -y_min]):
			self.current_coord = [self.init_x, -y_min]
			self.current_tetris = self.next_tetris
			self.next_tetris = self.getNextTetris()
		else:
			self.is_gameover = True
		self.shape_statistics[self.current_tetris.shape] += 1
	'''获得下个俄罗斯方块'''
	def getNextTetris(self):
		return tetrisShape(random.randint(1, 7))
	'''获得板块数据'''
	def getBoardData(self):
		return self.board_data
	'''获得板块数据上某坐标的值'''
	def getCoordValue(self, coord):
		return self.board_data[coord[0] + coord[1] * self.width]
	'''获得俄罗斯方块各个小块的绝对坐标'''
	def getCurrentTetrisCoords(self):
		return self.current_tetris.getAbsoluteCoords(self.current_direction, self.current_coord[0], self.current_coord[1])
	'''重置'''
	def reset(self):
		# 记录板块数据
		self.board_data = [0] * self.width * self.height
		# 当前俄罗斯方块的旋转状态
		self.current_direction = 0
		# 当前俄罗斯方块的坐标, 单位长度为小方块边长
		self.current_coord = [-1, -1]
		# 下一个俄罗斯方块
		self.next_tetris = self.getNextTetris()
		# 当前俄罗斯方块
		self.current_tetris = tetrisShape()
		# 游戏是否结束
		self.is_gameover = False
		# 俄罗斯方块的初始x位置
		self.init_x = self.width // 2
		# 形状数量统计
		self.shape_statistics = [0] * 8


'''
Function:
	外部板块
'''
class ExternalBoard(QFrame):
	score_signal = pyqtSignal(str)
	def __init__(self, parent, grid_size, inner_board):
		super().__init__(parent)
		self.grid_size = grid_size
		self.inner_board = inner_board
		self.setFixedSize(grid_size * inner_board.width, grid_size * inner_board.height)
		self.initExternalBoard()
	'''外部板块初始化'''
	def initExternalBoard(self):
		self.score = 0
	'''把内部板块结构画出来'''
	def paintEvent(self, event):
		painter = QPainter(self)
		for x in range(self.inner_board.width):
			for y in range(self.inner_board.height):
				shape = self.inner_board.getCoordValue([x, y])
				drawCell(painter, x * self.grid_size, y * self.grid_size, shape, self.grid_size)
		for x, y in self.inner_board.getCurrentTetrisCoords():
			shape = self.inner_board.current_tetris.shape
			drawCell(painter, x * self.grid_size, y * self.grid_size, shape, self.grid_size)
		painter.setPen(QColor(0x777777))
		painter.drawLine(0, self.height()-1, self.width(), self.height()-1)
		painter.drawLine(self.width()-1, 0, self.width()-1, self.height())
		painter.setPen(QColor(0xCCCCCC))
		painter.drawLine(self.width(), 0, self.width(), self.height())
		painter.drawLine(0, self.height(), self.width(), self.height())
	'''数据更新'''
	def updateData(self):
		self.score_signal.emit(str(self.score))
		self.update()


'''
Function:
	侧面板, 右边显示下一个俄罗斯方块的形状
'''
class SidePanel(QFrame):
	def __init__(self, parent, grid_size, inner_board):
		super().__init__(parent)
		self.grid_size = grid_size
		self.inner_board = inner_board
		self.setFixedSize(grid_size * 5, grid_size * inner_board.height)
		self.move(grid_size * inner_board.width, 0)
	'''画侧面板'''
	def paintEvent(self, event):
		painter = QPainter(self)
		x_min, x_max, y_min, y_max = self.inner_board.next_tetris.getRelativeBoundary(0)
		dy = 3 * self.grid_size
		dx = (self.width() - (x_max - x_min) * self.grid_size) / 2
		shape = self.inner_board.next_tetris.shape
		for x, y in self.inner_board.next_tetris.getAbsoluteCoords(0, 0, -y_min):
			drawCell(painter, x * self.grid_size + dx, y * self.grid_size + dy, shape, self.grid_size)
	'''更新数据'''
	def updateData(self):
		self.update()


'''
Function:
	给板块的一个Cell填色
'''
def drawCell(painter, x, y, shape, grid_size):
	colors = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC, 0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]
	if shape == 0:
		return
	color = QColor(colors[shape])
	painter.fillRect(x+1, y+1, grid_size-2, grid_size-2, color)
	painter.setPen(color.lighter())
	painter.drawLine(x, y+grid_size-1, x, y)
	painter.drawLine(x, y, x+grid_size-1, y)
	painter.setPen(color.darker())
	painter.drawLine(x+1, y+grid_size-1, x+grid_size-1, y+grid_size-1)
	painter.drawLine(x+grid_size-1, y+grid_size-1, x+grid_size-1, y+1)