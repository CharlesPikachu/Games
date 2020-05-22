'''
Function:
	定义场景元素(地板, 云等)
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import pygame


'''地板'''
class Ground(pygame.sprite.Sprite):
	def __init__(self, imagepath, position, **kwargs):
		pygame.sprite.Sprite.__init__(self)
		# 导入图片
		self.image_0 = pygame.image.load(imagepath)
		self.rect_0 = self.image_0.get_rect()
		self.rect_0.left, self.rect_0.bottom = position
		self.image_1 = pygame.image.load(imagepath)
		self.rect_1 = self.image_1.get_rect()
		self.rect_1.left, self.rect_1.bottom = self.rect_0.right, self.rect_0.bottom
		# 定义一些必要的参数
		self.speed = -10
	'''更新地板'''
	def update(self):
		self.rect_0.left += self.speed
		self.rect_1.left += self.speed
		if self.rect_0.right < 0:
			self.rect_0.left = self.rect_1.right
		if self.rect_1.right < 0:
			self.rect_1.left = self.rect_0.right
	'''将地板画到屏幕'''
	def draw(self, screen):
		screen.blit(self.image_0, self.rect_0)
		screen.blit(self.image_1, self.rect_1)


'''云'''
class Cloud(pygame.sprite.Sprite):
	def __init__(self, imagepath, position, **kwargs):
		pygame.sprite.Sprite.__init__(self)
		# 导入图片
		self.image = pygame.image.load(imagepath)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = position
		# 定义一些必要的参数
		self.speed = -1
	'''将云画到屏幕上'''
	def draw(self, screen):
		screen.blit(self.image, self.rect)
	'''更新云'''
	def update(self):
		self.rect = self.rect.move([self.speed, 0])
		if self.rect.right < 0:
			self.kill()


'''记分板'''
class Scoreboard(pygame.sprite.Sprite):
	def __init__(self, imagepath, position, size=(11, 13), is_highest=False, bg_color=None, **kwargs):
		pygame.sprite.Sprite.__init__(self)
		# 导入图片
		self.images = []
		image = pygame.image.load(imagepath)
		for i in range(12):
			self.images.append(pygame.transform.scale(image.subsurface((i*20, 0), (20, 24)), size))
		if is_highest:
			self.image = pygame.Surface((size[0]*8, size[1]))
		else:
			self.image = pygame.Surface((size[0]*5, size[1]))
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = position
		# 一些必要的变量
		self.is_highest = is_highest
		self.bg_color = bg_color
		self.score = '00000'
	'''设置得分'''
	def set(self, score):
		self.score = str(score).zfill(5)
	'''画到屏幕上'''
	def draw(self, screen):
		self.image.fill(self.bg_color)
		for idx, digital in enumerate(list(self.score)):
			digital_image = self.images[int(digital)]
			if self.is_highest:
				self.image.blit(digital_image, ((idx+3)*digital_image.get_rect().width, 0))
			else:
				self.image.blit(digital_image, (idx*digital_image.get_rect().width, 0))
		if self.is_highest:
			self.image.blit(self.images[-2], (0, 0))
			self.image.blit(self.images[-1], (digital_image.get_rect().width, 0))
		screen.blit(self.image, self.rect)