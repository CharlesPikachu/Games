# 作者: Charles
# 公众号: Charles的皮卡丘
# 管道类
import pygame
import random


# 管道头
class pipeHead(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.pipe_head = pygame.image.load("./resources/images/pipe_head.png")
		self.img = self.pipe_head
		self.rect = self.pipe_head.get_rect()
		self.height = self.pipe_head.get_height()
		self.width = self.pipe_head.get_width()


# 管道体
class pipeBody(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.pipe_body = pygame.image.load("./resources/images/pipe_body.png")
		self.img = self.pipe_body
		self.rect = self.pipe_body.get_rect()
		self.height = self.pipe_body.get_height()
		self.width = self.pipe_body.get_width()


# 管道类
class Pipe():
	def __init__(self, HEIGHT, WIDTH):
		# 游戏界面宽高
		self.HEIGHT = HEIGHT
		self.WIDTH = WIDTH
		# 管道体最多可以放几个
		self.max_pipe_body = (self.HEIGHT - 2 * pipeHead().height) // pipeBody().height
		# 空隙(供小鸟穿过用，以pipeBody().height为单位长度)
		self.interspace = 8
		# 上方管道体
		self.n_up_pipe_body = random.randint(0, self.max_pipe_body-self.interspace)
		# 下方管道体
		self.n_down_pipe_body = self.max_pipe_body - self.interspace - self.n_up_pipe_body
		# 位置
		self.x = 600
		# 速度(即小鸟前进速度)
		self.speed = 100
		# 小鸟通过该Pipe后变为True，防止重复加分
		self.add_score = False
		self.construct_pipe()
	# 用管道体和管道头构建管道
	def construct_pipe(self):
		# 管道
		self.pipe = pygame.sprite.Group()
		# 上半部分
		for i in range(self.n_up_pipe_body):
			pipe_body = pipeBody()
			pipe_body.rect.left, pipe_body.rect.top = self.x, i * pipe_body.height
			self.pipe.add(pipe_body)
		pipe_head = pipeHead()
		pipe_head.rect.left, pipe_head.rect.top = self.x - (pipeHead().width - pipeBody().width) / 2, self.n_up_pipe_body * pipeBody().height
		self.pipe.add(pipe_head)
		# 下半部分
		for i in range(self.n_down_pipe_body):
			pipe_body = pipeBody()
			pipe_body.rect.left, pipe_body.rect.top = self.x, self.HEIGHT - (i + 1) * pipeBody().height
			self.pipe.add(pipe_body)
		pipe_head = pipeHead()
		pipe_head.rect.left, pipe_head.rect.top = self.x - (pipeHead().width - pipeBody().width) / 2, self.HEIGHT - self.n_down_pipe_body * pipeBody().height - pipeHead().height
		self.pipe.add(pipe_head)
	# 更新管道
	def update(self, time_passed):
		self.x -= time_passed * self.speed
		self.construct_pipe()