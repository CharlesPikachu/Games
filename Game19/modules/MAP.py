'''
Function:
	地图类
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import random
from .Sprites import *


'''.map文件解析器'''
class mapParser():
	def __init__(self, mapfilepath, bg_paths, wall_paths, blocksize, **kwargs):
		self.instances_list = self.__parse(mapfilepath)
		self.bg_paths = bg_paths
		self.wall_paths = wall_paths
		self.blocksize = blocksize
		self.height = len(self.instances_list)
		self.width = len(self.instances_list[0])
		self.screen_size = (blocksize * self.width, blocksize * self.height)
	'''地图画到屏幕上'''
	def draw(self, screen):
		for j in range(self.height):
			for i in range(self.width):
				instance = self.instances_list[j][i]
				if instance == 'w':
					elem = Wall(self.wall_paths[0], [i, j], self.blocksize)
				elif instance == 'x':
					elem = Wall(self.wall_paths[1], [i, j], self.blocksize)
				elif instance == 'z':
					elem = Wall(self.wall_paths[2], [i, j], self.blocksize)
				elif instance == '0':
					elem = Background(self.bg_paths[0], [i, j], self.blocksize)
				elif instance == '1':
					elem = Background(self.bg_paths[1], [i, j], self.blocksize)
				elif instance == '2':
					elem = Background(self.bg_paths[2], [i, j], self.blocksize)
				else:
					raise ValueError('instance parse error in mapParser.draw...')
				elem.draw(screen)
	'''随机获取一个空地'''
	def randomGetSpace(self, used_spaces=None):
		while True:
			i = random.randint(0, self.width-1)
			j = random.randint(0, self.height-1)
			coordinate = [i, j]
			if used_spaces and coordinate in used_spaces:
				continue
			instance = self.instances_list[j][i]
			if instance in ['0', '1', '2']:
				break
		return coordinate
	'''根据坐标获取元素类型'''
	def getElemByCoordinate(self, coordinate):
		return self.instances_list[coordinate[1]][coordinate[0]]
	'''解析.map文件'''
	def __parse(self, mapfilepath):
		instances_list = []
		with open(mapfilepath) as f:
			for line in f.readlines():
				instances_line_list = []
				for c in line:
					if c in ['w', 'x', 'z', '0', '1', '2']:
						instances_line_list.append(c)
				instances_list.append(instances_line_list)
		return instances_list