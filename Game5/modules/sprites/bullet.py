'''
Function:
	子弹类
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import pygame


'''子弹'''
class Bullet(pygame.sprite.Sprite):
	def __init__(self, bullet_image_paths, screensize, direction, position, border_len, is_stronger=False, speed=8, **kwargs):
		pygame.sprite.Sprite.__init__(self)
		self.bullet_image_paths = bullet_image_paths
		self.width, self.height = screensize
		self.direction = direction
		self.position = position
		self.image = pygame.image.load(self.bullet_image_paths.get(direction))
		self.rect = self.image.get_rect()
		self.rect.center = position
		# 地图边缘宽度
		self.border_len = border_len
		# 是否为加强版子弹(加强版可碎铁墙)
		self.is_stronger = is_stronger
		# 子弹速度
		self.speed = speed
	'''移动子弹, 若子弹越界, 则返回True, 否则为False'''
	def move(self):
		if self.direction == 'up':
			self.rect = self.rect.move(0, -self.speed)
		elif self.direction == 'down':
			self.rect = self.rect.move(0, self.speed)
		elif self.direction == 'left':
			self.rect = self.rect.move(-self.speed, 0)
		elif self.direction == 'right':
			self.rect = self.rect.move(self.speed, 0)
		if (self.rect.top < self.border_len) or (self.rect.bottom > self.height) or (self.rect.left < self.border_len) or (self.rect.right > self.width):
			return True
		return False