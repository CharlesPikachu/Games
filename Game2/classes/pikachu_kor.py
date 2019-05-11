# coding: utf-8
# 저자: Charles
# 공공 번호: Charles's Pikachu
# 피카츄 클래스 정의(Define Pikachu Class)
import cocos
import os


class Pikachu(cocos.sprite.Sprite):
	def __init__(self):
		super(Pikachu, self).__init__('pikachu.png')
		# 점프 가능 여부
		self.able_jump = False
		# 속도
		self.speed = 0
		# 锚点 // 닻점?
 		self.image_anchor = 0, 0
		#피카츄의 위치
		self.position = 80, 280
		self.schedule(self.update)
	# 声控跳跃 // 사운드 점프?
	def jump(self, h):
		if self.able_jump:
			self.y += 1
			self.speed -= max(min(h, 10), 7)
			self.able_jump = False
	# 착륙 후 정지
	def land(self, y):
		if self.y > y - 25:
			self.able_jump = True
			self.speed = 0
			self.y = y
	# 更新(重力下降) //갱신(중력하강)?
 	def update(self, dt):
		self.speed += 10 * dt
		self.y -= self.speed
		if self.y < -85:
			self.reset()
	# 리셋
	def reset(self):
		self.parent.reset()
		self.able_jump = False
		self.speed = 0
		self.position = 80, 280