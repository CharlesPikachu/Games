# 게임 진행 중 인터페이스

# 저자: Charles

# 공개 번호 : Charles 's Pikachu

import sys

import json

import math

import random

import pygame

sys.path.append('..')

from sprites import Enemy

from sprites import Turret

from interface import PAUSE

from pygame.locals import *

from collections import namedtuple





# 버튼 클래스 : 위치, 텍스트, 클릭 이벤트 발생

Button = namedtuple('Button', ['rect', 'text', 'onClick'])

# 일부 색상 정의

info_color = (120, 20, 50)

red = (255, 0, 0)

green = (0, 255, 0)

black = (0, 0, 0)

white = (255, 255, 255)

grey = (127, 127, 127)

button_color1 = (0, 200, 0)

button_color2 = (0, 100, 0)





# 게임 진행 중 인터페이스

class GAMING():

	def __init__(self, WIDTH=800, HEIGHT=600):

		self.WIDTH = WIDTH

		self.HEIGHT = HEIGHT

		# 게임지도 크기

		map_w = WIDTH

		map_h = 500

		# 버튼 크기 및 위치

		button_w = 60

		button_h = 60

		button_y = 520

		# 간극

		gap = 20

		# 단추는 도구 모음에 있으며 도구 모음의 양쪽 끝에 메시지 표시 상자가 있습니다.

		toolbar_w = gap * 7 + button_w * 6

		info_w = (WIDTH - toolbar_w) // 2

		info_h = HEIGHT - map_h

		toolbar_h = HEIGHT - map_h

		# 인터페이스 레이아웃

		self.map_rect = pygame.Rect(0, 0, map_w, map_h)

		self.map_surface = pygame.Surface((map_w, map_h))

		self.leftinfo_rect = pygame.Rect(0, map_h, info_w, info_h)

		self.rightinfo_rect = pygame.Rect(WIDTH-info_w, map_h, info_w, info_h)

		self.toolbar_rect = pygame.Rect(info_w, map_h, toolbar_w, toolbar_h)

		# 풀

		self.grass = pygame.image.load("./resource/imgs/game/grass.png")

		# 바위 (포장용)

		self.rock = pygame.image.load("./resource/imgs/game/rock.png")

		# 흙

		self.dirt = pygame.image.load("./resource/imgs/game/dirt.png")

		# 물

		self.water = pygame.image.load("./resource/imgs/game/water.png")

		# 관목

		self.bush = pygame.image.load("./resource/imgs/game/bush.png")

		# 넥타이

		self.nexus = pygame.image.load("./resource/imgs/game/nexus.png")

		# 동굴

		self.cave = pygame.image.load("./resource/imgs/game/cave.png")

		# 지도 요소의 크기를 확인하려면 라이브러리의지도를 구성하는지도의 크기가 동일한 지 확인

		self.elementSize = int(self.grass.get_rect().width)

		# 일부 글꼴

		self.info_font = pygame.font.Font('./resource/fonts/Calibri.ttf', 14)

		self.button_font = pygame.font.Font('./resource/fonts/Calibri.ttf', 20)

		# 포탑을 쏠 수 있는 곳

		self.placeable = {0: self.grass}

		# 지도 요소 사전 (숫자는 .map 파일의 숫자와 일치 함)

		self.map_elements = {

								0: self.grass,

								1: self.rock,

								2: self.dirt,

								3: self.water,

								4: self.bush,

								5: self.nexus,

								6: self.cave

							}

		# 지도에 도로를 기록하는 데 사용

		self.path_list = []

		# 현재지도,지도 가져 오기

		self.currentMap = dict()

		# 현재 마우스가 가지고있는 아이콘 (예 : 선택한 항목) -> [소품 이름, 소품]

		self.mouseCarried = []

		# 지도에 포대 건설

		self.builtTurretGroup = pygame.sprite.Group()

		# 모든 적

		self.EnemiesGroup = pygame.sprite.Group()

		# 모든 방향키

		self.arrowsGroup = pygame.sprite.Group()

		# 플레이어 작동 버튼

		self.buttons = [

							Button(pygame.Rect((info_w+gap), button_y, button_w, button_h), 'T1', self.takeT1),

							Button(pygame.Rect((info_w+gap*2+button_w), button_y, button_w, button_h), 'T2', self.takeT2),

							Button(pygame.Rect((info_w+gap*3+button_w*2), button_y, button_w, button_h), 'T3', self.takeT3),

							Button(pygame.Rect((info_w+gap*4+button_w*3), button_y, button_w, button_h), 'XXX', self.takeXXX),

							Button(pygame.Rect((info_w+gap*5+button_w*4), button_y, button_w, button_h), 'Pause', self.pauseGame),

							Button(pygame.Rect((info_w+gap*6+button_w*5), button_y, button_w, button_h), 'Quit', self.quitGame)

						]

	# 게임 시작

	def start(self, screen, map_path=None, difficulty_path=None):

		# 게임의 어려움에 해당하는 매개 변수를 읽음

		with open(difficulty_path, 'r') as f:

			difficulty_dict = json.load(f)

		self.money = difficulty_dict.get('money')

		self.health = difficulty_dict.get('health')

		self.max_health = difficulty_dict.get('health')

		difficulty_dict = difficulty_dict.get('enemy')

		# 적의 물결을 60 초마다 생성

		GenEnemiesEvent = pygame.constants.USEREVENT + 0

		pygame.time.set_timer(GenEnemiesEvent, 60000)

		# 적의 깃발과 현재 생성 된 적의 총 개수 생성

		genEnemiesFlag = False

		genEnemiesNum = 0

		# 0.5초마다 적이 하나 나온다

		GenEnemyEvent = pygame.constants.USEREVENT + 1

		pygame.time.set_timer(GenEnemyEvent, 500)

		genEnemyFlag = False

		# 변수 정의 방지

		enemyRange = None

		numEnemy = None

		# 타워 촬영을 수동으로 조작할지 여부

		Manualshot = False

		has_control = False

		while True:

			if self.health <= 0:

				return

			for event in pygame.event.get():

				if event.type == pygame.QUIT:

					pygame.quit()

					sys.exit()

				if event.type == pygame.MOUSEBUTTONUP:

					# 항목을 선택하려면 왼쪽 버튼을 클릭

					if event.button == 1:

						# 鼠标点击在地图上

						if self.map_rect.collidepoint(event.pos):

							if self.mouseCarried:

								if self.mouseCarried[0] == 'turret':

									self.buildTurret(event.pos)

								elif self.mouseCarried[0] == 'XXX':

									self.sellTurret(event.pos)

						# 도구 모음에서 마우스를 클릭

						elif self.toolbar_rect.collidepoint(event.pos):

							for button in self.buttons:

								if button.rect.collidepoint(event.pos):

									if button.text == 'T1':

										button.onClick()

									elif button.text == 'T2':

										button.onClick()

									elif button.text == 'T3':

										button.onClick()

									elif button.text == 'XXX':

										button.onClick()

									elif button.text == 'Pause':

										button.onClick(screen)

									elif button.text == 'Quit':

										button.onClick()

									# 단 하나의 버튼 만 클릭

									break

					# 마우스 오른쪽 버튼으로 릴리스 항목 내보내기

					if event.button == 3:

						self.mouseCarried = []

					# 가운데 버튼을 눌러 포탑 활 쏘기 방향을 수동으로 한 번 제어하고, 그렇지 않으면 자유 활 쏘기

					if event.button == 2:

						Manualshot = True

				if event.type == GenEnemiesEvent:

					genEnemiesFlag = True

				if event.type == GenEnemyEvent:

					genEnemyFlag = True

			# 적을 생성

			# 생성된 적은 현재 이미 생성된 적의 총 횟수의 증가에 따라 강해지며 많아진다

			if genEnemiesFlag:

				genEnemiesFlag = False

				genEnemiesNum += 1

				idx = 0

				for key, value in difficulty_dict.items():

					idx += 1

					if idx == len(difficulty_dict.keys()):

						enemyRange = value['enemyRange']

						numEnemy = value['numEnemy']

						break

					if genEnemiesNum <= int(key):

						enemyRange = value['enemyRange']

						numEnemy = value['numEnemy']

						break

			if genEnemyFlag and numEnemy:

				genEnemyFlag = False

				numEnemy -= 1

				enemy = Enemy.Enemy(random.choice(range(enemyRange)))

				self.EnemiesGroup.add(enemy)

			# 양궁

			for turret in self.builtTurretGroup:

				if not Manualshot:

					position = turret.position[0] + self.elementSize // 2, turret.position[1]

					arrow = turret.shot(position)

				else:

					position = turret.position[0] + self.elementSize // 2, turret.position[1]

					mouse_pos = pygame.mouse.get_pos()

					angle = math.atan((mouse_pos[1]-position[1])/(mouse_pos[0]-position[0]+1e-6))

					arrow = turret.shot(position, angle)

					has_control = True

				if arrow:

					self.arrowsGroup.add(arrow)

				else:

					has_control = False

			if has_control:

				has_control = False

				Manualshot = False

			# 이동 화살표 및 충돌 감지

			for arrow in self.arrowsGroup:

				arrow.move()

				points = [(arrow.rect.left, arrow.rect.top), (arrow.rect.left, arrow.rect.bottom), (arrow.rect.right, arrow.rect.top), (arrow.rect.right, arrow.rect.bottom)]

				if (not self.map_rect.collidepoint(points[0])) and (not self.map_rect.collidepoint(points[1])) and \

					(not self.map_rect.collidepoint(points[2])) and (not self.map_rect.collidepoint(points[3])):

					self.arrowsGroup.remove(arrow)

					del arrow

					continue

				for enemy in self.EnemiesGroup:

					if pygame.sprite.collide_rect(arrow, enemy):

						enemy.life_value -= arrow.attack_power

						self.arrowsGroup.remove(arrow)

						del arrow

						break

			self.draw(screen, map_path)

	# 장면을 게임 인터페이스에 그립니다.

	def draw(self, screen, map_path):

		self.drawToolbar(screen)

		self.loadMap(screen, map_path)

		self.drawMouseCarried(screen)

		self.drawBuiltTurret(screen)

		self.drawEnemies(screen)

		self.drawArrows(screen)

		pygame.display.flip()

	# 총알을 그립니다.

	def drawArrows(self, screen):

		for arrow in self.arrowsGroup:

			screen.blit(arrow.image, arrow.rect)

	# 적을 그리다

	def drawEnemies(self, screen):

		for enemy in self.EnemiesGroup:

			if enemy.life_value <= 0:

				self.money += enemy.reward

				self.EnemiesGroup.remove(enemy)

				del enemy

				continue

			res = enemy.move(self.elementSize)

			if res:

				coord = self.find_next_path(enemy)

				if coord:

					enemy.reached_path.append(enemy.coord)

					enemy.coord = coord

					enemy.position = self.coord2pos(coord)

					enemy.rect.left, enemy.rect.top = enemy.position

				else:

					self.health -= enemy.damage

					self.EnemiesGroup.remove(enemy)

					del enemy

					continue

			# 혈액 스트립 그리기

			greenLen = max(0, enemy.life_value / enemy.max_life_value) * self.elementSize

			if greenLen > 0:

				pygame.draw.line(screen, green, (enemy.position), (enemy.position[0]+greenLen, enemy.position[1]), 1)

			if greenLen < self.elementSize:

				pygame.draw.line(screen, red, (enemy.position[0]+greenLen, enemy.position[1]), (enemy.position[0]+self.elementSize, enemy.position[1]), 1)

			screen.blit(enemy.image, enemy.rect)

	# 터렛을 그립니다.

	def drawBuiltTurret(self, screen):

		for turret in self.builtTurretGroup:

			screen.blit(turret.image, turret.rect)

	# 마우스가 가져온 것 그리기

	def drawMouseCarried(self, screen):

		if self.mouseCarried:

			position = pygame.mouse.get_pos()

			coord = self.pos2coord(position)

			position = self.coord2pos(coord)

			# 지도에 그리기

			if self.map_rect.collidepoint(position):

				if self.mouseCarried[0] == 'turret':

					screen.blit(self.mouseCarried[1].image, position)

					self.mouseCarried[1].coord = coord

					self.mouseCarried[1].position = position

					self.mouseCarried[1].rect.left, self.mouseCarried[1].rect.top = position

				else:

					screen.blit(self.mouseCarried[1], position)

	# 페인트 도구 모음

	def drawToolbar(self, screen):

		# 정보 표시 상자

		# 	왼쪽

		pygame.draw.rect(screen, info_color, self.leftinfo_rect)

		leftTitle = self.info_font.render('Player info:', True, white)

		moneyInfo = self.info_font.render('Money: ' + str(self.money), True, white)

		healthInfo = self.info_font.render('Health: ' + str(self.health), True, white)

		screen.blit(leftTitle, (self.leftinfo_rect.left+5, self.leftinfo_rect.top+5))

		screen.blit(moneyInfo, (self.leftinfo_rect.left+5, self.leftinfo_rect.top+35))

		screen.blit(healthInfo, (self.leftinfo_rect.left+5, self.leftinfo_rect.top+55))

		# 	오른쪽

		pygame.draw.rect(screen, info_color, self.rightinfo_rect)

		rightTitle = self.info_font.render('Selected info:', True, white)

		screen.blit(rightTitle, (self.rightinfo_rect.left+5, self.rightinfo_rect.top+5))

		# 중간 부분

		pygame.draw.rect(screen, grey, self.toolbar_rect)

		for button in self.buttons:

			mouse_pos = pygame.mouse.get_pos()

			if button.rect.collidepoint(mouse_pos):

				self.showSelectedInfo(screen, button)

				button_color = button_color1

			else:

				button_color = button_color2

			pygame.draw.rect(screen, button_color, button.rect)

			buttonText = self.button_font.render(button.text, True, white)

			buttonText_rect = buttonText.get_rect()

			buttonText_rect.center = (button.rect.centerx, button.rect.centery)

			screen.blit(buttonText, buttonText_rect)

	# 마우스로 선택한 버튼의 동작 정보를 표시

	def showSelectedInfo(self, screen, button):

		if button.text == 'T1':

			T1 = Turret.Turret(0)

			selectedInfo1 = self.info_font.render('Cost: '+str(T1.price), True, white)

			selectedInfo2 = self.info_font.render('Damage: '+str(T1.arrow.attack_power), True, white)

			selectedInfo3 = self.info_font.render('Affordable: '+str(self.money>=T1.price), True, white)

			screen.blit(selectedInfo1, (self.rightinfo_rect.left+5, self.rightinfo_rect.top+35))

			screen.blit(selectedInfo2, (self.rightinfo_rect.left+5, self.rightinfo_rect.top+55))

			screen.blit(selectedInfo3, (self.rightinfo_rect.left+5, self.rightinfo_rect.top+75))

		elif button.text == 'T2':

			T2 = Turret.Turret(1)

			selectedInfo1 = self.info_font.render('Cost: '+str(T2.price), True, white)

			selectedInfo2 = self.info_font.render('Damage: '+str(T2.arrow.attack_power), True, white)

			selectedInfo3 = self.info_font.render('Affordable: '+str(self.money>=T2.price), True, white)

			screen.blit(selectedInfo1, (self.rightinfo_rect.left+5, self.rightinfo_rect.top+35))

			screen.blit(selectedInfo2, (self.rightinfo_rect.left+5, self.rightinfo_rect.top+55))

			screen.blit(selectedInfo3, (self.rightinfo_rect.left+5, self.rightinfo_rect.top+75))

		elif button.text == 'T3':

			T3 = Turret.Turret(2)

			selectedInfo1 = self.info_font.render('Cost: '+str(T3.price), True, white)

			selectedInfo2 = self.info_font.render('Damage: '+str(T3.arrow.attack_power), True, white)

			selectedInfo3 = self.info_font.render('Affordable: '+str(self.money>=T3.price), True, white)

			screen.blit(selectedInfo1, (self.rightinfo_rect.left+5, self.rightinfo_rect.top+35))

			screen.blit(selectedInfo2, (self.rightinfo_rect.left+5, self.rightinfo_rect.top+55))

			screen.blit(selectedInfo3, (self.rightinfo_rect.left+5, self.rightinfo_rect.top+75))

		elif button.text == 'XXX':

			selectedInfo = self.info_font.render('Sell a turret', True, white)

			screen.blit(selectedInfo, (self.rightinfo_rect.left+5, self.rightinfo_rect.top+35))

		elif button.text == 'Pause':

			selectedInfo = self.info_font.render('Pause game', True, white)

			screen.blit(selectedInfo, (self.rightinfo_rect.left+5, self.rightinfo_rect.top+35))

		elif button.text == 'Quit':

			selectedInfo = self.info_font.render('Quit game', True, white)

			screen.blit(selectedInfo, (self.rightinfo_rect.left+5, self.rightinfo_rect.top+35))

	# 판매 포탑 (절반 가격)


	def sellTurret(self, position):

		coord = self.pos2coord(position)

		for turret in self.builtTurretGroup:

			if coord == turret.coord:

				self.builtTurretGroup.remove(turret)

				self.money += int(turret.price * 0.5)

				del turret

				break

	# 터렛 만들기

	def buildTurret(self, position):

		turret = self.mouseCarried[1]

		coord = self.pos2coord(position)

		position = self.coord2pos(coord)

		turret.position = position

		turret.coord = coord

		turret.rect.left, turret.rect.top = position

		if self.money - turret.price >= 0:

			if self.currentMap.get(turret.coord) in self.placeable.keys():

				self.money -= turret.price

				self.builtTurretGroup.add(turret)

				if self.mouseCarried[1].turret_type == 0:

					self.mouseCarried = []

					self.takeT1()

				elif self.mouseCarried[1].turret_type == 1:

					self.mouseCarried = []

					self.takeT2()

				elif self.mouseCarried[1].turret_type == 2:

					self.mouseCarried = []

					self.takeT3()

	# 포탑 1 가져 가라.

	def takeT1(self):

		T1 = Turret.Turret(0)

		if self.money >= T1.price:

			self.mouseCarried = ['turret', T1]

	# 포탑 2 가져 가라

	def takeT2(self):

		T2 = Turret.Turret(1)

		if self.money >= T2.price:

			self.mouseCarried = ['turret', T2]

	# 포탑 3 가져 가라

	def takeT3(self):

		T3 = Turret.Turret(2)

		if self.money >= T3.price:

			self.mouseCarried = ['turret', T3]

	# 터렛 판매

	def takeXXX(self):

		XXX = pygame.image.load('./resource/imgs/game/x.png')

		self.mouseCarried = ['XXX', XXX]

	# 다음 경로 단위 찾기

	def find_next_path(self, enemy):

		x, y = enemy.coord

		# 우선 순위 : 오른쪽 아래 왼쪽 위

		neighbours = [(x, y+1), (x+1, y), (x-1, y), (x, y-1)]

		for neighbour in neighbours:

			if (neighbour in self.path_list) and (neighbour not in enemy.reached_path):

				return neighbour

		return None

	# 지도 좌표를 실제 좌표로 변환합니다. 20 단위 길이의 실제 좌표 =지도 좌표

	def pos2coord(self, position):

		return (position[0]//self.elementSize, position[1]//self.elementSize)

	# 지도 좌표를 실제 좌표로 변환합니다. 20 단위 길이의 실제 좌표 =지도 좌표

	def coord2pos(self, coord):

		return (coord[0]*self.elementSize, coord[1]*self.elementSize)

	# 지도 가져 오기

	def loadMap(self, screen, map_path):

		map_file = open(map_path, 'r')

		idx_j = -1

		for line in map_file.readlines():

			line = line.strip()

			if not line:

				continue

			idx_j += 1

			idx_i = -1

			for col in line:

				try:

					element_type = int(col)

					element_img = self.map_elements.get(element_type)

					element_rect = element_img.get_rect()

					idx_i += 1

					element_rect.left, element_rect.top = self.elementSize * idx_i, self.elementSize * idx_j

					self.map_surface.blit(element_img, element_rect)

					self.currentMap[idx_i, idx_j] = element_type

					# 把道路记下来

					if element_type == 1:

						self.path_list.append((idx_i, idx_j))

				except:

					continue

		# 동굴과베이스 캠프

		self.map_surface.blit(self.cave, (0, 0))

		self.map_surface.blit(self.nexus, (740, 400))

		# 베이스 캠프의 혈액통

		nexus_width = self.nexus.get_rect().width

		greenLen = max(0, self.health / self.max_health) * nexus_width

		if greenLen > 0:

			pygame.draw.line(self.map_surface, green, (740, 400), (740+greenLen, 400), 3)

		if greenLen < nexus_width:

			pygame.draw.line(self.map_surface, red, (740+greenLen, 400), (740+nexus_width, 400), 3)

		screen.blit(self.map_surface, (0, 0))

		map_file.close()

	# 게임 일시 중지

	def pauseGame(self, screen):

		pause_interface = PAUSE.PAUSE(self.WIDTH, self.HEIGHT)

		pause_interface.update(screen)

	# 게임 나가기

	def quitGame(self):

		sys.exit(0)

		pygame.quit()