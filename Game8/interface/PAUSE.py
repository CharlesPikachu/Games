# 游戏暂停界面
# 作者: Charles
# 公众号: Charles的皮卡丘
import sys
import pygame


# 游戏暂停界面
class PauseInterface(pygame.sprite.Sprite):
	def __init__(self, WIDTH, HEIGHT):
		pygame.sprite.Sprite.__init__(self)
		self.imgs = ['./resource/imgs/pause/gamepaused.png']
		self.image = pygame.image.load(self.imgs[0]).convert()
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH/2, HEIGHT/2)
	# just pass
	def update(self):
		pass


# 恢复游戏按钮
class ResumeButton(pygame.sprite.Sprite):
	def __init__(self, position=(391, 380)):
		pygame.sprite.Sprite.__init__(self)
		self.imgs = ['./resource/imgs/pause/resume_black.png', './resource/imgs/pause/resume_red.png']
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


# 游戏暂停类
class PAUSE():
	def __init__(self, WIDTH, HEIGHT):
		self.PI = PauseInterface(WIDTH, HEIGHT)
		self.RB = ResumeButton()
		self.components = pygame.sprite.LayeredUpdates(self.PI, self.RB)
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
				screen.blit(self.PI.image, self.PI.rect)
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
					pygame.quit()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						mouse_pos = pygame.mouse.get_pos()
						if self.RB.rect.collidepoint(mouse_pos):
							return True