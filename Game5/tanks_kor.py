# coding: utf-8
# 저자 : Charles//
# 공개번호 : Charles의 피카츄
# 탱크 클래스
import pygame
import random
from bullet import Bullet


# 아군 탱크 클래스
class myTank(pygame.sprite.Sprite):
	def __init__(self, player):
		pygame.sprite.Sprite.__init__(self)
		# 플레이어 수(1/2)
		self.player = player
		# 다른 플레이어는 다른 탱크를 사용(다른 레벨은 다른 맵에 해당한다)
		if player == 1:
			self.tanks = ['./images/myTank/tank_T1_0.png', './images/myTank/tank_T1_1.png', './images/myTank/tank_T1_2.png']
		elif player == 2:
			self.tanks = ['./images/myTank/tank_T2_0.png', './images/myTank/tank_T2_1.png', './images/myTank/tank_T2_2.png']
		else:
			raise ValueError('myTank class -> player value error.')
		# 탱크 등급(초기0)
		self.level = 0
		# 로드(불러오기)(두개의 Tank는 휠을 위한 특수효과)
		self.tank = pygame.image.load(self.tanks[self.level]).convert_alpha()
		self.tank_0 = self.tank.subsurface((0, 0), (48, 48))
		self.tank_1 = self.tank.subsurface((48, 0), (48, 48))
		self.rect = self.tank_0.get_rect()
		# 보호막
		self.protected_mask = pygame.image.load('./images/others/protect.png').convert_alpha()
		self.protected_mask1 = self.protected_mask.subsurface((0, 0), (48, 48))
		self.protected_mask2 = self.protected_mask.subsurface((48, 0), (48, 48))
		# 탱크 방향
		self.direction_x, self.direction_y = 0, -1
		# 플레이어에 따라 출생 위치가 다름
		if player == 1:
			self.rect.left, self.rect.top = 3 + 24 * 8, 3 + 24 * 24
		elif player == 2:
			self.rect.left, self.rect.top = 3 + 24 * 16, 3 + 24 * 24
		else:
			raise ValueError('myTank class -> player value error.')
		# 탱크 속도
		self.speed = 3
		# 생존 여부
		self.being = True
		# 목숨 수
		self.life = 3
		# 보호상태 여부
		self.protected = False
		# 총알
		self.bullet = Bullet()
	# 슈팅(공격)
	def shoot(self):
		self.bullet.being = True
		self.bullet.turn(self.direction_x, self.direction_y)
		if self.direction_x == 0 and self.direction_y == -1:
			self.bullet.rect.left = self.rect.left + 20
			self.bullet.rect.bottom = self.rect.top - 1
		elif self.direction_x == 0 and self.direction_y == 1:
			self.bullet.rect.left = self.rect.left + 20
			self.bullet.rect.top = self.rect.bottom + 1
		elif self.direction_x == -1 and self.direction_y == 0:
			self.bullet.rect.right = self.rect.left - 1
			self.bullet.rect.top = self.rect.top + 20
		elif self.direction_x == 1 and self.direction_y == 0:
			self.bullet.rect.left = self.rect.right + 1
			self.bullet.rect.top = self.rect.top + 20
		else:
			raise ValueError('myTank class -> direction value error.')
		if self.level == 0:
			self.bullet.speed = 8
			self.bullet.stronger = False
		elif self.level == 1:
			self.bullet.speed = 12
			self.bullet.stronger = False
		elif self.level == 2:
			self.bullet.speed = 12
			self.bullet.stronger = True
		elif self.level == 3:
			self.bullet.speed = 16
			self.bullet.stronger = True
		else:
			raise ValueError('myTank class -> level value error.')
	# 레벨 업
	def up_level(self):
		if self.level < 3:
			self.level += 1
		try:
			self.tank = pygame.image.load(self.tanks[self.level]).convert_alpha()
		except:
			self.tank = pygame.image.load(self.tanks[-1]).convert_alpha()
	# 레벨 다운
	def down_level(self):
		if self.level > 0:
			self.level -= 1
		self.tank = pygame.image.load(self.tanks[self.level]).convert_alpha()
	# 위로
	def move_up(self, tankGroup, brickGroup, ironGroup, myhome):
		self.direction_x, self.direction_y = 0, -1
		# 먼저 이동 후 판단
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		self.tank_0 = self.tank.subsurface((0, 0), (48, 48))
		self.tank_1 = self.tank.subsurface((48, 0), (48, 48))
		# 움직일수 있는지 여부
		is_move = True
		# 지도 맨 위로
		if self.rect.top < 3:
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 돌 벽/강철 벽 에 부딫히기
		if pygame.sprite.spritecollide(self, brickGroup, False, None) or \
			pygame.sprite.spritecollide(self, ironGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 다른 탱크와 충돌
		if pygame.sprite.spritecollide(self, tankGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 베이스캠프
		if pygame.sprite.collide_rect(self, myhome):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		return is_move
	# 아래로
	def move_down(self, tankGroup, brickGroup, ironGroup, myhome):
		self.direction_x, self.direction_y = 0, 1
		# 先移动后判断//먼저 이동한 후 판단
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		self.tank_0 = self.tank.subsurface((0, 48), (48, 48))
		self.tank_1 = self.tank.subsurface((48, 48), (48, 48))
		# 이동가능 여부
		is_move = True
		# 지도의 맨 아래
		if self.rect.bottom > 630 - 3:
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 돌 벽/ 강철 벽에 부딪히기 
		if pygame.sprite.spritecollide(self, brickGroup, False, None) or \
			pygame.sprite.spritecollide(self, ironGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 다른 탱크와의 충돌
		if pygame.sprite.spritecollide(self, tankGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 베이스캠프
		if pygame.sprite.collide_rect(self, myhome):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		return is_move
	# 왼쪽으로
	def move_left(self, tankGroup, brickGroup, ironGroup, myhome):
		self.direction_x, self.direction_y = -1, 0
		# 먼저 이동한 후 판단
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		self.tank_0 = self.tank.subsurface((0, 96), (48, 48))
		self.tank_1 = self.tank.subsurface((48, 96), (48, 48))
		# 이동 가능 여부
		is_move = True
		# 지도 왼쪽 끝
		if self.rect.left < 3:
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 돌 벽/강철 벽에 부딪히다
		if pygame.sprite.spritecollide(self, brickGroup, False, None) or \
			pygame.sprite.spritecollide(self, ironGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 다른 탱크와의 충돌
		if pygame.sprite.spritecollide(self, tankGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False		
		# 베이스캠프
		if pygame.sprite.collide_rect(self, myhome):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		return is_move
	# 오른쪽으로
	def move_right(self, tankGroup, brickGroup, ironGroup, myhome):
		self.direction_x, self.direction_y = 1, 0
		# 먼저 이동한 후 판단
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		self.tank_0 = self.tank.subsurface((0, 144), (48, 48))
		self.tank_1 = self.tank.subsurface((48, 144), (48, 48))
		# 이동 가능 여부
		is_move = True
		# 지도 오른쪽끝
		if self.rect.right > 630 - 3:
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 돌 벽/ 강철 벽에 부딪히다
		if pygame.sprite.spritecollide(self, brickGroup, False, None) or \
			pygame.sprite.spritecollide(self, ironGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 다른 탱크와의 충돌
		if pygame.sprite.spritecollide(self, tankGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		# 베이스캠프
		if pygame.sprite.collide_rect(self, myhome):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			is_move = False
		return is_move
	# 사망후 재설정
	def reset(self):
		self.level = 0
		self.protected = False
		self.tank = pygame.image.load(self.tanks[self.level]).convert_alpha()
		self.tank_0 = self.tank.subsurface((0, 0), (48, 48))
		self.tank_1 = self.tank.subsurface((48, 0), (48, 48))
		self.rect = self.tank_0.get_rect()
		self.direction_x, self.direction_y = 0, -1
		if self.player == 1:
			self.rect.left, self.rect.top = 3 + 24 * 8, 3 + 24 * 24
		elif self.player == 2:
			self.rect.left, self.rect.top = 3 + 24 * 16, 3 + 24 * 24
		else:
			raise ValueError('myTank class -> player value error.')
		self.speed = 3


# 적 탱크
class enemyTank(pygame.sprite.Sprite):
	def __init__(self, x=None, kind=None, is_red=None):
		pygame.sprite.Sprite.__init__(self)
		# 새로 생성된 탱크의 탄생 효과를 재생하는데 사용된다.
		self.born = True
		self.times = 90
		# 탱크의 종류
		if kind is None:
			self.kind = random.randint(0, 3)
		else:
			self.kind = kind
		# 모든 탱크
		self.tanks1 = ['./images/enemyTank/enemy_1_0.png', './images/enemyTank/enemy_1_1.png', './images/enemyTank/enemy_1_2.png', './images/enemyTank/enemy_1_3.png']
		self.tanks2 = ['./images/enemyTank/enemy_2_0.png', './images/enemyTank/enemy_2_1.png', './images/enemyTank/enemy_2_2.png', './images/enemyTank/enemy_2_3.png']
		self.tanks3 = ['./images/enemyTank/enemy_3_0.png', './images/enemyTank/enemy_3_1.png', './images/enemyTank/enemy_3_2.png', './images/enemyTank/enemy_3_3.png']
		self.tanks4 = ['./images/enemyTank/enemy_4_0.png', './images/enemyTank/enemy_4_1.png', './images/enemyTank/enemy_4_2.png', './images/enemyTank/enemy_4_3.png']
		self.tanks = [self.tanks1, self.tanks2, self.tanks3, self.tanks4]
		# 음식을 가져올지 여부확인(빨간 탱크는 음식을 나른다)
		if is_red is None:
			self.is_red = random.choice((True, False, False, False, False))
		else:
			self.is_red = is_red
		# 같은 종류의 탱크는 색깔이 다르며 붉은 색 탱크는 같은 종류의 탱크보다 혈액(체력,피)이 조금 더 많습니다.
		if self.is_red:
			self.color = 3
		else:
			self.color = random.randint(0, 2)
		# 혈액량
		self.blood = self.color
		# 로드(불러오기)(휠 효과를 위한 두개의 탱크)
		self.tank = pygame.image.load(self.tanks[self.kind][self.color]).convert_alpha()
		self.tank_0 = self.tank.subsurface((0, 48), (48, 48))
		self.tank_1 = self.tank.subsurface((48, 48), (48, 48))
		self.rect = self.tank_0.get_rect()
		# 탱크 위치
		if x is None:
			self.x = random.randint(0, 2)
		else:
			self.x = x
		self.rect.left, self.rect.top = 3 + self.x * 12 * 24, 3
		# 탱크가 움직일 수 있는지 여부
		self.can_move = True
		# 탱크 속도
		self.speed = max(3 - self.kind, 1)
		# 방향
		self.direction_x, self.direction_y = 0, 1
		# 생존 여부
		self.being = True
		# 총알
		self.bullet = Bullet()
	# 슈팅(공격)
	def shoot(self):
		self.bullet.being = True
		self.bullet.turn(self.direction_x, self.direction_y)
		if self.direction_x == 0 and self.direction_y == -1:
			self.bullet.rect.left = self.rect.left + 20
			self.bullet.rect.bottom = self.rect.top - 1
		elif self.direction_x == 0 and self.direction_y == 1:
			self.bullet.rect.left = self.rect.left + 20
			self.bullet.rect.top = self.rect.bottom + 1
		elif self.direction_x == -1 and self.direction_y == 0:
			self.bullet.rect.right = self.rect.left - 1
			self.bullet.rect.top = self.rect.top + 20
		elif self.direction_x == 1 and self.direction_y == 0:
			self.bullet.rect.left = self.rect.right + 1
			self.bullet.rect.top = self.rect.top + 20
		else:
			raise ValueError('enemyTank class -> direction value error.')
	# 무작위 운동
	def move(self, tankGroup, brickGroup, ironGroup, myhome):
		self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
		is_move = True
		if self.direction_x == 0 and self.direction_y == -1:
			self.tank_0 = self.tank.subsurface((0, 0), (48, 48))
			self.tank_1 = self.tank.subsurface((48, 0), (48, 48))
			if self.rect.top < 3:
				self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
				self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
				is_move = False
		elif self.direction_x == 0 and self.direction_y == 1:
			self.tank_0 = self.tank.subsurface((0, 48), (48, 48))
			self.tank_1 = self.tank.subsurface((48, 48), (48, 48))
			if self.rect.bottom > 630 - 3:
				self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
				self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
				is_move = False
		elif self.direction_x == -1 and self.direction_y == 0:
			self.tank_0 = self.tank.subsurface((0, 96), (48, 48))
			self.tank_1 = self.tank.subsurface((48, 96), (48, 48))
			if self.rect.left < 3:
				self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
				self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
				is_move = False
		elif self.direction_x == 1 and self.direction_y == 0:
			self.tank_0 = self.tank.subsurface((0, 144), (48, 48))
			self.tank_1 = self.tank.subsurface((48, 144), (48, 48))
			if self.rect.right > 630 - 3:
				self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
				self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
				is_move = False
		else:
			raise ValueError('enemyTank class -> direction value error.')
		if pygame.sprite.spritecollide(self, brickGroup, False, None) \
			or pygame.sprite.spritecollide(self, ironGroup, False, None) \
			or pygame.sprite.spritecollide(self, tankGroup, False, None):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
			is_move = False
		if pygame.sprite.collide_rect(self, myhome):
			self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
			self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
			is_move = False
		return is_move
	# 탱크를 재장전 하기
	def reload(self):
		self.tank = pygame.image.load(self.tanks[self.kind][self.color]).convert_alpha()
		self.tank_0 = self.tank.subsurface((0, 48), (48, 48))
		self.tank_1 = self.tank.subsurface((48, 48), (48, 48))