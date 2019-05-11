# 저자: Charles

# 공공 번호 : Charles의 피카츄

# 조류

import pygame





# Bird 종류

class Bird(pygame.sprite.Sprite):

	def __init__(self, HEIGHT, WIDTH):

		pygame.sprite.Sprite.__init__(self)

		# 기준

		self.ori_bird = pygame.image.load("./resources/images/bird.png")

		# 디스플레이

		self.rotated_bird = pygame.image.load("./resources/images/bird.png")

		self.rect = self.rotated_bird.get_rect()

		# 게임 인터페이스 너비와 높이

		self.HEIGHT = HEIGHT

		self.WIDTH = WIDTH

		# 각도

		self.angle = 0

		self.max_angle = 15

		# 속도

		self.angle_speed = 300

		self.down_speed = 300

		self.jump_speed = 150

		# 현재 점프 높이

		self.cur_jump_height = 0

		# 현재 점프 높이가 임계값에 도달하면 새가 점프를 완료합니다 

		self.jump_height_thresh = 8

		# 점프 여부

		self.is_jump = False

		# 위치 정보

		self.x = 150

		self.y = (self.HEIGHT - self.ori_bird.get_height()) / 2

		self.set_bird()

	# 새의 위치 설정

	def set_bird(self):

		self.rotated_bird = pygame.transform.rotate(self.ori_bird, self.angle)

		delta_width = (self.rotated_bird.get_rect().width - self.ori_bird.get_rect().width) / 2

		delta_height = (self.rotated_bird.get_rect().width - self.ori_bird.get_rect().height) / 2

		self.rect.left, self.rect.top = self.x - delta_width, self.y - delta_height

	# 새의 사망 여부 판단

	def is_dead(self):

		if self.y >= self.HEIGHT:

			return True

		else:

			return False

	# 새 업데이트

	def update(self, time_passed):

		if self.is_jump:

			if self.angle < self.max_angle:

				self.angle = min(time_passed * self.angle_speed + self.angle, self.max_angle)

				self.set_bird()

				return

			if self.cur_jump_height < self.jump_height_thresh:

				self.cur_jump_height += time_passed * self.jump_speed

				self.y = max(0, self.y - self.cur_jump_height)

				self.set_bird()

				return

			self.cur_jump_height = 0

			self.is_jump = False

		if self.angle > -self.max_angle:

			self.angle = max(-self.max_angle, self.angle - self.angle_speed * time_passed)

			self.set_bird()

			return

		self.y += self.down_speed * time_passed

		self.set_bird()

	# 재설정(초기화)

	def reset(self):

		self.angle = 0

		self.cur_jump_height = 0

		self.is_jump = False

		self.x = 150

		self.y = (self.HEIGHT - self.ori_bird.get_height()) / 2

		self.set_bird()
