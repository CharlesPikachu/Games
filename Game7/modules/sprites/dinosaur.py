'''
Function:
	小恐龙类
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import pygame


'''小恐龙'''
class Dinosaur(pygame.sprite.Sprite):
	def __init__(self, imagepaths, position=(40, 147), size=[(44, 47), (59, 47)], **kwargs):
		pygame.sprite.Sprite.__init__(self)
		# 导入所有图片
		self.images = []
		image = pygame.image.load(imagepaths[0])
		for i in range(5):
			self.images.append(pygame.transform.scale(image.subsurface((i*88, 0), (88, 95)), size[0]))
		image = pygame.image.load(imagepaths[1])
		for i in range(2):
			self.images.append(pygame.transform.scale(image.subsurface((i*118, 0), (118, 95)), size[1]))
		self.image_idx = 0
		self.image = self.images[self.image_idx]
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.bottom = position
		self.mask = pygame.mask.from_surface(self.image)
		# 定义一些必要的变量
		self.init_position = position
		self.refresh_rate = 5
		self.refresh_counter = 0
		self.speed = 11.5
		self.gravity = 0.6
		self.is_jumping = False
		self.is_ducking = False
		self.is_dead = False
		self.movement = [0, 0]
	'''跳跃'''
	def jump(self, sounds):
		if self.is_dead or self.is_jumping:
			return
		sounds['jump'].play()
		self.is_jumping = True
		self.movement[1] = -1 * self.speed
	'''低头'''
	def duck(self):
		if self.is_jumping or self.is_dead:
			return
		self.is_ducking = True
	'''不低头'''
	def unduck(self):
		self.is_ducking = False
	'''死掉了'''
	def die(self, sounds):
		if self.is_dead:
			return
		sounds['die'].play()
		self.is_dead = True
	'''将恐龙画到屏幕'''
	def draw(self, screen):
		screen.blit(self.image, self.rect)
	'''载入当前状态的图片'''
	def loadImage(self):
		self.image = self.images[self.image_idx]
		rect = self.image.get_rect()
		rect.left, rect.top = self.rect.left, self.rect.top
		self.rect = rect
		self.mask = pygame.mask.from_surface(self.image)
	'''更新小恐龙'''
	def update(self):
		if self.is_dead:
			self.image_idx = 4
			self.loadImage()
			return
		if self.is_jumping:
			self.movement[1] += self.gravity
			self.image_idx = 0
			self.loadImage()
			self.rect = self.rect.move(self.movement)
			if self.rect.bottom >= self.init_position[1]:
				self.rect.bottom = self.init_position[1]
				self.is_jumping = False
		elif self.is_ducking:
			if self.refresh_counter % self.refresh_rate == 0:
				self.refresh_counter = 0
				self.image_idx = 5 if self.image_idx == 6 else 6
				self.loadImage()
		else:
			if self.refresh_counter % self.refresh_rate == 0:
				self.refresh_counter = 0
				if self.image_idx == 1:
					self.image_idx = 2
				elif self.image_idx == 2:
					self.image_idx = 3
				else:
					self.image_idx = 1
				self.loadImage()
		self.refresh_counter += 1