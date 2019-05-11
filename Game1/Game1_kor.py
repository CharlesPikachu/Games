# coding: utf-8
# 저자: Charles
# 공개 번호: Charles的皮卡丘
# pygame 라이브러리를 가져오면 라이브러리에서 제공하는 기능을 사용할 수 있다
import pygame
from pygame.locals import *
import math   # 회전각도 계산할때 필요
import random # 랜덤함수 사용할때 필요

# pygame 초기화, 창 설정
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
# keys리스트는 버튼 누르기를 위한 것：WASD(순서대로 적용)
keys = [False, False, False, False]
# playerpos리스트는 플레이어의 위치를 표시
playerpos = [100, 100]
# 플레이어의 쏘는 정확도를 추적하여 쏜 화살 수와 맞은 오소리의 수를 기록
# 사격 정확도를 계산하는 데 사용.
acc = [0, 0]
# 추적 화살 변수
arrows = []
# 게임에서 시간이 경과하면 오소리를 새로 만들도록 타이머를 설정하였다.
badtimer = 100
badtimer1 = 0
badguys = [[640, 100]]
healthvalue = 194
# 재생 소리 초기화
pygame.mixer.init()

# 사진 추가
rabbit_img = pygame.image.load("resources/images/dude.png")
# 풍경을 더 추가~
grass_img = pygame.image.load("resources/images/grass.png")
castle_img = pygame.image.load("resources/images/castle.png")
# 화살 추가
arrow_img = pygame.image.load('resources/images/bullet.png')
# 오소리 추가
badguy_img1 = pygame.image.load("resources/images/badguy.png")
badguy_img = badguy_img1
# 성의 체력 사진 추가
healthbar_img = pygame.image.load("resources/images/healthbar.png")
health_img = pygame.image.load("resources/images/health.png")
# 승리 및 실패 사진 추가
gameover_img = pygame.image.load("resources/images/gameover.png")
youwin_img = pygame.image.load("resources/images/youwin.png")
# 음악 파일 추가 및 볼륨 설정
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
# 게임 배경음악 추가로 로딩, 배경음악 계속 틀게끔 함
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# 이어지게 끊임없이 계속 실행
# running변수는 게임 종료 여부를 확인하며，
# exitcode변수는 플레이어의 승리 여부를 확인한다。
running = True
exitcode = False
while running:
	# 실행하기 전 화면창 검정색으로 채우기
	screen.fill(0)
	# 풍경 사진 화면창에 띄우기
	for x in range(width//grass_img.get_width()+1):
		for y in range(height//grass_img.get_height()+1):
			screen.blit(grass_img, (x*100, y*100))
	screen.blit(castle_img, (0, 30))
	screen.blit(castle_img, (0, 135))
	screen.blit(castle_img, (0, 240))
	screen.blit(castle_img, (0, 345))
	# 마우스와 플레이어의 위치를 먼저 가져온다; 그리고 atan2 함수를 통해 도출된 각도와 호도를 얻는다.
	# 토끼가 회전하면 , 위치가 바뀐다。
	# 토끼의 바뀐 위치를 계산하고 화면에 띄워야 한다.
	position = pygame.mouse.get_pos()
	angle = math.atan2(position[1]-(playerpos[1]+32), position[0]-(playerpos[0]+26))
	playerrot = pygame.transform.rotate(rabbit_img, 360-angle*57.29)
	playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
	screen.blit(playerrot, playerpos1)
	# 화면에 화살 띄우기
	# vely와 velx의 값은 삼각정리에 의해 계산된다.
	# 10은 화살표의 속도. if 문은 화살이 화면 범위를 벗어나는지 검사하며,
	# 벗어나면 이 화살을 삭제
	# 두 번째 for 문은 화살을 해당 회전에 맞게 순환하여 쏩니다.
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
	# badtimer가 0인지 검사하고 0이면 오소리 하나를 만든 다음 badtimer를 다시 설정
	# 첫 번째 사이클은 오소리의 x 좌표를 업데이트하여 오소리를 화면 범위를 벗어나지 않는지 검사하고 범위를 벗어나면 오소리를 삭제.
	# 第二个循环是来画出所有的獾。// 두 번째 순환은 모든 오소리를 그리러 왔습니다?
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
		# 오소리는 성을 파괴한다
		# 이 단락 코드는 상당히 간단; 오소리의 x 좌표가 왼쪽에서 64보다 작으면
		# 악당(오소리)을 삭제하고 게임에서 체력 값을 줄이며 줄인 크기는 5~20의 랜덤 수다
		# 물론 오소리는 달려와 성에 닿을 때 사라진다
		badrect = pygame.Rect(badguy_img.get_rect())
		badrect.top = badguy[1]
		badrect.left = badguy[0]
		if badrect.left < 64:
			hit.play()
			healthvalue -= random.randint(5, 20)
			badguys.pop(index_badguy)
		# 모든 악당과 모든 화살을 순환시켜 충돌 여부를 검사합니다.
		# 충돌하면 오소리를 지우고 화살을 지우며 정밀도 변수에 1을 더한다.
		# 使用了PyGame内建功能来检查两个矩形是否交叉. //두 개의 직사각형이 교차하는지 검사하기 위해 PyGame 내건 기능이 사용되었다.?
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
	# 添加一个计时 //타임베이스를 하나 추가하려면?
	# 使用了PyGame默认的大小为24的字体来显示时间信息 //PyGame 묵시적인 크기가 24인 글꼴을 사용하여 시간 정보를 표시?
	font = pygame.font.Font(None, 24)
	survivedtext = font.render(str((90000-pygame.time.get_ticks())//60000)+":"+
							   str((90000-pygame.time.get_ticks())//1000%60).zfill(2), True, (0,0,0))
	textRect = survivedtext.get_rect()
	textRect.topright=[635,5]
	screen.blit(survivedtext, textRect)
	# 성의 체력 표시
	# 먼저 빨간색 체력 막대를 그림; 그리고 성의 체력값에 따라 체력 막대 안에 녹색을 더했습니다.
	screen.blit(healthbar_img, (5, 5))
	for health1 in range(healthvalue):
		screen.blit(health_img, (health1+8, 8))
	# 화면 업데이트
	pygame.display.flip()
	# 检查一些新的事件，如果有退出命令，则终止程序的执行 //일부 새로운 사건을 검토하여, 탈퇴 명령이 있을 경우, 프로그램의 실행을 중지한다.?
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		# 根据按下的键来更新按键记录数组 //누른 키에 따라 버튼 기록 그룹 업데이트?
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
		# 플레이어가 마우스를 클릭할 때, 화살 한 자루를 발사한다.
		#이 코드는 마우스가 클릭되었는지 검사하며, 만약 클릭하면
		# 그것은 마우스의 위치를 얻고 플레이어와 커서의 위치에 따라 화살표 회전 각도를 계산.
		# 회전 각도 값은 arrows라는 수 그룹에 저장된다.
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
	# 다음은  승리/실패의 기본 조건들이다：
	# 如果时间到了(90s)：那么,停止运行游戏,设置游戏的输出; //시간이 다 되면(90s): 그러면 게임을 실행 중지하고 게임의 출력을 설정
	# 如果城堡被毁，那么：停止运行游戏，设置游戏的输出。 //성이 파괴되면: 게임을 실행 중지하고 게임의 출력을 설정.
	# 정확도는 항상 계산해야 함
	# 第一个if表达式是检查是否时间到了。//첫 번째 if 문은 시간이 왔는지 검사합니다
	# 두번째 if문은 성이 파괴되었는지 검사.
	# 세 번째 if문은 플레이어의 정확도를 계산.
	# 마지막 if 문은 플레이어가 이겼는지 졌는지를 검사한 후에 그에 상응하는 그림을 보여준다。
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