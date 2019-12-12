'''
Function:
	大本营类
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import pygame


'''大本营类'''
class Home(pygame.sprite.Sprite):
	def __init__(self, position, imagepaths, **kwargs):
		pygame.sprite.Sprite.__init__(self)
		self.imagepaths = imagepaths
		self.image = pygame.image.load(self.imagepaths[0])
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = position
		self.alive = True
	'''被摧毁'''
	def setDead(self):
		self.image = pygame.image.load(self.imagepaths[1])
		self.alive = False
	'''画到屏幕上'''
	def draw(self, screen):
		screen.blit(self.image, self.rect)