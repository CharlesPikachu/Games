# 游戏开始界面
# 作者: Charles
# 公众号: Charles的皮卡丘
import sys
import pygame


# 游戏开始界面
class StartInterface(pygame.sprite.Sprite):
	def __init__(self, WIDTH, HEIGHT):
		pygame.sprite.Sprite.__init__(self)
		self.imgs = ['./resource/imgs/start/start_interface.png']
		self.image = pygame.image.load(self.imgs[0]).convert()
		self.rect = self.image.get_rect()
		self.rect.center = WIDTH/2, HEIGHT/2
	# just pass
	def update(self):
		pass


# 开始游戏按钮
class PlayButton(pygame.sprite.Sprite):
	def __init__(self, position=(220, 415)):
		pygame.sprite.Sprite.__init__(self)
		self.imgs = ['./resource/imgs/start/play_black.png', './resource/imgs/start/play_red.png']
		self.img_1 = pygame.image.load(self.imgs[0]).convert()
		self.img_2 = pygame.image.load(self.imgs[1]).convert()
		self.image = self.img_1
		self.rect = self.image.get_rect()
		self.rect.center = position
	# 不断地更新检测鼠标是否在按钮上
	def update(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(mouse_pos):
			self.image = self.img_2
		else:
			self.image = self.img_1


# 结束游戏按钮
class QuitButton(pygame.sprite.Sprite):
	def __init__(self, position=(580, 415)):
		pygame.sprite.Sprite.__init__(self)
		self.imgs = ['./resource/imgs/start/quit_black.png', './resource/imgs/start/quit_red.png']
		self.img_1 = pygame.image.load(self.imgs[0]).convert()
		self.img_2 = pygame.image.load(self.imgs[1]).convert()
		self.image = self.img_1
		self.rect = self.image.get_rect()
		self.rect.center = position
	# 不断地更新检测鼠标是否在按钮上
	def update(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(mouse_pos):
			self.image = self.img_2
		else:
			self.image = self.img_1


# 游戏开始类
class START():
	def __init__(self, WIDTH, HEIGHT):
		self.SI = StartInterface(WIDTH, HEIGHT)
		self.PB = PlayButton()
		self.QB = QuitButton()
		self.components = pygame.sprite.LayeredUpdates(self.SI, self.PB, self.QB)
	# 外部调用
	def update(self, screen):
		clock = pygame.time.Clock()
		while True:
			clock.tick(60)
			self.components.update()
			self.components.draw(screen)
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
					pygame.quit()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						mouse_pos = pygame.mouse.get_pos()
						if self.PB.rect.collidepoint(mouse_pos):
							return True
						elif self.QB.rect.collidepoint(mouse_pos):
							return False