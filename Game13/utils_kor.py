'''
Function:
	일부 종류/함수 정의
Author:
	Charles
닉네임:
	Charles의 피카츄
'''
import sys
import pygame
	

	

'''표시자'''
def showText(screen, text, color, font, x, y):
	text = font.render(text, True, color)
	screen.blit(text, (x, y))
	

	

'''생명값과 같은 수의 비행선 표시(오른쪽 상단)'''
def showLife(screen, num_life, color):
	cell = [2, 2]
	num_cols = 15
	filled_cells = [7,21,22,23,36,37,38,46,47,48,49,50,51,52,53,54,55,56,57,58,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119]
	for i in range(num_life):
		position = [750-35*i, 8]
		for i in range(0, len(filled_cells)):
			y = filled_cells[i] // num_cols
			x = filled_cells[i] % num_cols
			rect = [x * cell[0] + position[0], y * cell[1] + position[1], cell[0], cell[1]]
			pygame.draw.rect(screen, color, rect)
	

	

'''인터페이스 끝냄'''
def endInterface(screen, color, is_win):
	screen.fill(color)
	clock = pygame.time.Clock()
	if is_win:
		text = 'VICTORY'
	else:
		text = 'FAILURE'
	font = pygame.font.SysFont('arial', 30)
	text_render = font.render(text, 1, (255, 255, 255))
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if (event.type == pygame.KEYDOWN) or (event.type == pygame.MOUSEBUTTONDOWN):
				return
		screen.blit(text_render, (350, 300))
		clock.tick(60)
		pygame.display.update()
	

	

'''우리측 비행선'''
class aircraftSprite(pygame.sprite.Sprite):
	def __init__(self, color, bullet_color, **kwargs):
		pygame.sprite.Sprite.__init__(self)
		# 체력
		self.num_life = 3
		self.max_num_life = 5
		# 최소 셀
		self.cell = [3, 3]
		self.num_cols = 15
		self.num_rows = 8
		# 충돌 감지에 사용
		self.rect = pygame.Rect(0, 550, self.cell[0]*self.num_cols, self.cell[0]*self.num_rows)
		# 채우기 색 영역
		self.filled_cells = [7,21,22,23,36,37,38,46,47,48,49,50,51,52,53,54,55,56,57,58,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119]
		# 비행선 색
		self.color = color
		# 우주선 탄알 색
		self.bullet_color = bullet_color
		# 총알이 냉각 중인지 여부
		self.is_cooling = False
		self.init_count = 35
		self.cooling_count = self.init_count
		# 득점
		self.score = 0
		# 	생명을 중복적으로 증가시키는 것 피하기
		self.old_score = -1
		self.resetBoom()
	'''사격'''
	def shot(self):
		if self.is_cooling:
			return None
		self.is_cooling = True
		self.cooling_count = self.init_count
		return myBulletSprite(self.rect.x + self.rect.width // 2, self.rect.y, self.bullet_color)
	'''스크린에 그림'''
	def draw(self, screen):
		for i in range(0, len(self.filled_cells)):
			y = self.filled_cells[i] // self.num_cols
			x = self.filled_cells[i] % self.num_cols
			rect = [x * self.cell[0] + self.rect[0], y * self.cell[1] + self.rect[1], self.cell[0], self.cell[1]]
			pygame.draw.rect(screen, self.color, rect)
	'''비행선 위치 등의 정보 업데이트'''
	def update(self, WIDTH):
		# 위치 정보
		x = pygame.mouse.get_pos()[0] - (self.rect.width // 2)
		if x < 0:
			x = pygame.mouse.get_pos()[0]
		elif x > WIDTH - self.rect.width:
			x = WIDTH - self.rect.width
		self.rect.x = x
		# 총알 정보
		if self.is_cooling:
			self.cooling_count -= 1
			if self.cooling_count == 0:
				self.is_cooling = False
	'''맞아서 폭발'''
	def boom(self, screen):
		self.boomed_rect.x = self.rect.x
		self.boomed_rect.y = self.rect.y
		self.boomed_count += 1
		if self.boomed_count % 1 == 0:
			self.boomed_frame += 1
			for i in range(0, len(self.boomed_filled_cells)):
				y = self.boomed_filled_cells[i] // self.boomed_num_cols
				x = self.boomed_filled_cells[i] % self.boomed_num_cols
				rect = [x * self.boomed_cell[0] + self.boomed_rect[0], y * self.boomed_cell[1] + self.boomed_rect[1], self.boomed_cell[0], self.boomed_cell[1]]
				pygame.draw.rect(screen, self.color, rect)
		if self.boomed_frame > 4:
			return True
		else:
			return False
	'''폭발에 사용된 데이터 리셋'''
	def resetBoom(self):
		# 폭발할 때 씀
		# 	죽을 때 특수 효과 한번 방영
		self.one_dead = False
		self.boomed_filled_cells = [3,7,12,15,17,20,24,30,36,40,44,45,53,54,58,62,68,74,78,81,83,86,91,95]
		self.boomed_cell = [3, 3]
		self.boomed_num_cols = 11
		self.boomed_num_rows = 9
		self.boomed_rect = pygame.Rect(0, 0, self.boomed_num_cols*self.boomed_cell[0], self.boomed_num_rows*self.boomed_cell[1])
		# 	프레임 당 시간 제어
		self.boomed_count = 0
		#	폭발 특수 효과 현재 프레임
		self.boomed_frame = 0
	

	

'''ufo종류'''
class ufoSprite(pygame.sprite.Sprite):
	def __init__(self, color, **kwargs):
		pygame.sprite.Sprite.__init__(self)
		# 이것과 같은 종류의 인센티브 맞히다
		self.reward = 200
		self.color = color
		self.reset()
	'''스크린에 그림'''
	def draw(self, screen):
		if self.is_dead:
			return None
		for i in range(0, len(self.filled_cells)):
			y = self.filled_cells[i] // self.num_cols
			x = self.filled_cells[i] % self.num_cols
			rect = [x * self.cell[0] + self.rect[0], y * self.cell[1] + self.rect[1], self.cell[0], self.cell[1]]
			pygame.draw.rect(screen, self.color, rect)
	'''UFO위치 등의 정보 업데이트'''
	def update(self, WIDTH):
		if self.rect.x + self.rect.width < 0 or self.rect.x > WIDTH:
			self.rect.x += self.low_speed
		else:
			self.rect.x += self.high_speed
		if self.rect.x > WIDTH + 500:
			self.reset()
	'''맞아서 폭발'''
	def boom(self, screen):
		self.boomed_rect.x = self.rect.x
		self.boomed_rect.y = self.rect.y
		self.boomed_count += 1
		if self.boomed_count % 1 == 0:
			self.boomed_frame += 1
			for i in range(0, len(self.boomed_filled_cells)):
				y = self.boomed_filled_cells[i] // self.boomed_num_cols
				x = self.boomed_filled_cells[i] % self.boomed_num_cols
				rect = [x * self.boomed_cell[0] + self.boomed_rect[0], y * self.boomed_cell[1] + self.boomed_rect[1], self.boomed_cell[0], self.boomed_cell[1]]
				pygame.draw.rect(screen, self.color, rect)
		if self.boomed_frame > 4:
			return True
		else:
			return False
	'''리셋'''
	def reset(self):
		self.cell = [3, 3]
		self.num_cols = 16
		self.num_rows = 7
		self.rect = pygame.Rect(-500-self.num_cols*self.cell[0], 60, self.num_cols*self.cell[0], self.num_rows*self.cell[1])
		self.filled_cells = [5,6,7,8,9,10,19,20,21,22,23,24,25,26,27,28,34,35,36,37,38,39,40,41,42,43,44,45,49,50,52,53,55,56,58,59,61,62,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,82,83,84,87,88,91,92,93,99,108]
		self.low_speed = 1
		self.high_speed = 2
		self.is_dead = False
		# 폭발할 때 씀
		# 	폭발의 특효가 이미 나와있는지
		self.has_boomed = False
		self.boomed_filled_cells = [3,7,12,15,17,20,24,30,36,40,44,45,53,54,58,62,68,74,78,81,83,86,91,95]
		self.boomed_cell = [3, 3]
		self.boomed_num_cols = 11
		self.boomed_num_rows = 9
		self.boomed_rect = pygame.Rect(0, 0, self.boomed_num_cols*self.boomed_cell[0], self.boomed_num_rows*self.boomed_cell[1])
		self.boomed_count = 0
		self.boomed_frame = 0
	

	

'''적방류'''
class enemySprite(pygame.sprite.Sprite):
	def __init__(self, category, number, color, bullet_color, **kwargs):
		pygame.sprite.Sprite.__init__(self)
		self.cell = [3, 3]
		# 번호
		self.number = number
		# 종류
		self.category = category
		if category == 'small':
			self.reward = 20
			self.num_cols = 8
			self.num_rows = 8
			self.rect = pygame.Rect(0, 0, self.num_cols*self.cell[0], self.num_rows*self.cell[1])
			self.filled_cells = [[3,4,10,11,12,13,17,18,19,20,21,22,24,25,27,28,30,31,32,33,34,35,36,37,38,39,42,45,49,51,52,54,56,58,61,63], 
									[3,4,10,11,12,13,17,18,19,20,21,22,24,25,27,28,30,31,32,33,34,35,36,37,38,39,41,43,44,46,48,55,57,62]]
		elif category == 'medium':
			self.reward = 15
			self.num_cols = 11
			self.num_rows = 8
			self.rect = pygame.Rect(0, 0, self.num_cols*self.cell[0], self.num_rows*self.cell[1])
			self.filled_cells = [[2,8,11,14,18,21,22,24,25,26,27,28,29,30,32,33,34,35,37,38,39,41,42,43,44,45,46,47,48,49,50,51,52,53,54,56,57,58,59,60,61,62,63,64,68,74,78,86], 
									 [2,8,14,18,24,25,26,27,28,29,30,34,35,37,38,39,41,42,44,45,46,47,48,49,50,51,52,53,54,55,57,58,59,60,61,62,63,65,66,68,74,76,80,81,83,84]]
		elif category == 'large':
			self.reward = 10
			self.num_cols = 12
			self.num_rows = 8
			self.rect = pygame.Rect(0, 0, self.num_cols*self.cell[0], self.num_rows*self.cell[1])
			self.filled_cells = [[4,5,6,7,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,41,42,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,62,63,64,67,68,69,73,74,77,78,81,82,86,87,92,93], 
									 [4,5,6,7,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,41,42,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,63,64,67,68,74,75,77,78,80,81,84,85,94,95]]
		self.color = color
		self.bullet_color = bullet_color
		self.speed = [8, 20]
		self.change_count = 0
		self.change_flag = False
		# 맞아서 폭발할 때 씀
		self.boomed_filled_cells = [3,7,12,15,17,20,24,30,36,40,44,45,53,54,58,62,68,74,78,81,83,86,91,95]
		self.boomed_cell = [3, 3]
		self.boomed_num_cols = 11
		self.boomed_num_rows = 9
		self.boomed_rect = pygame.Rect(0, 0, self.boomed_num_cols*self.boomed_cell[0], self.boomed_num_rows*self.boomed_cell[1])
		self.boomed_count = 0
		self.boomed_frame = 0
	'''사격'''
	def shot(self):
		return enemyBulletSprite(self.rect.x + self.rect.width // 2, self.rect.y, self.bullet_color)
	'''스크린에 그림'''
	def draw(self, screen):
		if self.change_count > 50:
			self.change_count = 0
			self.change_flag = not self.change_flag
		if self.change_flag:
			for i in range(0, len(self.filled_cells[0])):
				y = self.filled_cells[0][i] // self.num_cols
				x = self.filled_cells[0][i] % self.num_cols
				rect = [x * self.cell[0] + self.rect[0], y * self.cell[1] + self.rect[1], self.cell[0], self.cell[1]]
				pygame.draw.rect(screen, self.color, rect)
		else:
			for i in range(0, len(self.filled_cells[1])):
				y = self.filled_cells[1][i] // self.num_cols
				x = self.filled_cells[1][i] % self.num_cols
				rect = [x * self.cell[0] + self.rect[0], y * self.cell[1] + self.rect[1], self.cell[0], self.cell[1]]
				pygame.draw.rect(screen, self.color, rect)
	'''적 위치 등의 정보 업데이트'''
	def update(self, direction, HEIGHT):
		# 모양 바꾸는데 사용
		self.change_count += 1
		# 위치 정보 업데이트
		if direction == 'right':
			self.rect.x += self.speed[0]
		elif direction == 'left':
			self.rect.x -= self.speed[0]
		elif direction == 'down':
			self.rect.y += self.speed[1]
		if self.rect.y >= HEIGHT - self.rect.height:
			return True
		else:
			return False
	'''맞아서 폭발'''
	def boom(self, screen):
		self.boomed_rect.x = self.rect.x
		self.boomed_rect.y = self.rect.y
		self.boomed_count += 1
		if self.boomed_count % 1 == 0:
			self.boomed_frame += 1
			for i in range(0, len(self.boomed_filled_cells)):
				y = self.boomed_filled_cells[i] // self.boomed_num_cols
				x = self.boomed_filled_cells[i] % self.boomed_num_cols
				rect = [x * self.boomed_cell[0] + self.boomed_rect[0], y * self.boomed_cell[1] + self.boomed_rect[1], self.boomed_cell[0], self.boomed_cell[1]]
				pygame.draw.rect(screen, self.color, rect)
		if self.boomed_frame > 4:
			return True
		else:
			return False
	

	

'''우리쪽 총알 요정류'''
class myBulletSprite(pygame.sprite.Sprite):
	def __init__(self, x, y, color, **kwargs):
		pygame.sprite.Sprite.__init__(self)
		self.cell = [2, 2]
		self.num_cols = 1
		self.num_rows = 4
		self.rect = pygame.Rect(x, y, self.num_cols*self.cell[0], self.num_rows*self.cell[1])
		self.filled_cells = [0,1,2,3]
		self.speed = 8
		self.color = color
	'''스크린에 그림'''
	def draw(self, screen):
		for i in range(0, len(self.filled_cells)):
			y = self.filled_cells[i] // self.num_cols
			x = self.filled_cells[i] % self.num_cols
			rect = [x * self.cell[0] + self.rect[0], y * self.cell[1] + self.rect[1], self.cell[0], self.cell[1]]
			pygame.draw.rect(screen, self.color, rect)
	'''탄환 위치 등의 정보 갱신'''
	def update(self):
		self.rect.y -= self.speed
		if self.rect.y + self.rect.height < 0:
			return True
		else:
			return False
	

	

'''적탄요정류'''
class enemyBulletSprite(pygame.sprite.Sprite):
	def __init__(self, x, y, color):
		pygame.sprite.Sprite.__init__(self)
		self.cell = [3, 3]
		self.num_cols = 3
		self.num_rows = 7
		self.rect = pygame.Rect(x, y, self.num_cols*self.cell[0], self.num_rows*self.cell[1])
		self.filled_cells = [[0,4,8,10,12,16,20], 
								[2,4,6,10,14,16,18]]
		self.change_count = 0
		self.change_flag = False
		self.speed = 4
		self.color = color
	'''스크린에 그림'''
	def draw(self, screen):
		if self.change_count > 2:
			self.change_count = 0
			self.change_flag = not self.change_flag
		if self.change_flag:
			for i in range(0, len(self.filled_cells[0])):
				y = self.filled_cells[0][i] // self.num_cols
				x = self.filled_cells[0][i] % self.num_cols
				rect = [x * self.cell[0] + self.rect[0], y * self.cell[1] + self.rect[1], self.cell[0], self.cell[1]]
				pygame.draw.rect(screen, self.color, rect)
		else:
			for i in range(0, len(self.filled_cells[1])):
				y = self.filled_cells[1][i] // self.num_cols
				x = self.filled_cells[1][i] % self.num_cols
				rect = [x * self.cell[0] + self.rect[0], y * self.cell[1] + self.rect[1], self.cell[0], self.cell[1]]
				pygame.draw.rect(screen, self.color, rect)
	'''탄환 위치 등의 정보 갱신'''
	def update(self, HEIGHT):
		#총알 모양 바꾸는데 사용되는 계수
		self.change_count += 1
		# 위치 정보
		self.rect.y += self.speed
		if self.rect.y > HEIGHT:
			return True
		else:
			return False
