# 游戏模式选择界面
# 作者: Charles
# 公众号: Charles的皮卡丘
import sys
import pygame


# 游戏地图选择界面
class MapChoiceInterface(pygame.sprite.Sprite):
	def __init__(self, WIDTH, HEIGHT):
		pygame.sprite.Sprite.__init__(self)
		self.imgs = ['./resource/imgs/choice/load_game.png']
		self.image = pygame.image.load(self.imgs[0]).convert()
		self.rect = self.image.get_rect()
		self.rect.topleft = (0, 0)
	# just pass
	def update(self):
		pass


# 地图1
class MapButton1(pygame.sprite.Sprite):
	def __init__(self, position=(175, 240)):
		pygame.sprite.Sprite.__init__(self)
		self.imgs = ['./resource/imgs/choice/map1_black.png', './resource/imgs/choice/map1_red.png', './resource/imgs/choice/map1.png']
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


# 地图2
class MapButton2(pygame.sprite.Sprite):
	def __init__(self, position=(400, 240)):
		pygame.sprite.Sprite.__init__(self)
		self.imgs = ['./resource/imgs/choice/map2_black.png', './resource/imgs/choice/map2_red.png', './resource/imgs/choice/map2.png']
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


# 地图3
class MapButton3(pygame.sprite.Sprite):
	def __init__(self, position=(625, 240)):
		pygame.sprite.Sprite.__init__(self)
		self.imgs = ['./resource/imgs/choice/map3_black.png', './resource/imgs/choice/map3_red.png', './resource/imgs/choice/map3.png']
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


# 信息显示框
class InfoBox(pygame.sprite.Sprite):
	def __init__(self, position=(400, 475)):
		pygame.sprite.Sprite.__init__(self)
		self.ori_image = pygame.Surface((625, 200))
		self.ori_image.fill((255, 255, 255))
		self.ori_image_front = pygame.Surface((621, 196))
		self.ori_image_front.fill((0, 0, 0))
		self.ori_image.blit(self.ori_image_front, (2, 2))
		self.rect = self.ori_image.get_rect()
		self.rect.center = position
	def update(self, MBs):
		self.image = self.ori_image
		mouse_pos = pygame.mouse.get_pos()
		for mb in MBs:
			if mb.rect.collidepoint(mouse_pos):
				map_img = pygame.image.load(mb.imgs[2]).convert()
				self.image.blit(map_img, (225, 25))
				break


# 简单按钮
class EasyButton(pygame.sprite.Sprite):
	def __init__(self, position=(400, 150)):
		pygame.sprite.Sprite.__init__(self)
		self.img_1 = pygame.Surface((285, 100))
		self.img_1_front = pygame.Surface((281, 96))
		self.img_1.fill((255, 255, 255))
		self.img_1_front.fill((0, 0, 0))
		self.img_1.blit(self.img_1_front, (2, 2))
		self.img_2 = pygame.Surface((285, 100))
		self.img_2_front = pygame.Surface((281, 96))
		self.img_2.fill((255, 255, 255))
		self.img_2_front.fill((24, 196, 40))
		self.img_2.blit(self.img_2_front, (2, 2))
		self.text = 'easy'
		self.font = pygame.font.Font('./resource/fonts/m04.ttf', 42)
		self.textRender = self.font.render(self.text, 1, (255, 255, 255))
		self.img_1.blit(self.textRender, (46, 29))
		self.img_2.blit(self.textRender, (46, 29))
		self.image = self.img_1
		self.rect = self.image.get_rect()
		self.rect.center = position
	def update(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(mouse_pos):
			self.image = self.img_2
		else:
			self.image = self.img_1


# 中等难度按钮
class MediumButton(pygame.sprite.Sprite):
	def __init__(self, position=(400, 300)):
		pygame.sprite.Sprite.__init__(self)
		self.img_1 = pygame.Surface((285, 100))
		self.img_1_front = pygame.Surface((281, 96))
		self.img_1.fill((255, 255, 255))
		self.img_1_front.fill((0, 0, 0))
		self.img_1.blit(self.img_1_front, (2, 2))
		self.img_2 = pygame.Surface((285, 100))
		self.img_2_front = pygame.Surface((281, 96))
		self.img_2.fill((255, 255, 255))
		self.img_2_front.fill((24, 30, 196))
		self.img_2.blit(self.img_2_front, (2, 2))
		self.text = 'medium'
		self.font = pygame.font.Font('./resource/fonts/m04.ttf', 42)
		self.textRender = self.font.render(self.text, 1, (255, 255, 255))
		self.img_1.blit(self.textRender, (46, 29))
		self.img_2.blit(self.textRender, (46, 29))
		self.image = self.img_1
		self.rect = self.image.get_rect()
		self.rect.center = position
	def update(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(mouse_pos):
			self.image = self.img_2
		else:
			self.image = self.img_1


# 困难难度按钮
class HardButton(pygame.sprite.Sprite):
	def __init__(self, position=(400, 450)):
		pygame.sprite.Sprite.__init__(self)
		self.img_1 = pygame.Surface((285, 100))
		self.img_1_front = pygame.Surface((281, 96))
		self.img_1.fill((255, 255, 255))
		self.img_1_front.fill((0, 0, 0))
		self.img_1.blit(self.img_1_front, (2, 2))
		self.img_2 = pygame.Surface((285, 100))
		self.img_2_front = pygame.Surface((281, 96))
		self.img_2.fill((255, 255, 255))
		self.img_2_front.fill((196, 24, 24))
		self.img_2.blit(self.img_2_front, (2, 2))
		self.text = 'hard'
		self.font = pygame.font.Font('./resource/fonts/m04.ttf', 42)
		self.textRender = self.font.render(self.text, 1, (255, 255, 255))
		self.img_1.blit(self.textRender, (46, 29))
		self.img_2.blit(self.textRender, (46, 29))
		self.image = self.img_1
		self.rect = self.image.get_rect()
		self.rect.center = position
	def update(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(mouse_pos):
			self.image = self.img_2
		else:
			self.image = self.img_1


# 游戏模式选择界面
class CHOICE():
	def __init__(self, WIDTH, HEIGHT):
		# part1
		self.MCP = MapChoiceInterface(WIDTH, HEIGHT)
		self.MB1 = MapButton1()
		self.MB2 = MapButton2()
		self.MB3 = MapButton3()
		self.IB = InfoBox()
		# part2
		self.EB = EasyButton()
		self.MB = MediumButton()
		self.HB = HardButton()
	# 外部调用
	def update(self, screen):
		clock = pygame.time.Clock()
		# part1
		self.MBs = pygame.sprite.Group(self.MB1, self.MB2, self.MB3)
		map_choice, difficulty_choice = None, None
		while True:
			clock.tick(60)
			self.MCP.update()
			self.MBs.update()
			self.IB.update(self.MBs)
			screen.blit(self.MCP.image, self.MCP.rect)
			self.MBs.draw(screen)
			screen.blit(self.IB.image, self.IB.rect)
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
					pygame.quit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						mouse_pos = pygame.mouse.get_pos()
						idx = 0
						for mb in self.MBs:
							idx += 1
							if mb.rect.collidepoint(mouse_pos):
								map_choice = idx
			if map_choice:
				break
		# part2
		self.Bs = pygame.sprite.Group(self.EB, self.MB, self.HB)
		while True:
			clock.tick(60)
			screen.fill((0, 0, 0))
			self.Bs.update()
			self.Bs.draw(screen)
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
					pygame.quit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						mouse_pos = pygame.mouse.get_pos()
						idx = 0
						for b in self.Bs:
							idx += 1
							if b.rect.collidepoint(mouse_pos):
								difficulty_choice = b.text
			if difficulty_choice:
				break
		return map_choice, difficulty_choice