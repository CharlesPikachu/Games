# 저자: Charles 

# 공공 번호 : Charles의 피카츄

# 파이프 라인 클래스

import pygame

import random





# 파이프 헤드

class pipeHead(pygame.sprite.Sprite):

	def __init__(self):

		pygame.sprite.Sprite.__init__(self)

		self.pipe_head = pygame.image.load("./resources/images/pipe_head.png")

		self.img = self.pipe_head

		self.rect = self.pipe_head.get_rect()

		self.height = self.pipe_head.get_height()

		self.width = self.pipe_head.get_width()





# 파이프 몸체

class pipeBody(pygame.sprite.Sprite):

	def __init__(self):

		pygame.sprite.Sprite.__init__(self)

		self.pipe_body = pygame.image.load("./resources/images/pipe_body.png")

		self.img = self.pipe_body

		self.rect = self.pipe_body.get_rect()

		self.height = self.pipe_body.get_height()

		self.width = self.pipe_body.get_width()





# 파이프 라인 클래스 

class Pipe():

	def __init__(self, HEIGHT, WIDTH):

		# 게임 인터페이스 너비와 높이

		self.HEIGHT = HEIGHT

		self.WIDTH = WIDTH

		# 파이프 몸체는 몇 개까지 놓을 수 있다

		self.max_pipe_body = (self.HEIGHT - 2 * pipeHead().height) // pipeBody().height

		# void (새들이 지나가려면 pipeBody (). height는 단위 길이입니다)

		self.interspace = 8

		# 파이프 몸체 상부

		self.n_up_pipe_body = random.randint(0, self.max_pipe_body-self.interspace)

		# 파이프 몸체 하부

		self.n_down_pipe_body = self.max_pipe_body - self.interspace - self.n_up_pipe_body

		# 위치

		self.x = 600

		# 속도 (즉, 새 속도)

		self.speed = 100

		# 새가 파이프를 지나간 후 참으로 바뀌어 반복 방지
		self.add_score = False

		self.construct_pipe()

	# 파이프 본체와 파이프 헤드로 파이프를 구성

	def construct_pipe(self):

		# 파이프

		self.pipe = pygame.sprite.Group()

		# 윗부분

		for i in range(self.n_up_pipe_body):

			pipe_body = pipeBody()

			pipe_body.rect.left, pipe_body.rect.top = self.x, i * pipe_body.height

			self.pipe.add(pipe_body)

		pipe_head = pipeHead()

		pipe_head.rect.left, pipe_head.rect.top = self.x - (pipeHead().width - pipeBody().width) / 2, self.n_up_pipe_body * pipeBody().height

		self.pipe.add(pipe_head)

		# 아랫부분

		for i in range(self.n_down_pipe_body):

			pipe_body = pipeBody()

			pipe_body.rect.left, pipe_body.rect.top = self.x, self.HEIGHT - (i + 1) * pipeBody().height

			self.pipe.add(pipe_body)

		pipe_head = pipeHead()

		pipe_head.rect.left, pipe_head.rect.top = self.x - (pipeHead().width - pipeBody().width) / 2, self.HEIGHT - self.n_down_pipe_body * pipeBody().height - pipeHead().height

		self.pipe.add(pipe_head)

	# 업데이트 파이프 라인

	def update(self, time_passed):

		self.x -= time_passed * self.speed

		self.construct_pipe()
