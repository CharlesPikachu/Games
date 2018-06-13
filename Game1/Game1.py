# coding: utf-8
# 作者: Charles
# 公众号: Charles的皮卡丘
# 导入pygame库，这一步能让你使用库里提供的功能
import pygame
from pygame.locals import *
import math   # 因为需要计算旋转的角度
import random # 因为需要用到随机的功能

# 初始化pygame，设置展示窗口
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
# keys用来记录按键情况：WASD(依次对应)
keys = [False, False, False, False]
# playerpos表示玩家位置
playerpos = [100, 100]
# 跟踪玩家的精度变量，记录了射出的箭头数和被击中的獾的数量。
# 之后我们会用到这些信息用来计算射击精确度。
acc = [0, 0]
# 跟踪箭头变量
arrows = []
# 定义了一个定时器，使得游戏里经过一段时间后就新建一支獾
badtimer = 100
badtimer1 = 0
badguys = [[640, 100]]
healthvalue = 194
# 播放声音初始化
pygame.mixer.init()

# 加载图片
rabbit_img = pygame.image.load("resources/images/dude.png")
# 再加一些风景~
grass_img = pygame.image.load("resources/images/grass.png")
castle_img = pygame.image.load("resources/images/castle.png")
# 加载箭头
arrow_img = pygame.image.load('resources/images/bullet.png')
# 加载獾
badguy_img1 = pygame.image.load("resources/images/badguy.png")
badguy_img = badguy_img1
# 加载城堡健康值图片
healthbar_img = pygame.image.load("resources/images/healthbar.png")
health_img = pygame.image.load("resources/images/health.png")
# 加载胜利与失败图片
gameover_img = pygame.image.load("resources/images/gameover.png")
youwin_img = pygame.image.load("resources/images/youwin.png")
# 加载声音文件并配置音量
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
# 加载游戏的背景音乐并让背景音乐一直不停的播放。
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# 不停地循环执行接下来的部分
# running变量会跟踪游戏是否结束，
# exitcode变量会跟踪玩家是否胜利。
running = True
exitcode = False
while running:
	# 在给屏幕画任何东西之前用黑色进行填充
	screen.fill(0)
	# 添加的风景也需要画在屏幕上
	for x in range(width//grass_img.get_width()+1):
		for y in range(height//grass_img.get_height()+1):
			screen.blit(grass_img, (x*100, y*100))
	screen.blit(castle_img, (0, 30))
	screen.blit(castle_img, (0, 135))
	screen.blit(castle_img, (0, 240))
	screen.blit(castle_img, (0, 345))
	# 首先获取鼠标和玩家的位置。然后，获取通过atan2函数得出的角度和弧度。
	# 当兔子被旋转的时候，它的位置将会改变。
	# 所以你需要计算兔子新的位置，然后将其在屏幕上显示出来。
	position = pygame.mouse.get_pos()
	angle = math.atan2(position[1]-(playerpos[1]+32), position[0]-(playerpos[0]+26))
	playerrot = pygame.transform.rotate(rabbit_img, 360-angle*57.29)
	playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
	screen.blit(playerrot, playerpos1)
	# 在屏幕上画出箭头来
	# vely和velx的值是根据三角定理算出来的。
	# 10是箭头的速度。if表达式是检查箭头是否超出了屏幕范围，
	# 如果超出，就删除这个箭头。
	# 第二个for表达式是循环来把箭头根据相应的旋转画出来。
	for bullet in arrows:
		index = 0
		velx = math.cos(bullet[0])*10
		vely = math.sin(bullet[0])*10
		bullet[1] += velx
		bullet[2] += vely
		if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
			arrows.pop(index)
		index += 1
		for projectile in arrows:
			arrow1 = pygame.transform.rotate(arrow_img, 360-projectile[0]*57.29)
			screen.blit(arrow1, (projectile[1], projectile[2]))
	# 更新并且显示这些坏蛋
	# 检查badtimer是否为0，如果为0，创建一个獾然后重新设置badtimer。
	# 第一个循环更新獾的x坐标，检查獾是否超出屏幕范围，如果超出范围，将獾删掉。
	# 第二个循环是来画出所有的獾。
	if badtimer == 0:
		badguys.append([640, random.randint(50, 430)])
		badtimer = 100 -(badtimer1*2)
		if badtimer1 >= 35:
			badtimer1 = 35
		else:
			badtimer1 += 5
	index_badguy = 0
	for badguy in badguys:
		if badguy[0] < -64:
			badguys.pop(index_badguy)
		badguy[0] -= 7
		# 獾可以炸掉城堡
		# 这段代码相当简单。如果獾的x坐标离左边小于64，
		# 就删除坏蛋并且减少游戏里的健康值，减少的大小为5至20里的一个随机数。
		# 当然獾冲过来并且在碰到城堡的时候会消失
		badrect = pygame.Rect(badguy_img.get_rect())
		badrect.top = badguy[1]
		badrect.left = badguy[0]
		if badrect.left < 64:
			hit.play()
			healthvalue -= random.randint(5, 20)
			badguys.pop(index_badguy)
		# 循环所有的坏蛋和所有的箭头来检查是否有碰撞。
		# 如果碰撞上，删除獾，删除箭头，并且精确度的变量里面加1。
		# 使用了PyGame内建功能来检查两个矩形是否交叉.
		index_arrow = 0
		for bullet in arrows:
			bulletrect = pygame.Rect(arrow_img.get_rect())
			bulletrect.left = bullet[1]
			bulletrect.top = bullet[2]
			if badrect.colliderect(bulletrect):
				enemy.play()
				acc[0] += 1
				badguys.pop(index_badguy)
				arrows.pop(index_arrow)
			index_arrow += 1
		index_badguy += 1
	for badguy in badguys:
		screen.blit(badguy_img, badguy)
	# 添加一个计时
	# 使用了PyGame默认的大小为24的字体来显示时间信息。
	font = pygame.font.Font(None, 24)
	survivedtext = font.render(str((90000-pygame.time.get_ticks())//60000)+":"+
							   str((90000-pygame.time.get_ticks())//1000%60).zfill(2), True, (0,0,0))
	textRect = survivedtext.get_rect()
	textRect.topright=[635,5]
	screen.blit(survivedtext, textRect)
	# 画出城堡健康值
	# 首先画了一个全红色的生命值条。然后根据城堡的生命值往生命条里面添加绿色。
	screen.blit(healthbar_img, (5, 5))
	for health1 in range(healthvalue):
		screen.blit(health_img, (health1+8, 8))
	# 更新屏幕
	pygame.display.flip()
	# 检查一些新的事件，如果有退出命令，则终止程序的执行
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		# 根据按下的键来更新按键记录数组
		if event.type == pygame.KEYDOWN:
			if event.key == K_w:
				keys[0] = True
			elif event.key == K_a:
				keys[1] = True
			elif event.key == K_s:
				keys[2] = True
			elif event.key == K_d:
				keys[3] = True
		if event.type == pygame.KEYUP:
			if event.key == K_w:
				keys[0] = False
			elif event.key == K_a:
				keys[1] = False
			elif event.key == K_s:
				keys[2] = False
			elif event.key == K_d:
				keys[3] = False
		# 当玩家点击鼠标，就要射出一支箭
		# 这段代码会检查是否鼠标被点击了，如果点击了，
		# 它就会得到鼠标的位置并且根据玩家和光标的位置计算出箭头旋转角度。
		# 旋转角度的值存放在arrows这个数组里。
		if event.type == pygame.MOUSEBUTTONDOWN:
			shoot.play()
			position = pygame.mouse.get_pos()
			acc[1] += 1
			arrows.append([math.atan2(position[1]-(playerpos1[1]+32), position[0]-(playerpos1[0]+26)),
						   playerpos1[0]+32, playerpos1[1]+26])
	# 移动玩家
	if keys[0]:
		playerpos[1] -= 5
	elif keys[2]:
		playerpos[1] += 5
	if keys[1]:
		playerpos[0] -= 5
	elif keys[3]:
		playerpos[0] += 5
	badtimer -= 1
	# 下面是一些胜利/失败的基本条件：
	# 如果时间到了(90s)：那么,停止运行游戏,设置游戏的输出;
	# 如果城堡被毁，那么：停止运行游戏，设置游戏的输出。
	# 精确度是一直都需要计算的。
	# 第一个if表达式是检查是否时间到了。
	# 第二个是检查城堡是否被摧毁了。
	# 第三个计算你的精准度。
	# 之后，一个if表达式是检查你是赢了还是输了，然后显示出相应的图片。
	if pygame.time.get_ticks() >= 90000:
		running = False
		exitcode = True
	if healthvalue <= 0:
		running = False
		exitcode = False
	if acc[1] != 0:
		accuracy = acc[0]*1.0/acc[1]*100
		accuracy = ("%.2f" % accuracy)
	else:
		accuracy = 0
if exitcode == False:
	pygame.font.init()
	font = pygame.font.Font(None, 24)
	text = font.render("Accuracy: "+str(accuracy)+"%", True, (255,0,0))
	textRect = text.get_rect()
	textRect.centerx = screen.get_rect().centerx
	textRect.centery = screen.get_rect().centery+24
	screen.blit(gameover_img, (0, 0))
	screen.blit(text, textRect)
else:
	pygame.font.init()
	font = pygame.font.Font(None, 24)
	text = font.render("Accuracy: "+accuracy+"%", True, (0,255,0))
	textRect = text.get_rect()
	textRect.centerx = screen.get_rect().centerx
	textRect.centery = screen.get_rect().centery+24
	screen.blit(youwin_img, (0,0))
	screen.blit(text, textRect)
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
	pygame.display.flip()