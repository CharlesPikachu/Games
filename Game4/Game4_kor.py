# coding: utf-8
# 공공 번호: Charles's Pikachu
# 저자: Charles
# 스키 게임
import sys
import pygame
import random
from pygame.locals import *


# 滑雪者类
class SkierClass(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		# 滑雪者的朝向(-2到2)
		self.direction = 0
		self.imgs = ["./images/skier_forward.png", "./images/skier_right1.png", "./images/skier_right2.png", "./images/skier_left2.png", "./images/skier_left1.png"]
		self.person = pygame.image.load(self.imgs[self.direction])
		self.rect = self.person.get_rect()
		self.rect.center = [320, 100]
		self.speed = [self.direction, 6-abs(self.direction)*2]
	# 스키의 방향을 바꾸기
	# 음수는 왼쪽으로, 정수는 오른쪽으로, 0은 앞으로
	def turn(self, num):
		self.direction += num
		self.direction = max(-2, self.direction)
		self.direction = min(2, self.direction)
		center = self.rect.center
		self.person = pygame.image.load(self.imgs[self.direction])
		self.rect = self.person.get_rect()
		self.rect.center = center
		self.speed = [self.direction, 6-abs(self.direction)*2]
		return self.speed
	# 스키 이동
	def move(self):
		self.rect.centerx += self.speed[0]
		self.rect.centerx = max(20, self.rect.centerx)
		self.rect.centerx = min(620, self.rect.centerx)


# 장애물 종류
# Input:
# 	-img_path: 장애물 이미지 경로
# 	-location: 장애물 위치
# 	-attribute: 장애물 카테고리 속성
class ObstacleClass(pygame.sprite.Sprite):
	def __init__(self, img_path, location, attribute):
		pygame.sprite.Sprite.__init__(self)
		self.img_path = img_path
		self.image = pygame.image.load(self.img_path)
		self.location = location
		self.rect = self.image.get_rect()
		self.rect.center = self.location
		self.attribute = attribute
		self.passed = False
	# 이동
	def move(self, num):
		self.rect.centery = self.location[1] - num


# 장애물 만들기
def create_obstacles(s, e, num=10):
	obstacles = pygame.sprite.Group()
	locations = []
	for i in range(num):
		row = random.randint(s, e)
		col = random.randint(0, 9)
		location  = [col*64+20, row*64+20]
		if location not in locations:
			locations.append(location)
			attribute = random.choice(["tree", "flag"])
			img_path = './images/tree.png' if attribute=="tree" else './images/flag.png'
			obstacle = ObstacleClass(img_path, location, attribute)
			obstacles.add(obstacle)
	return obstacles


# 장애물 통합
def AddObstacles(obstacles0, obstacles1):
	obstacles = pygame.sprite.Group()
	for obstacle in obstacles0:
		obstacles.add(obstacle)
	for obstacle in obstacles1:
		obstacles.add(obstacle)
	return obstacles


# 게임 시작 인터페이스 표시
def Show_Start_Interface(Demo, width, height):
	Demo.fill((255, 255, 255))
	tfont = pygame.font.Font('./font/simkai.ttf', width//4)
	cfont = pygame.font.Font('./font/simkai.ttf', width//20)
	title = tfont.render(u'滑雪游戏', True, (255, 0, 0))
	content = cfont.render(u'按任意键开始游戏', True, (0, 0, 255))
	trect = title.get_rect()
	trect.midtop = (width/2, height/10)
	crect = content.get_rect()
	crect.midtop = (width/2, height/2.2)
	Demo.blit(title, trect)
	Demo.blit(content, crect)
	pygame.display.update()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				return


# 메인 프로그램
def main():
	'''
	초기화
	'''
	pygame.init()
	# 소리
	pygame.mixer.init()
	pygame.mixer.music.load("./music/bg_music.mp3")
	pygame.mixer.music.set_volume(0.4)
	pygame.mixer.music.play(-1)
	# 화면
	screen = pygame.display.set_mode([640, 640])
	pygame.display.set_caption('滑雪游戏-公众号:Charles的皮卡丘')
	# 主频
	clock = pygame.time.Clock()
	# 스키
	skier = SkierClass()
	# 스키 거리 기록
	distance = 0
	# 장애물 만들기
	obstacles0 = create_obstacles(20, 29)
	obstacles1 = create_obstacles(10, 19)
	obstaclesflag = 0
	obstacles = AddObstacles(obstacles0, obstacles1)
	# 分数
	font = pygame.font.Font(None, 50)
	score = 0
	score_text = font.render("Score: "+str(score), 1, (0, 0, 0))
	# 속도
	speed = [0, 6]
	Show_Start_Interface(screen, 640, 640)
	'''
	主循环
	'''
	# 화면 업데이트
	def update():
		screen.fill([255, 255, 255])
		pygame.display.update(obstacles.draw(screen))
		screen.blit(skier.person, skier.rect)
		screen.blit(score_text, [10, 10])
		pygame.display.flip()
	while True:
		# 좌우 버튼은 플레이어의 방향을 제어한다
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT or event.key == pygame.K_a:
					speed = skier.turn(-1)
				elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					speed = skier.turn(1)
		skier.move()
		distance += speed[1]
		if distance >= 640 and obstaclesflag == 0:
			obstaclesflag = 1
			obstacles0 = create_obstacles(20, 29)
			obstacles = AddObstacles(obstacles0, obstacles1)
		if distance >= 1280 and obstaclesflag == 1:
			obstaclesflag = 0
			distance -= 1280
			for obstacle in obstacles0:
				obstacle.location[1] = obstacle.location[1] - 1280
			obstacles1 = create_obstacles(10, 19)
			obstacles = AddObstacles(obstacles0, obstacles1)
		# 충돌 감지에 사용
		for obstacle in obstacles:
			obstacle.move(distance)
		#충돌 검사
		is_hit = pygame.sprite.spritecollide(skier, obstacles, False)
		if is_hit:
			if is_hit[0].attribute == "tree" and not is_hit[0].passed:
				score -= 50
				skier.person = pygame.image.load("./images/skier_fall.png")
				update()
				# 넘어진 후 잠시 멈추었다가 다시 일어서기
				pygame.time.delay(1000)
				skier.person = pygame.image.load("./images/skier_forward.png")
				skier.direction = 0
				speed = [0, 6]
				is_hit[0].passed = True
			elif is_hit[0].attribute == "flag" and not is_hit[0].passed:
				score += 10
				obstacles.remove(is_hit[0])
		score_text = font.render("Score: "+str(score), 1, (0, 0, 0))
		update()
		clock.tick(40)


if __name__ == '__main__':
	main()