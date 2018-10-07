# 飞机大战
# 作者: Charles
# 公众号: Charles的皮卡丘
import os
import sys
import pygame
import random


WIDTH = 956
HEIGHT = 560


# 定义按钮
def BUTTON(screen, position, text):
	bwidth = 310
	bheight = 65
	left, top = position
	pygame.draw.line(screen, (150, 150, 150), (left, top), (left+bwidth, top), 5)
	pygame.draw.line(screen, (150, 150, 150), (left, top-2), (left, top+bheight), 5)
	pygame.draw.line(screen, (50, 50, 50), (left, top+bheight), (left+bwidth, top+bheight), 5)
	pygame.draw.line(screen, (50, 50, 50), (left+bwidth, top+bheight), [left+bwidth, top], 5)
	pygame.draw.rect(screen, (100, 100, 100), (left, top, bwidth, bheight))
	font = pygame.font.Font('./resources/font/simkai.ttf', 50)
	text_render = font.render(text, 1, (255, 0, 0))
	return screen.blit(text_render, (left+50, top+10))


# 开始界面
def start_interface(screen):
	clock = pygame.time.Clock()
	while True:
		button_1 = BUTTON(screen, (330, 190), '单人模式')
		button_2 = BUTTON(screen, (330, 305), '双人模式')
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if button_1.collidepoint(pygame.mouse.get_pos()):
					return 1
				elif button_2.collidepoint(pygame.mouse.get_pos()):
					return 2
		clock.tick(60)
		pygame.display.update()


# 子弹
class Bullet(pygame.sprite.Sprite):
	def __init__(self, idx, position):
		pygame.sprite.Sprite.__init__(self)
		self.imgs = ['./resources/imgs/bullet.png']
		self.image = pygame.image.load(self.imgs[0]).convert_alpha()
		self.image = pygame.transform.scale(self.image, (10, 10))
		# 位置
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = position
		self.position = position
		# 速度
		self.speed = 8
		# 玩家编号
		self.playerIdx = idx
	# 移动子弹
	def move(self):
		self.position = self.position[0], self.position[1] - self.speed
		self.rect.left, self.rect.top = self.position
	# 画子弹
	def draw(self, screen):
		screen.blit(self.image, self.rect)


# 小行星
class Asteroid(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.imgs = ['./resources/imgs/asteroid.png']
		self.image = pygame.image.load(self.imgs[0]).convert_alpha()
		# 位置
		self.rect = self.image.get_rect()
		self.position = (random.randrange(20, WIDTH-20), -64)
		self.rect.left, self.rect.top = self.position
		# 速度
		self.speed = random.randrange(3, 9)
		self.angle = 0
		self.angular_velocity = random.randrange(1, 5)
		self.rotate_ticks = 3
	# 移动小行星
	def move(self):
		self.position = self.position[0], self.position[1] + self.speed
		self.rect.left, self.rect.top = self.position
	# 转动小行星
	def rotate(self):
		self.rotate_ticks -= 1
		if self.rotate_ticks == 0:
			self.angle = (self.angle + self.angular_velocity) % 360
			orig_rect = self.image.get_rect()
			rot_image = pygame.transform.rotate(self.image, self.angle)
			rot_rect = orig_rect.copy()
			rot_rect.center = rot_image.get_rect().center
			rot_image = rot_image.subsurface(rot_rect).copy()
			self.image = rot_image
			self.rotate_ticks = 3
	# 画小行星
	def draw(self, screen):
		screen.blit(self.image, self.rect)


# 飞船
class Ship(pygame.sprite.Sprite):
	def __init__(self, idx):
		pygame.sprite.Sprite.__init__(self)
		self.imgs = ['./resources/imgs/ship.png', './resources/imgs/ship_exploded.png']
		self.image = pygame.image.load(self.imgs[0]).convert_alpha()
		self.explode_img = pygame.image.load(self.imgs[1]).convert_alpha()
		# 位置
		self.position = {'x': random.randrange(-10, 918), 'y': random.randrange(-10, 520)}
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = self.position['x'], self.position['y']
		# 速度
		self.speed = {'x': 10, 'y': 5}
		# 玩家编号
		self.playerIdx = idx
		# 子弹冷却时间
		self.cooling_time = 0
		# 爆炸用
		self.explode_step = 0
	# 飞船爆炸
	def explode(self, screen):
		img = self.explode_img.subsurface((48*(self.explode_step-1), 0), (48, 48))
		screen.blit(img, (self.position['x'], self.position['y']))
		self.explode_step += 1
	# 移动飞船
	def move(self, direction):
		if direction == 'left':
			self.position['x'] = max(-self.speed['x']+self.position['x'], -10)
		elif direction == 'right':
			self.position['x'] = min(self.speed['x']+self.position['x'], 918)
		elif direction == 'up':
			self.position['y'] = max(-self.speed['y']+self.position['y'], -10)
		elif direction == 'down':
			self.position['y'] = min(self.speed['y']+self.position['y'], 520)
		self.rect.left, self.rect.top = self.position['x'], self.position['y']
	# 画飞船
	def draw(self, screen):
		screen.blit(self.image, self.rect)
	# 射击
	def shot(self):
		return Bullet(self.playerIdx, (self.rect.center[0] - 5, self.position['y'] - 5))


# 游戏界面
def GameDemo(num_player, screen):
	pygame.mixer.music.load(("./resources/sounds/Cool Space Music.mp3"))
	pygame.mixer.music.set_volume(0.4)
	pygame.mixer.music.play(-1)
	explosion_sound = pygame.mixer.Sound('./resources/sounds/boom.wav')
	fire_sound = pygame.mixer.Sound('./resources/sounds/shot.ogg')
	font = pygame.font.Font('./resources/font/simkai.ttf', 20)
	# 游戏背景图
	bg_imgs = ['./resources/imgs/bg_big.png',
			   './resources/imgs/seamless_space.png',
			   './resources/imgs/space3.jpg']
	bg_move_dis = 0
	bg_1 = pygame.image.load(bg_imgs[0]).convert()
	bg_2 = pygame.image.load(bg_imgs[1]).convert()
	bg_3 = pygame.image.load(bg_imgs[2]).convert()
	# 玩家, 子弹和小行星精灵组
	playerGroup = pygame.sprite.Group()
	bulletGroup = pygame.sprite.Group()
	asteroidGroup = pygame.sprite.Group()
	# 产生小行星的时间间隔
	asteroid_ticks = 90
	for i in range(num_player):
		playerGroup.add(Ship(i+1))
	clock = pygame.time.Clock()
	# 分数
	Score_1 = 0
	Score_2 = 0
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		# 玩家一: ↑↓←→控制, j射击
		# 玩家二: wsad控制, 空格射击
		pressed_keys = pygame.key.get_pressed()
		i = -1
		for player in playerGroup:
			i += 1
			direction = None
			if i == 0:
				if pressed_keys[pygame.K_UP]:
					direction = 'up'
				elif pressed_keys[pygame.K_DOWN]:
					direction = 'down'
				elif pressed_keys[pygame.K_LEFT]:
					direction = 'left'
				elif pressed_keys[pygame.K_RIGHT]:
					direction = 'right'
				if direction:
					player.move(direction)
				if pressed_keys[pygame.K_j]:
					if player.cooling_time == 0:
						fire_sound.play()
						bulletGroup.add(player.shot())
						player.cooling_time = 20
			elif i == 1:
				if pressed_keys[pygame.K_w]:
					direction = 'up'
				elif pressed_keys[pygame.K_s]:
					direction = 'down'
				elif pressed_keys[pygame.K_a]:
					direction = 'left'
				elif pressed_keys[pygame.K_d]:
					direction = 'right'
				if direction:
					player.move(direction)
				if pressed_keys[pygame.K_SPACE]:
					if player.cooling_time == 0:
						fire_sound.play()
						bulletGroup.add(player.shot())
						player.cooling_time = 20
			if player.cooling_time > 0:
				player.cooling_time -= 1
		if (Score_1 + Score_2) < 500:
			background = bg_1
		elif (Score_1 + Score_2) < 1500:
			background = bg_2
		else:
			background = bg_3
		# 向下移动背景图实现飞船向上移动的效果
		screen.blit(background, (0, -background.get_rect().height + bg_move_dis))
		screen.blit(background, (0, bg_move_dis))
		bg_move_dis = (bg_move_dis + 2) % background.get_rect().height
		# 生成小行星
		if asteroid_ticks == 0:
			asteroid_ticks = 90
			asteroidGroup.add(Asteroid())
		else:
			asteroid_ticks -= 1
		# 画飞船
		for player in playerGroup:
			if pygame.sprite.spritecollide(player, asteroidGroup, True, None):
				player.explode_step = 1
				explosion_sound.play()
			elif player.explode_step > 0:
				if player.explode_step > 3:
					playerGroup.remove(player)
					if len(playerGroup) == 0:
						return
				else:
					player.explode(screen)
			else:
				player.draw(screen)
		# 画子弹
		for bullet in bulletGroup:
			bullet.move()
			if pygame.sprite.spritecollide(bullet, asteroidGroup, True, None):
				bulletGroup.remove(bullet)
				if bullet.playerIdx == 1:
					Score_1 += 1
				else:
					Score_2 += 1
			else:
				bullet.draw(screen)
		# 画小行星
		for asteroid in asteroidGroup:
			asteroid.move()
			asteroid.rotate()
			asteroid.draw(screen)
		# 显示分数
		Score_1_text = '玩家一得分: %s' % Score_1
		Score_2_text = '玩家二得分: %s' % Score_2
		text_1 = font.render(Score_1_text, True, (0, 0, 255))
		text_2 = font.render(Score_2_text, True, (255, 0, 0))
		screen.blit(text_1, (2, 5))
		screen.blit(text_2, (2, 35))
		pygame.display.update()
		clock.tick(60)


# 结束界面
def end_interface(screen):
	clock = pygame.time.Clock()
	while True:
		button_1 = BUTTON(screen, (330, 190), '重新开始')
		button_2 = BUTTON(screen, (330, 305), '退出游戏')
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if button_1.collidepoint(pygame.mouse.get_pos()):
					return
				elif button_2.collidepoint(pygame.mouse.get_pos()):
					pygame.quit()
					sys.exit()
		clock.tick(60)
		pygame.display.update()


# 主函数
def main():
	pygame.init()
	pygame.font.init()
	pygame.mixer.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('飞机大战-公众号: Charles的皮卡丘')
	num_player = start_interface(screen)
	if num_player == 1:
		while True:
			GameDemo(num_player=1, screen=screen)
			end_interface(screen)
	else:
		while True:
			GameDemo(num_player=2, screen=screen)
			end_interface(screen)


if __name__ == '__main__':
	main()