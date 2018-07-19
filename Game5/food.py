# coding: utf-8
# 作者: Charles
# 公众号: Charles的皮卡丘
# 食物类
import pygame
import random


# 食物类, 用于提升坦克能力
class Food(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		# 消灭当前所有敌人
		self.food_boom = './images/food/food_boom.png'
		# 当前所有敌人静止一段时间
		self.food_clock = './images/food/food_clock.png'
		# 使得坦克子弹可碎钢板
		self.food_gun = './images/food/food_gun.png'
		# 使得大本营的墙变为钢板
		self.food_iron = './images/food/food_gun.png'
		# 坦克获得一段时间的保护罩
		self.food_protect = './images/food/food_protect.png'
		# 坦克升级
		self.food_star = './images/food/food_star.png'
		# 坦克生命+1
		self.food_tank = './images/food/food_tank.png'
		# 所有食物
		self.foods = [self.food_boom, self.food_clock, self.food_gun, self.food_iron, self.food_protect, self.food_star, self.food_tank]
		self.kind = None
		self.food = None
		self.rect = None
		# 是否存在
		self.being = False
		# 存在时间
		self.time = 1000
	# 生成食物
	def generate(self):
		self.kind = random.randint(0, 6)
		self.food = pygame.image.load(self.foods[self.kind]).convert_alpha()
		self.rect = self.food.get_rect()
		self.rect.left, self.rect.top = random.randint(100, 500), random.randint(100, 500)
		self.being = True