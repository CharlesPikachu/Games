# coding: utf-8
# 저자 : Charles
# 공개번호 : Charles의 피카츄
# 베이스캠프
import pygame


# 베이스캠프
class Home(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.homes = ['./images/home/home1.png', './images/home/home2.png', './images/home/home_destroyed.png']
		self.home = pygame.image.load(self.homes[0])
		self.rect = self.home.get_rect()
		self.rect.left, self.rect.top = (3 + 12 * 24, 3 + 24 * 24)
		self.alive = True
	# 베이스캠프 파괴
	def set_dead(self):
		self.home = pygame.image.load(self.homes[-1])
		self.alive = False