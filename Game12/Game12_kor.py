'''
	Author:
		Charles
	Function:
		상자 밀기 게임
	닉네임:
		Charles의 피카츄
	'''
import os
import sys
import pygame
from Sprites import *
from config import Config
from itertools import chain
	

	

'''
Function:
		게임 나가기
'''
def quitGame():
	pygame.quit()
	sys.exit(0)
	

	

'''
Function:
		게임 지도
'''
class gameMap():
	def __init__(self, num_cols, num_rows):
		self.walls = []
		self.boxes = []
		self.targets = []
		self.num_cols = num_cols
		self.num_rows = num_rows
	'''게임 요소 추가'''
	def addElement(self, elem_type, col, row):
		if elem_type == 'wall':
			self.walls.append(elementSprite('wall.png', col, row))
		elif elem_type == 'box':
			self.boxes.append(elementSprite('box.png', col, row))
		elif elem_type == 'target':
			self.targets.append(elementSprite('target.png', col, row))
	'''게임 지도 그리기'''
	def draw(self, screen):
		for elem in self.elemsIter():
			elem.draw(screen)
	'''게임 원소 디지타이저'''
	def elemsIter(self):
		for elem in chain(self.targets, self.walls, self.boxes):
			yield elem
	'''모든 상자가 지정된 위치에 있는지의 여부 판단'''
	def levelCompleted(self):
		for box in self.boxes:
			is_match = False
			for target in self.targets:
				if box.col == target.col and box.row == target.row:
					is_match = True
					break
			if not is_match:
				return False
		return True
	'''어느 위치에 도달할 수 있는지 여부'''
	def isValidPos(self, col, row):
		if col >= 0 and row >= 0 and col < self.num_cols and row < self.num_rows:
			block_size = Config.get('block_size')
			temp1 = self.walls + self.boxes
			temp2 = pygame.Rect(col * block_size, row * block_size, block_size, block_size)
			return temp2.collidelist(temp1) == -1
		else:
			return False
	'''어떤 위치를 획득한 box'''
	def getBox(self, col, row):
		for box in self.boxes:
			if box.col == col and box.row == row:
				return box
		return None
	

	

'''
Function:
	게임 인터페이스
'''
class gameInterface():
	def __init__(self, screen):
		self.screen = screen
		self.levels_path = Config.get('levels_path')
		self.initGame()
	'''관문 지도 가져오기'''
	def loadLevel(self, game_level):
		with open(os.path.join(self.levels_path, game_level), 'r') as f:
			lines = f.readlines()
		# 게임 지도
		self.game_map = gameMap(max([len(line) for line in lines]) - 1, len(lines))
		# 게임 surface
		height = Config.get('block_size') * self.game_map.num_rows
		width = Config.get('block_size') * self.game_map.num_cols
		self.game_surface = pygame.Surface((width, height))
		self.game_surface.fill(Config.get('bg_color'))
		self.game_surface_blank = self.game_surface.copy()
		for row, elems in enumerate(lines):
			for col, elem in enumerate(elems):
				if elem == 'p':
					self.player = pusherSprite(col, row)
				elif elem == '*':
					self.game_map.addElement('wall', col, row)
				elif elem == '#':
					self.game_map.addElement('box', col, row)
				elif elem == 'o':
					self.game_map.addElement('target', col, row)
	'''게임 초기화'''
	def initGame(self):
		self.scroll_x = 0
		self.scroll_y = 0
	'''게임의 경계를 그려내다'''
	def draw(self, *elems):
		self.scroll()
		self.game_surface.blit(self.game_surface_blank, dest=(0, 0))
		for elem in elems:
			elem.draw(self.game_surface)
		self.screen.blit(self.game_surface, dest=(self.scroll_x, self.scroll_y))
	'''게임 계면 면적 > 게임 창구 계면 때문에 인물 위치에 따른 스크롤이 필요'''
	def scroll(self):
		x, y = self.player.rect.center
		width = self.game_surface.get_rect().w
		height = self.game_surface.get_rect().h
		if (x + Config.get('WIDTH') // 2) > Config.get('WIDTH'):
			if -1 * self.scroll_x + Config.get('WIDTH') < width:
				self.scroll_x -= 2
		elif (x + Config.get('WIDTH') // 2) > 0:
			if self.scroll_x < 0:
				self.scroll_x += 2
		if (y + Config.get('HEIGHT') // 2) > Config.get('HEIGHT'):
			if -1 * self.scroll_y + Config.get('HEIGHT') < height:
				self.scroll_y -= 2
		elif (y + 250) > 0:
			if self.scroll_y < 0:
				self.scroll_y += 2
	

	

'''
Function:
	어느 관문의 게임 마스터 사이클
'''
def runGame(screen, game_level):
	clock = pygame.time.Clock()
	game_interface = gameInterface(screen)
	game_interface.loadLevel(game_level)
	font_path = os.path.join(Config.get('resources_path'), Config.get('fontfolder'), 'simkai.ttf')
	text = 'R키를 눌러 이 게이트웨이를 다시 시작'
	font = pygame.font.Font(font_path, 15)
	text_render = font.render(text, 1, (255, 255, 255))
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quitGame()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					next_pos = game_interface.player.move('left', is_test=True)
					if game_interface.game_map.isValidPos(*next_pos):
					game_interface.player.move('left')
					else:
						box = game_interface.game_map.getBox(*next_pos)
						if box:
							next_pos = box.move('left', is_test=True)
							if game_interface.game_map.isValidPos(*next_pos):
								game_interface.player.move('left')
								box.move('left')
					break
				if event.key == pygame.K_RIGHT:
					next_pos = game_interface.player.move('right', is_test=True)
					if game_interface.game_map.isValidPos(*next_pos):
						game_interface.player.move('right')
					else:
						box = game_interface.game_map.getBox(*next_pos)
						if box:
							next_pos = box.move('right', is_test=True)
							if game_interface.game_map.isValidPos(*next_pos):
								game_interface.player.move('right')
								box.move('right')
					break
				if event.key == pygame.K_DOWN:
					next_pos = game_interface.player.move('down', is_test=True)
					if game_interface.game_map.isValidPos(*next_pos):
						game_interface.player.move('down')
					else:
						box = game_interface.game_map.getBox(*next_pos)
						if box:
							next_pos = box.move('down', is_test=True)
							if game_interface.game_map.isValidPos(*next_pos):
								game_interface.player.move('down')
								box.move('down')
					break
				if event.key == pygame.K_UP:
					next_pos = game_interface.player.move('up', is_test=True)
					if game_interface.game_map.isValidPos(*next_pos):
						game_interface.player.move('up')
					else:
						box = game_interface.game_map.getBox(*next_pos)
						if box:
							next_pos = box.move('up', is_test=True)
							if game_interface.game_map.isValidPos(*next_pos):
								game_interface.player.move('up')
								box.move('up')
					break
				if event.key == pygame.K_r:
					game_interface.initGame()
					game_interface.loadLevel(game_level)
		game_interface.draw(game_interface.player, game_interface.game_map)
		if game_interface.game_map.levelCompleted():
		return
		screen.blit(text_render, (5, 5))
		pygame.display.flip()
		clock.tick(100)
	

	

# 정의 버튼
def BUTTON(screen, position, text):
	bwidth = 310
	bheight = 65
	left, top = position
	pygame.draw.line(screen, (150, 150, 150), (left, top), (left+bwidth, top), 5)
	pygame.draw.line(screen, (150, 150, 150), (left, top-2), (left, top+bheight), 5)
	pygame.draw.line(screen, (50, 50, 50), (left, top+bheight), (left+bwidth, top+bheight), 5)
	pygame.draw.line(screen, (50, 50, 50), (left+bwidth, top+bheight), [left+bwidth, top], 5)
	pygame.draw.rect(screen, (100, 100, 100), (left, top, bwidth, bheight))
	font_path = os.path.join(Config.get('resources_path'), Config.get('fontfolder'), 'simkai.ttf')
	font = pygame.font.Font(font_path, 50)
	text_render = font.render(text, 1, (255, 0, 0))
	return screen.blit(text_render, (left+50, top+10))
	
	

# 시작 계면
def startInterface(screen):
	screen.fill(Config.get('bg_color'))
	clock = pygame.time.Clock()
	while True:
		button_1 = BUTTON(screen, (95, 150), '게임 시작')
		button_2 = BUTTON(screen, (95, 305), '게임 종료')
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if button_1.collidepoint(pygame.mouse.get_pos()):
					return
				elif button_2.collidepoint(pygame.mouse.get_pos()):
					quitGame()
		clock.tick(60)
		pygame.display.update()
	

	

# 스크린 변환
def switchInterface(screen):
	screen.fill(Config.get('bg_color'))
	clock = pygame.time.Clock()
	while True:
		button_1 = BUTTON(screen, (95, 150), '처음부터 다시 시작')
		button_2 = BUTTON(screen, (95, 305), '게임 종료')
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if button_1.collidepoint(pygame.mouse.get_pos()):
					return
				elif button_2.collidepoint(pygame.mouse.get_pos()):
					quitGame()
		clock.tick(60)
		pygame.display.update()
	

	

# 계면 끝내기
def endInterface(screen):
	screen.fill(Config.get('bg_color'))
	clock = pygame.time.Clock()
	font_path = os.path.join(Config.get('resources_path'), Config.get('fontfolder'), 'simkai.ttf')
	text = '잘했습니다~ 통과를 축하해요!'
	font = pygame.font.Font(font_path, 30)
	text_render = font.render(text, 1, (255, 255, 255))
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		screen.blit(text_render, (120, 200))
		clock.tick(60)
		pygame.display.update()
	

	

'''
Function:
	메인 함수
'''
def main():
	pygame.init()
	pygame.mixer.init()
	pygame.display.set_caption('상자 밀기 - 닉네임: Charles의 피카츄')
	screen = pygame.display.set_mode([Config.get('WIDTH'), Config.get('HEIGHT')])
	pygame.mixer.init()
	audio_path = os.path.join(Config.get('resources_path'), Config.get('audiofolder'), 'EineLiebe.mp3')
	pygame.mixer.music.load(audio_path)
	pygame.mixer.music.set_volume(0.4)
	pygame.mixer.music.play(-1)
	startInterface(screen)
	levels_path = Config.get('levels_path')
	for level_name in sorted(os.listdir(levels_path)):
		runGame(screen, level_name)
		switchInterface(screen)
	endInterface(screen)
	

	

if __name__ == '__main__':
	main()

