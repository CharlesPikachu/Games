# 游戏结束界面
# 作者: Charles
# 公众号: Charles的皮卡丘
import sys
import pygame


# 游戏结束界面
class EndInterface(pygame.sprite.Sprite):
	def __init__(self, WIDTH, HEIGHT):
		pygame.sprite.Sprite.__init__(self)
		self.imgs = ['./resource/imgs/end/gameover.png']
		self.image = pygame.image.load(self.imgs[0]).convert()
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH/2, HEIGHT/2)
	# just pass
	def update(self):
		pass


# 继续游戏按钮
class ContinueButton(pygame.sprite.Sprite):
	def __init__(self, position=(400, 409)):
		pygame.sprite.Sprite.__init__(self)
		self.imgs = ['./resource/imgs/end/continue_black.png', './resource/imgs/end/continue_red.png']
		self.img_1 = pygame.image.load(self.imgs[0]).convert()
		self.img_2 = pygame.image.load(self.imgs[1]).convert()
		self.image = self.img_1
		self.rect = self.image.get_rect()
		self.rect.center = position
	def update(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(mouse_pos):
			self.image = self.img_2
		else:
			self.image = self.img_1


# 游戏结束类
class END():
	def __init__(self, WIDTH, HEIGHT):
		self.EI = EndInterface(WIDTH, HEIGHT)
		self.CB = ContinueButton()
		self.components = pygame.sprite.LayeredUpdates(self.EI, self.CB)
	# 外部调用
	def update(self, screen):
		clock = pygame.time.Clock()
		background = pygame.Surface(screen.get_size())
		count = 0
		flag = True
		while True:
			count += 1
			clock.tick(60)
			self.components.clear(screen, background)
			self.components.update()
			if count % 10 == 0:
				count = 0
				flag = not flag
			if flag:
				self.components.draw(screen)
			else:
				screen.blit(self.EI.image, self.EI.rect)
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
					pygame.quit()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						mouse_pos = pygame.mouse.get_pos()
						if self.CB.rect.collidepoint(mouse_pos):
							return True