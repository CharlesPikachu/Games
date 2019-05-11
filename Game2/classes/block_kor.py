# coding: utf-8
# 저 자: Charles
# 공공 번호: Charles's Pikachu
# 定义block类，用于随机生成地面块 //블록 종류를 정의하여 무작위로 지상 블록을 생성하는 데 사용?
import random
import cocos
import os


class Block(cocos.sprite.Sprite):
	def __init__(self, position):
		super(Block, self).__init__('black.png')
		# 锚点 // 닻 점?
 		self.image_anchor = 0, 0
		x, y = position
		if x == 0:
			self.scale_x = 4.5
			self.scale_y = 1
		else:
			self.scale_x = 0.5 + random.random() * 1.5
			self.scale_y = min(max(y - 50 + random.random() * 100, 50), 300) / 100.0
			self.position = x + 50 + random.random() * 100, 0