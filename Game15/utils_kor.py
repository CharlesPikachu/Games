'''
Function:
	도구 함수
Author:
	Charles
WeChat 공개번호:
	Charles의 피카츄
'''
import sys
import time
import random
import pygame
from config import *


'''퍼즐 클래스'''
class gemSprite(pygame.sprite.Sprite):
	def __init__(self, img_path, size, position, downlen, **kwargs):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(img_path)
		self.image = pygame.transform.smoothscale(self.image, size)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = position
		self.downlen = downlen
		self.target_x = position[0]
		self.target_y = position[1] + downlen
		self.type = img_path.split('/')[-1].split('.')[0]
		self.fixed = False
		self.speed_x = 10
		self.speed_y = 10
		self.direction = 'down'
	'''퍼즐조각의 움직임'''
	def move(self):
		if self.direction == 'down':
			self.rect.top = min(self.target_y, self.rect.top+self.speed_y)
			if self.target_y == self.rect.top:
				self.fixed = True
		elif self.direction == 'up':
			self.rect.top = max(self.target_y, self.rect.top-self.speed_y)
			if self.target_y == self.rect.top:
				self.fixed = True
		elif self.direction == 'left':
			self.rect.left = max(self.target_x, self.rect.left-self.speed_x)
			if self.target_x == self.rect.left:
				self.fixed = True
		elif self.direction == 'right':
			self.rect.left = min(self.target_x, self.rect.left+self.speed_x)
			if self.target_x == self.rect.left:
				self.fixed = True
	'''좌표 얻기'''
	def getPosition(self):
		return self.rect.left, self.rect.top
	'''좌표 설정'''
	def setPosition(self, position):
		self.rect.left, self.rect.top = position


'''게임 클래스'''
class gemGame():
	def __init__(self, screen, sounds, font, gem_imgs, **kwargs):
		self.info = 'Gemgem-微信公众号:Charles的皮卡丘'#젬젬-WeChat 공개번호 : Charles의 피카츄
		self.screen = screen
		self.sounds = sounds
		self.font = font
		self.gem_imgs = gem_imgs
		self.reset()
	'''게임 시작'''
	def start(self):
		clock = pygame.time.Clock()
		# 전체 게임 인터페이스 업데이트 위치 탐색
		overall_moving = True
		# 개별 개체 업데이트 위치 지정
		individual_moving = False
		# 필요한 몇가지 변수를 정의하기
		gem_selected_xy = None
		gem_selected_xy2 = None
		swap_again = False
		add_score = 0
		add_score_showtimes = 10
		time_pre = int(time.time())
		# 메인 게임루프
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
					pygame.quit()
					sys.exit()
				elif event.type == pygame.MOUSEBUTTONUP:
					if (not overall_moving) and (not individual_moving) and (not add_score):
						position = pygame.mouse.get_pos()
						if gem_selected_xy is None:
							gem_selected_xy = self.checkSelected(position)
						else:
							gem_selected_xy2 = self.checkSelected(position)
							if gem_selected_xy2:
								if self.swapGem(gem_selected_xy, gem_selected_xy2):
									individual_moving = True
									swap_again = False
								else:
									gem_selected_xy = None
			if overall_moving:
				overall_moving = not self.dropGems(0, 0)
				# 게임의 메인 루프가 한번 움직이면 여러개의 3블록을 사용할 수 있다.
				if not overall_moving:
					res_match = self.isMatch()
					add_score = self.removeMatched(res_match)
					if add_score > 0:
						overall_moving = True
			if individual_moving:
				gem1 = self.getGemByPos(*gem_selected_xy)
				gem2 = self.getGemByPos(*gem_selected_xy2)
				gem1.move()
				gem2.move()
				if gem1.fixed and gem2.fixed:
					res_match = self.isMatch()
					if res_match[0] == 0 and not swap_again:
						swap_again = True
						self.swapGem(gem_selected_xy, gem_selected_xy2)
						self.sounds['mismatch'].play()
					else:
						add_score = self.removeMatched(res_match)
						overall_moving = True
						individual_moving = False
						gem_selected_xy = None
						gem_selected_xy2 = None
			self.screen.fill((135, 206, 235))
			self.drawGrids()
			self.gems_group.draw(self.screen)
			if gem_selected_xy:
				self.drawBlock(self.getGemByPos(*gem_selected_xy).rect)
			if add_score:
				if add_score_showtimes == 10:
					random.choice(self.sounds['match']).play()
				self.drawAddScore(add_score)
				add_score_showtimes -= 1
				if add_score_showtimes < 1:
					add_score_showtimes = 10
					add_score = 0
			self.remaining_time -= (int(time.time()) - time_pre)
			time_pre = int(time.time())
			self.showRemainingTime()
			self.drawScore()
			if self.remaining_time <= 0:
				return self.score
			pygame.display.update()
			clock.tick(FPS)
	'''초기화'''
	def reset(self):
		# 무작위로 각 블록을 생성 (즉, 게임 맵의 요소를 초기화)
		while True:
			self.all_gems = []
			self.gems_group = pygame.sprite.Group()
			for x in range(NUMGRID):
				self.all_gems.append([])
				for y in range(NUMGRID):
					gem = gemSprite(img_path=random.choice(self.gem_imgs), size=(GRIDSIZE, GRIDSIZE), position=[XMARGIN+x*GRIDSIZE, YMARGIN+y*GRIDSIZE-NUMGRID*GRIDSIZE], downlen=NUMGRID*GRIDSIZE)
					self.all_gems[x].append(gem)
					self.gems_group.add(gem)
			if self.isMatch()[0] == 0:
				break
		# 점수
		self.score = 0
		# 보상을 주기
		self.reward = 10
		# 시간
		self.remaining_time = 300
	'''남은 시간 표시'''
	def showRemainingTime(self):
		remaining_time_render = self.font.render('CountDown: %ss' % str(self.remaining_time), 1, (85, 65, 0))
		rect = remaining_time_render.get_rect()
		rect.left, rect.top = (WIDTH-201, 6)
		self.screen.blit(remaining_time_render, rect)
	'''점수 표시'''
	def drawScore(self):
		score_render = self.font.render('SCORE:'+str(self.score), 1, (85, 65, 0))
		rect = score_render.get_rect()
		rect.left, rect.top = (10, 6)
		self.screen.blit(score_render, rect)
	'''추가 포인트 표시'''
	def drawAddScore(self, add_score):
		score_render = self.font.render('+'+str(add_score), 1, (255, 100, 100))
		rect = score_render.get_rect()
		rect.left, rect.top = (250, 250)
		self.screen.blit(score_render, rect)
	'''새로운 퍼즐 조각을 생성하기'''
	def generateNewGems(self, res_match):
		if res_match[0] == 1:
			start = res_match[2]
			while start > -2:
				for each in [res_match[1], res_match[1]+1, res_match[1]+2]:
					gem = self.getGemByPos(*[each, start])
					if start == res_match[2]:
						self.gems_group.remove(gem)
						self.all_gems[each][start] = None
					elif start >= 0:
						gem.target_y += GRIDSIZE
						gem.fixed = False
						gem.direction = 'down'
						self.all_gems[each][start+1] = gem
					else:
						gem = gemSprite(img_path=random.choice(self.gem_imgs), size=(GRIDSIZE, GRIDSIZE), position=[XMARGIN+each*GRIDSIZE, YMARGIN-GRIDSIZE], downlen=GRIDSIZE)
						self.gems_group.add(gem)
						self.all_gems[each][start+1] = gem
				start -= 1
		elif res_match[0] == 2:
			start = res_match[2]
			while start > -4:
				if start == res_match[2]:
					for each in range(0, 3):
						gem = self.getGemByPos(*[res_match[1], start+each])
						self.gems_group.remove(gem)
						self.all_gems[res_match[1]][start+each] = None
				elif start >= 0:
					gem = self.getGemByPos(*[res_match[1], start])
					gem.target_y += GRIDSIZE * 3
					gem.fixed = False
					gem.direction = 'down'
					self.all_gems[res_match[1]][start+3] = gem
				else:
					gem = gemSprite(img_path=random.choice(self.gem_imgs), size=(GRIDSIZE, GRIDSIZE), position=[XMARGIN+res_match[1]*GRIDSIZE, YMARGIN+start*GRIDSIZE], downlen=GRIDSIZE*3)
					self.gems_group.add(gem)
					self.all_gems[res_match[1]][start+3] = gem
				start -= 1
	'''일치하는 젬(보석) 제거'''
	def removeMatched(self, res_match):
		if res_match[0] > 0:
			self.generateNewGems(res_match)
			self.score += self.reward
			return self.reward
		return 0
	'''게임 인터페이스 그리드 그리기'''
	def drawGrids(self):
		for x in range(NUMGRID):
			for y in range(NUMGRID):
				rect = pygame.Rect((XMARGIN+x*GRIDSIZE, YMARGIN+y*GRIDSIZE, GRIDSIZE, GRIDSIZE))
				self.drawBlock(rect, color=(0, 0, 255), size=1)
	'''직사각형 블록 프레임 그리기'''
	def drawBlock(self, block, color=(255, 0, 255), size=4):
		pygame.draw.rect(self.screen, color, block, size)
	'''드롭효과'''
	def dropGems(self, x, y):
		if not self.getGemByPos(x, y).fixed:
			self.getGemByPos(x, y).move()
		if x < NUMGRID-1:
			x += 1
			return self.dropGems(x, y)
		elif y < NUMGRID-1:
			x = 0
			y += 1
			return self.dropGems(x, y)
		else:
			return self.isFull()
	'''모든 위치에 퍼즐 조각이 있는지 여부 확인'''
	def isFull(self):
		for x in range(NUMGRID):
			for y in range(NUMGRID):
				if not self.getGemByPos(x, y).fixed:
					return False
		return True
	'''퍼즐 조각이 선택 되었는지 확인하기'''
	def checkSelected(self, position):
		for x in range(NUMGRID):
			for y in range(NUMGRID):
				if self.getGemByPos(x, y).rect.collidepoint(*position):
					return [x, y]
		return None
	'''연속적으로 세 블록이 있습니까?(no-return 0 / level - return 1 / vertical - return 2)'''
	def isMatch(self):
		for x in range(NUMGRID):
			for y in range(NUMGRID):
				if x + 2 < NUMGRID:
					if self.getGemByPos(x, y).type == self.getGemByPos(x+1, y).type == self.getGemByPos(x+2, y).type:
						return [1, x, y]
				if y + 2 < NUMGRID:
					if self.getGemByPos(x, y).type == self.getGemByPos(x, y+1).type == self.getGemByPos(x, y+2).type:
						return [2, x, y]
		return [0, x, y]
	'''죄표에 따라 해당 위치에 해당하는 퍼즐 개체를 가져온다'''
	def getGemByPos(self, x, y):
		return self.all_gems[x][y]
	'''퍼즐 교환'''
	def swapGem(self, gem1_pos, gem2_pos):
		margin = gem1_pos[0] - gem2_pos[0] + gem1_pos[1] - gem2_pos[1]
		if abs(margin) != 1:
			return False
		gem1 = self.getGemByPos(*gem1_pos)
		gem2 = self.getGemByPos(*gem2_pos)
		if gem1_pos[0] - gem2_pos[0] == 1:
			gem1.direction = 'left'
			gem2.direction = 'right'
		elif gem1_pos[0] - gem2_pos[0] == -1:
			gem2.direction = 'left'
			gem1.direction = 'right'
		elif gem1_pos[1] - gem2_pos[1] == 1:
			gem1.direction = 'up'
			gem2.direction = 'down'
		elif gem1_pos[1] - gem2_pos[1] == -1:
			gem2.direction = 'up'
			gem1.direction = 'down'
		gem1.target_x = gem2.rect.left
		gem1.target_y = gem2.rect.top
		gem1.fixed = False
		gem2.target_x = gem1.rect.left
		gem2.target_y = gem1.rect.top
		gem2.fixed = False
		self.all_gems[gem2_pos[0]][gem2_pos[1]] = gem1
		self.all_gems[gem1_pos[0]][gem1_pos[1]] = gem2
		return True
	'''info'''
	def __repr__(self):
		return self.info