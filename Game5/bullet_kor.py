# coding: utf-8
# 저자 : Charles
# 공개번호 : Charles의 피카츄
# 총알
import pygame


# 총알
class Bullet(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		# 4방향총알(상하좌우)
		self.bullets = ['./images/bullet/bullet_up.png', './images/bullet/bullet_down.png', './images/bullet/bullet_left.png', './images/bullet/bullet_right.png']
		# 총알방향(기본 값)
		self.direction_x, self.direction_y = 0, -1
		self.bullet = pygame.image.load(self.bullets[0])
		self.rect = self.bullet.get_rect()
		# 탱크 클래스에 실제 값 지정
		self.rect.left, self.rect.right = 0, 0
		# 속도
		self.speed = 6
		# 생존 여부
		self.being = False
		# 강화된 총알(강철 벽을 뚫을 수 있는)인지 여부 확인
		self.stronger = False
	# 총알 방향 바꾸기
	def turn(self, direction_x, direction_y):
		self.direction_x, self.direction_y = direction_x, direction_y
		if self.direction_x == 0 and self.direction_y == -1:
			self.bullet = pygame.image.load(self.bullets[0])
		elif self.direction_x == 0 and self.direction_y == 1:
			self.bullet = pygame.image.load(self.bullets[1])
		elif self.direction_x == -1 and self.direction_y == 0:
			self.bullet = pygame.image.load(self.bullets[2])
		elif self.direction_x == 1 and self.direction_y == 0:
			self.bullet = pygame.image.load(self.bullets[3])
		else:
			raise ValueError('Bullet class -> direction value error.')
	# 이동하기
	def move(self):
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		# 지도의 가장자리로 이동한 후 사라짐
		if (self.rect.top < 3) or (self.rect.bottom > 630 - 3) or (self.rect.left < 3) or (self.rect.right > 630 - 3):
			self.being = False