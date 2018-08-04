# 作者: Charles
# 公众号: Charles的皮卡丘
# 鸟类
import pygame


# Bird类
class Bird(pygame.sprite.Sprite):
	def __init__(self, HEIGHT, WIDTH):
		pygame.sprite.Sprite.__init__(self)
		# 基准
		self.ori_bird = pygame.image.load("./resources/images/bird.png")
		# 显示用
		self.rotated_bird = pygame.image.load("./resources/images/bird.png")
		self.rect = self.rotated_bird.get_rect()
		# 游戏界面宽高
		self.HEIGHT = HEIGHT
		self.WIDTH = WIDTH
		# 角度
		self.angle = 0
		self.max_angle = 15
		# 速度
		self.angle_speed = 300
		self.down_speed = 300
		self.jump_speed = 150
		# 当前跳跃的高度
		self.cur_jump_height = 0
		# 当前跳跃高度到达该阈值时小鸟完成一次跳跃
		self.jump_height_thresh = 8
		# 是否跳跃
		self.is_jump = False
		# 位置信息
		self.x = 150
		self.y = (self.HEIGHT - self.ori_bird.get_height()) / 2
		self.set_bird()
	# 设置小鸟的位置
	def set_bird(self):
		self.rotated_bird = pygame.transform.rotate(self.ori_bird, self.angle)
		delta_width = (self.rotated_bird.get_rect().width - self.ori_bird.get_rect().width) / 2
		delta_height = (self.rotated_bird.get_rect().width - self.ori_bird.get_rect().height) / 2
		self.rect.left, self.rect.top = self.x - delta_width, self.y - delta_height
	# 判断小鸟是否死亡
	def is_dead(self):
		if self.y >= self.HEIGHT:
			return True
		else:
			return False
	# 更新小鸟
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
	# 重置
	def reset(self):
		self.angle = 0
		self.cur_jump_height = 0
		self.is_jump = False
		self.x = 150
		self.y = (self.HEIGHT - self.ori_bird.get_height()) / 2
		self.set_bird()