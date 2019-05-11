# coding: utf-8
# 저자 : Charles
# 공개번호 : Charles의 피카츄
# 음식
import pygame
import random


# 탱크 용량을 향상시키는데 사용되는 음식
class Food(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		# 현재의 모든 적을 파괴하십시오
		self.food_boom = './images/food/food_boom.png'
		# 현재의 모든 적들은 여전히 잠시동안 있습니다.
		self.food_clock = './images/food/food_clock.png'
		# 탱크의 총알을 강철로 만든다.
		self.food_gun = './images/food/food_gun.png'
		# 베이스캠프의 벽을 강철벽으로 만든다
		self.food_iron = './images/food/food_gun.png'
		# 탱크가 잠시동안 보호막을 얻는다.
		self.food_protect = './images/food/food_protect.png'
		# 탱크 업그레이드
		self.food_star = './images/food/food_star.png'
		# 탱크생명+1
		self.food_tank = './images/food/food_tank.png'
		# 모든 음식
		self.foods = [self.food_boom, self.food_clock, self.food_gun, self.food_iron, self.food_protect, self.food_star, self.food_tank]
		self.kind = None
		self.food = None
		self.rect = None
		# 존재 여부
		self.being = False
		# 시간제한(남은 시간)
		self.time = 1000
	# 음식 생성
	def generate(self):
		self.kind = random.randint(0, 6)
		self.food = pygame.image.load(self.foods[self.kind]).convert_alpha()
		self.rect = self.food.get_rect()
		self.rect.left, self.rect.top = random.randint(100, 500), random.randint(100, 500)
		self.being = True