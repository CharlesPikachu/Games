# 恐龙类
# 作者: Charles
# 公众号: Charles的皮卡丘
import pygame


# 恐龙类
class Dinosaur(pygame.sprite.Sprite):
	def __init__(self, WIDTH=640, HEIGHT=500):
		pygame.sprite.Sprite.__init__(self)
		self.HEIGHT = HEIGHT
		self.WIDTH = WIDTH
		# self.imgs = ['./images/dinosaur/wait.png', './images/dinosaur/afraid.png', './images/dinosaur/running.png', './images/dinosaur/flying.png']
		self.imgs = ['./images/dinosaur/dino.png', './images/dinosaur/dino_ducking.png']
		self.reset()
	# 跳跃
	def jump(self, time_passed):
		# time_passed很小时，可近似为匀速运动
		if self.is_jumping_up:
			self.rect.top -= self.jump_v * time_passed
			self.jump_v = max(0, self.jump_v - self.jump_a_up * time_passed)
			if self.jump_v == 0:
				self.is_jumping_up = False
		else:
			self.rect.top = min(self.initial_top, self.rect.top + self.jump_v * time_passed)
			self.jump_v += self.jump_a_down * time_passed
			if self.rect.top == self.initial_top:
				self.is_jumping = False
				self.is_jumping_up = True
				self.jump_v = self.jump_v0
	# 跳跃时变为感到恐惧的表情
	def be_afraid(self):
		self.dinosaur = self.dinosaurs.subsurface((352, 0), (88, 95))
	# 把自己画到屏幕上去
	def draw(self, screen):
		if self.is_running and not self.is_jumping:
			self.running_count += 1
			if self.running_count == 6:
				self.running_count = 0
				self.running_flag = not self.running_flag
			if self.running_flag:
				self.dinosaur = self.dinosaurs.subsurface((176, 0), (88, 95))
			else:
				self.dinosaur = self.dinosaurs.subsurface((264, 0), (88, 95))
		screen.blit(self.dinosaur, self.rect)
	# 重置
	def reset(self):
		# 恐龙是否在奔跑
		self.is_running = False
		# 为了奔跑特效
		self.running_flag = False
		self.running_count = 0
		# 恐龙是否在跳跃
		self.is_jumping = False
		# 恐龙是否在向上跳跃
		self.is_jumping_up = True
		# 跳跃初始速度
		self.jump_v0 = 500
		# 跳跃瞬时速度
		self.jump_v = self.jump_v0
		# 跳跃加速度
		self.jump_a_up = 1000
		self.jump_a_down = 800
		# 小恐龙初始位置
		self.initial_left = 40
		self.initial_top = int(self.HEIGHT/2.3)
		self.dinosaurs = pygame.image.load(self.imgs[0]).convert_alpha()
		self.dinosaur = self.dinosaurs.subsurface((0, 0), (88, 95))
		self.rect = self.dinosaur.get_rect()
		self.rect.left, self.rect.top = self.initial_left, self.initial_top