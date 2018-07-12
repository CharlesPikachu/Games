# coding: utf-8
# 公众号: Charles的皮卡丘
# 作者: Charles
# 滑雪小游戏
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
	# 改变滑雪者的朝向
	# 负数为向左，正数为向右，0为向前
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
	# 移动滑雪者
	def move(self):
		self.rect.centerx += self.speed[0]
		self.rect.centerx = max(20, self.rect.centerx)
		self.rect.centerx = min(620, self.rect.centerx)


# 障碍物类
# Input:
# 	-img_path: 障碍物图片路径
# 	-location: 障碍物位置
# 	-attribute: 障碍物类别属性
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
	# 移动
	def move(self, num):
		self.rect.centery = self.location[1] - num


# 创建障碍物
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


# 合并障碍物
def AddObstacles(obstacles0, obstacles1):
	obstacles = pygame.sprite.Group()
	for obstacle in obstacles0:
		obstacles.add(obstacle)
	for obstacle in obstacles1:
		obstacles.add(obstacle)
	return obstacles


# 显示游戏开始界面
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


# 主程序
def main():
	'''
	初始化
	'''
	pygame.init()
	# 声音
	pygame.mixer.init()
	pygame.mixer.music.load("./music/bg_music.mp3")
	pygame.mixer.music.set_volume(0.4)
	pygame.mixer.music.play(-1)
	# 屏幕
	screen = pygame.display.set_mode([640, 640])
	pygame.display.set_caption('滑雪游戏-公众号:Charles的皮卡丘')
	# 主频
	clock = pygame.time.Clock()
	# 滑雪者
	skier = SkierClass()
	# 记录滑雪的距离
	distance = 0
	# 创建障碍物
	obstacles0 = create_obstacles(20, 29)
	obstacles1 = create_obstacles(10, 19)
	obstaclesflag = 0
	obstacles = AddObstacles(obstacles0, obstacles1)
	# 分数
	font = pygame.font.Font(None, 50)
	score = 0
	score_text = font.render("Score: "+str(score), 1, (0, 0, 0))
	# 速度
	speed = [0, 6]
	Show_Start_Interface(screen, 640, 640)
	'''
	主循环
	'''
	# 更新屏幕
	def update():
		screen.fill([255, 255, 255])
		pygame.display.update(obstacles.draw(screen))
		screen.blit(skier.person, skier.rect)
		screen.blit(score_text, [10, 10])
		pygame.display.flip()
	while True:
		# 左右键控制人物方向
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
		# 用于碰撞检测
		for obstacle in obstacles:
			obstacle.move(distance)
		# 碰撞检测
		is_hit = pygame.sprite.spritecollide(skier, obstacles, False)
		if is_hit:
			if is_hit[0].attribute == "tree" and not is_hit[0].passed:
				score -= 50
				skier.person = pygame.image.load("./images/skier_fall.png")
				update()
				# 摔倒后暂停一会再站起来
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