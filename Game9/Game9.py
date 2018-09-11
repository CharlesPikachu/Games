# 接苹果/金币小游戏
# 作者: Charles
# 公众号: Charles的皮卡丘
import os
import sys
import random
import pygame


# 获取历史最高分
def getScore():
	if os.path.isfile('score'):
		with open('score', 'r') as f:
			score = f.readline().strip()
			if not score:
				score = 0
	else:
		score = 0
	return score


# 保存分数(仅当超过历史最高分时)
def saveScore(score):
	with open('score', 'w') as f:
		f.write(score)


# 定义接苹果/金币的人类精灵
class FarmerSprite(pygame.sprite.Sprite):
	def __init__(self, WIDTH, HEIGHT):
		pygame.sprite.Sprite.__init__(self)
		self.imgs = ['./imgs/farmer.png']
		self.farmer = pygame.image.load(self.imgs[0]).convert_alpha()
		self.direction_dict = {
								'top': [0, (0, -1)],
								'righttop': [1, (1, -1)],
								'right': [2, (1, 0)],
								'rightbottom': [3, (1, 1)],
								'bottom': [4, (0, 1)],
								'leftbottom': [5, (-1, 1)],
								'left': [6, (-1, 0)],
								'lefttop': [7, (-1, -1)]
								}
		# 当前农民方向
		self.direction = 'left'
		# 实现农民行走的效果
		self.farmerIdx = 0
		self.farmerIdxNum = 8
		# 农民的位置
		self.x, self.y = WIDTH/2, HEIGHT/1.1
		# 速度
		self.speed = 5
		self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
		# 激活一下
		self.move()
	# 移动
	def move(self, direction='left'):
		if direction != self.direction:
			self.direction = direction
			self.farmerIdx = 0
		else:
			self.farmerIdx += 1
			self.farmerIdx = self.farmerIdx % self.farmerIdxNum
		farmerPos = self.farmerIdx * 96, self.direction_dict[self.direction][0] * 96
		self.image = self.farmer.subsurface(farmerPos, (96, 96))
		self.rect = self.image.get_rect()
		self.x = self.x + self.direction_dict[self.direction][1][0] * self.speed
		self.y = self.y + self.direction_dict[self.direction][1][1] * self.speed
		self.rect.left, self.rect.top = self.x, self.y
		# 避免农民走出游戏界面
		self.rect.right = self.WIDTH if self.rect.right > self.WIDTH else self.rect.right
		self.rect.left = 0 if self.rect.left < 0 else self.rect.left
		self.rect.top = 0 if self.rect.top < 0 else self.rect.top
		self.rect.bottom = self.HEIGHT if self.rect.bottom > self.HEIGHT else self.rect.bottom
	# 画上去
	def draw(self, screen):
		screen.blit(self.image, self.rect)


# 掉落的食物类
class foodSprite(pygame.sprite.Sprite):
	def __init__(self, WIDTH, HEIGHT):
		pygame.sprite.Sprite.__init__(self)
		self.imgs = ['./imgs/apple.png', './imgs/gold.png']
		# 食物种类
		self.kind = random.randint(0, 1)
		# 食物价值
		self.value = 10 if self.kind == 0 else 100
		# 下落速度
		self.speed = 3 if self.kind == 0 else 6
		self.image = pygame.image.load(self.imgs[self.kind]).convert_alpha()
		self.rect = self.image.get_rect()
		self.x = random.randint(0, WIDTH-self.rect.width)
		self.y = -50
		self.rect.left, self.rect.top = self.x, self.y
	# 移动
	def move(self):
		self.y += self.speed
		self.rect.top = self.y
	# 画到屏幕上
	def draw(self, screen):
		screen.blit(self.image, self.rect)


# 显示游戏结束界面
def GameOver(screen, width, height, score, highest):
	screen.fill((255, 255, 255))
	tfont = pygame.font.Font('./font/simkai.ttf', width//10)
	cfont = pygame.font.Font('./font/simkai.ttf', width//20)
	title = tfont.render('GameOver', True, (255, 0, 0))
	content = cfont.render('Score: %s, Highest: %s' % (score, highest), True, (0, 0, 255))
	trect = title.get_rect()
	trect.midtop = (width/2, height/4)
	crect = content.get_rect()
	crect.midtop = (width/2, height/2)
	screen.blit(title, trect)
	screen.blit(content, crect)
	pygame.display.update()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				return


# 主函数
def main():
	# 初始化
	pygame.init()
	WIDTH = 800
	HEIGHT = 600
	screen = pygame.display.set_mode([WIDTH, HEIGHT])
	pygame.display.set_caption('接金币/苹果-公众号: Charles的皮卡丘')
	pygame.mixer.init()
	pygame.mixer.music.load("./audios/DasBeste.mp3")
	pygame.mixer.music.set_volume(0.4)
	pygame.mixer.music.play(-1)
	get_sound = pygame.mixer.Sound("./audios/get.wav")
	get_sound.set_volume(6)
	clock = pygame.time.Clock()
	# 定义一些必要的参数并实例化农民
	farmer = FarmerSprite(WIDTH, HEIGHT)
	foodGroup = pygame.sprite.Group()
	foodInterval = 100
	foodCount = 0
	direction = 'left'
	font = pygame.font.Font('./font/simkai.ttf', 20)
	score = 0
	# 如果20个食物没接住的话就Game Over
	maxDown = 20
	while True:
		if maxDown < 0:
			highest = getScore()
			if int(highest) < score:
				saveScore(str(score))
			GameOver(screen, WIDTH, HEIGHT, score, highest)
		screen.fill([0, 160, 233])
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		key_pressed = pygame.key.get_pressed()
		if key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
			if direction in ['top', 'bottom', 'right']:
				direction = 'left'
			elif direction == 'left':
				farmer.move(direction)
		elif key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
			if direction in ['top', 'bottom', 'left']:
				direction = 'right'
			elif direction == 'right':
				farmer.move(direction)
		elif key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]:
			if direction in ['right', 'left', 'bottom']:
				direction = 'top'
			elif direction == 'top':
				farmer.move(direction)
		elif key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
			if direction in ['right', 'left', 'top']:
				direction = 'bottom'
			elif direction == 'bottom':
				farmer.move(direction)
		farmer.draw(screen)
		foodCount += 1
		if foodCount > foodInterval:
			food = foodSprite(WIDTH, HEIGHT)
			foodGroup.add(food)
			foodCount = 0
		for food in foodGroup:
			food.move()
			if pygame.sprite.collide_rect(food, farmer):
				foodGroup.remove(food)
				score += food.value
				get_sound.play()
				continue
			if food.rect.top > HEIGHT:
				foodGroup.remove(food)
				if food.kind == 0:
					maxDown -= 1
				continue
			food.draw(screen)
		life_text = font.render("Life: "+str(maxDown), 1, (0, 0, 0))
		score_text = font.render("Score: "+str(score), 1, (0, 0, 0))
		screen.blit(score_text, [10, 10])
		screen.blit(life_text, [10, 35])
		pygame.display.flip()
		clock.tick(60)




if __name__ == '__main__':
	main()