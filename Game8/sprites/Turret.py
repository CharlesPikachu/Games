# 炮塔类
# 作者:Charles
# 公众号: Charles的皮卡丘
import pygame
from sprites import Arrow


# 炮塔类
class Turret(pygame.sprite.Sprite):
	def __init__(self, turret_type):
		assert turret_type in range(3)
		pygame.sprite.Sprite.__init__(self)
		self.turret_type = turret_type
		self.imgs = ['./resource/imgs/game/basic_tower.png', './resource/imgs/game/med_tower.png', './resource/imgs/game/heavy_tower.png']
		self.image = pygame.image.load(self.imgs[turret_type])
		self.rect = self.image.get_rect()
		# 箭
		self.arrow = Arrow.Arrow(turret_type)
		# 当前的位置
		self.coord = 0, 0
		self.position = 0, 0
		self.rect.left, self.rect.top = self.position
		self.reset()
	# 射击
	def shot(self, position, angle=None):
		arrow = None
		if not self.is_cooling:
			arrow = Arrow.Arrow(self.turret_type)
			arrow.reset(position, angle)
			self.is_cooling = True
		if self.is_cooling:
			self.coolTime -= 1
			if self.coolTime == 0:
				self.reset()
		return arrow
	# 重置
	def reset(self):
		if self.turret_type == 0:
			# 价格
			self.price = 500
			# 射箭的冷却时间
			self.coolTime = 30
			# 是否在冷却期
			self.is_cooling = False
		elif self.turret_type == 1:
			self.price = 1000
			self.coolTime = 50
			self.is_cooling = False
		elif self.turret_type == 2:
			self.price = 1500
			self.coolTime = 100
			self.is_cooling = False