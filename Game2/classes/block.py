# coding: utf-8
# 作者: Charles
# 公众号: Charles的皮卡丘
# 定义block类，用于随机生成地面块
import random
import cocos
import os


class Block(cocos.sprite.Sprite):
	def __init__(self, position):
		super(Block, self).__init__('black.png')
		# 锚点
		self.image_anchor = 0, 0
		x, y = position
		if x == 0:
			self.scale_x = 4.5
			self.scale_y = 1
		else:
			self.scale_x = 0.5 + random.random() * 1.5
			self.scale_y = min(max(y - 50 + random.random() * 100, 50), 300) / 100.0
			self.position = x + 50 + random.random() * 100, 0