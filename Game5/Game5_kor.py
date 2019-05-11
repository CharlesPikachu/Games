# coding: utf-8
# 저자 : Charles
# 공개번호 : Charles의 피카츄
# 메인 프로그램을 실행하는 게임
import sys
import pygame
import scene
import bullet
import food
import tanks
import home
from pygame.locals import *


# 인터페이스 디스플레이 시작
def show_start_interface(screen, width, height):
	tfont = pygame.font.Font('./font/simkai.ttf', width//4)
	cfont = pygame.font.Font('./font/simkai.ttf', width//20)
	title = tfont.render(u'坦克大战', True, (255, 0, 0))#탱크 전투
	content1 = cfont.render(u'按1键进入单人游戏', True, (0, 0, 255))#싱글플레이를 시작하려면 1을 누르십시오
	content2 = cfont.render(u'按2键进入双人人游戏', True, (0, 0, 255))#듀오플레이를 시작하려면 2를 누르십시오
	trect = title.get_rect()
	trect.midtop = (width/2, height/4)
	crect1 = content1.get_rect()
	crect1.midtop = (width/2, height/1.8)
	crect2 = content2.get_rect()
	crect2.midtop = (width/2, height/1.6)
	screen.blit(title, trect)
	screen.blit(content1, crect1)
	screen.blit(content2, crect2)
	pygame.display.update()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					return 1
				if event.key == pygame.K_2:
					return 2


# 종료화면 표시
def show_end_interface(screen, width, height, is_win):
	bg_img = pygame.image.load("./images/others/background.png")
	screen.blit(bg_img, (0, 0))
	if is_win:
		font = pygame.font.Font('./font/simkai.ttf', width//10)
		content = font.render(u'恭喜通关！', True, (255, 0, 0))#축하해!
		rect = content.get_rect()
		rect.midtop = (width/2, height/2)
		screen.blit(content, rect)
	else:
		fail_img = pygame.image.load("./images/others/gameover.png")
		rect = fail_img.get_rect()
		rect.midtop = (width/2, height/2)
		screen.blit(fail_img, rect)
	pygame.display.update()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()


# 레벨스위치
def show_switch_stage(screen, width, height, stage):
	bg_img = pygame.image.load("./images/others/background.png")
	screen.blit(bg_img, (0, 0))
	font = pygame.font.Font('./font/simkai.ttf', width//10)
	content = font.render(u'第%d关' % stage, True, (0, 255, 0))#레벨(숫자)
	rect = content.get_rect()
	rect.midtop = (width/2, height/2)
	screen.blit(content, rect)
	pygame.display.update()
	delay_event = pygame.constants.USEREVENT
	pygame.time.set_timer(delay_event, 1000)
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()
			if event.type == delay_event:
				return


# 주요기능
def main():
	# 초기화
	pygame.init()
	pygame.mixer.init()
	screen = pygame.display.set_mode((630, 630))
	pygame.display.set_caption("坦克大战-公众号: Charles的皮卡丘")#탱크전투-공개번호:Charles의 피카츄
	# 이미지 로드중
	bg_img = pygame.image.load("./images/others/background.png")
	# 사운드 로드
	add_sound = pygame.mixer.Sound("./audios/add.wav")
	add_sound.set_volume(1)
	bang_sound = pygame.mixer.Sound("./audios/bang.wav")
	bang_sound.set_volume(1)
	blast_sound = pygame.mixer.Sound("./audios/blast.wav")
	blast_sound.set_volume(1)
	fire_sound = pygame.mixer.Sound("./audios/fire.wav")
	fire_sound.set_volume(1)
	Gunfire_sound = pygame.mixer.Sound("./audios/Gunfire.wav")
	Gunfire_sound.set_volume(1)
	hit_sound = pygame.mixer.Sound("./audios/hit.wav")
	hit_sound.set_volume(1)
	start_sound = pygame.mixer.Sound("./audios/start.wav")
	start_sound.set_volume(1)
	# 시작인터페이스
	num_player = show_start_interface(screen, 630, 630)
	# 게임 시작시 음악재생
	start_sound.play()
	# 레벨(수준)
	stage = 0
	num_stage = 2
	# 게임이 끝났는지 여부
	is_gameover = False
	# 시계
	clock = pygame.time.Clock()
	# 메인루프
	while not is_gameover:
		# 레벨(수준)
		stage += 1
		if stage > num_stage:
			break
		show_switch_stage(screen, 630, 630, stage)
		# 레벨에서의 탱크의 총 수
		enemytanks_total = min(stage * 18, 80)
		# 현장에 있는 총 적 탱크 수
		enemytanks_now = 0
		# 현장에 존재할 수 있는 적의 총 탱크 수
		enemytanks_now_max = min(max(stage * 2, 4), 8)
		# 스프라이트그룹
		tanksGroup = pygame.sprite.Group()
		mytanksGroup = pygame.sprite.Group()
		enemytanksGroup = pygame.sprite.Group()
		bulletsGroup = pygame.sprite.Group()
		mybulletsGroup = pygame.sprite.Group()
		enemybulletsGroup = pygame.sprite.Group()
		myfoodsGroup = pygame.sprite.Group()
		# 맞춤사건
		# 	-적 탱크 생성 사건
		genEnemyEvent = pygame.constants.USEREVENT + 0
		pygame.time.set_timer(genEnemyEvent, 100)
		# 	-\적 탱크 정지 복구 사건
		recoverEnemyEvent = pygame.constants.USEREVENT + 1
		pygame.time.set_timer(recoverEnemyEvent, 8000)
		# 	-아군 탱크 무적 회복 사건
		noprotectMytankEvent = pygame.constants.USEREVENT + 2
		pygame.time.set_timer(noprotectMytankEvent, 8000)
		# 레벨 맵
		map_stage = scene.Map(stage)
		# 아군 탱크
		tank_player1 = tanks.myTank(1)
		tanksGroup.add(tank_player1)
		mytanksGroup.add(tank_player1)
		if num_player > 1:
			tank_player2 = tanks.myTank(2)
			tanksGroup.add(tank_player2)
			mytanksGroup.add(tank_player2)
		is_switch_tank = True
		player1_moving = False
		player2_moving = False
		# 타이어를 위한 애니메이션 효과
		time = 0
		# 적 탱크
		for i in range(0, 3):
			if enemytanks_total > 0:
				enemytank = tanks.enemyTank(i)
				tanksGroup.add(enemytank)
				enemytanksGroup.add(enemytank)
				enemytanks_now += 1
				enemytanks_total -= 1
		# 베이스 캠프
		myhome = home.Home()
		# 모양 효과
		appearance_img = pygame.image.load("./images/others/appear.png").convert_alpha()
		appearances = []
		appearances.append(appearance_img.subsurface((0, 0), (48, 48)))
		appearances.append(appearance_img.subsurface((48, 0), (48, 48)))
		appearances.append(appearance_img.subsurface((96, 0), (48, 48)))
		# 레벨 메인 루프
		while True:
			if is_gameover is True:
				break
			if enemytanks_total < 1 and enemytanks_now < 1:
				is_gameover = False
				break
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == genEnemyEvent:
					if enemytanks_total > 0:
						if enemytanks_now < enemytanks_now_max:
							enemytank = tanks.enemyTank()
							if not pygame.sprite.spritecollide(enemytank, tanksGroup, False, None):
								tanksGroup.add(enemytank)
								enemytanksGroup.add(enemytank)
								enemytanks_now += 1
								enemytanks_total -= 1
				if event.type == recoverEnemyEvent:
					for each in enemytanksGroup:
						each.can_move = True
				if event.type == noprotectMytankEvent:
					for each in mytanksGroup:
						mytanksGroup.protected = False
			# 사용자 키보드 작업 확인
			key_pressed = pygame.key.get_pressed()
			# 플레이어1
			# WSAD키 -> 상하 좌우(각각)
			# 스페이스 바 슈팅(공격)
			if key_pressed[pygame.K_w]:
				tanksGroup.remove(tank_player1)
				tank_player1.move_up(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
				tanksGroup.add(tank_player1)
				player1_moving = True
			elif key_pressed[pygame.K_s]:
				tanksGroup.remove(tank_player1)
				tank_player1.move_down(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
				tanksGroup.add(tank_player1)
				player1_moving = True
			elif key_pressed[pygame.K_a]:
				tanksGroup.remove(tank_player1)
				tank_player1.move_left(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
				tanksGroup.add(tank_player1)
				player1_moving = True
			elif key_pressed[pygame.K_d]:
				tanksGroup.remove(tank_player1)
				tank_player1.move_right(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
				tanksGroup.add(tank_player1)
				player1_moving = True
			elif key_pressed[pygame.K_SPACE]:
				if not tank_player1.bullet.being:
					fire_sound.play()
					tank_player1.shoot()
			# 플레이어2
			# ↑↓←→ -> 상하좌우(각각)
			# 작은 키보드의 0키 공격
			if num_player > 1:
				if key_pressed[pygame.K_UP]:
					tanksGroup.remove(tank_player2)
					tank_player2.move_up(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
					tanksGroup.add(tank_player2)
					player2_moving = True
				elif key_pressed[pygame.K_DOWN]:
					tanksGroup.remove(tank_player2)
					tank_player2.move_down(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
					tanksGroup.add(tank_player2)
					player2_moving = True
				elif key_pressed[pygame.K_LEFT]:
					tanksGroup.remove(tank_player2)
					tank_player2.move_left(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
					tanksGroup.add(tank_player2)
					player2_moving = True
				elif key_pressed[pygame.K_RIGHT]:
					tanksGroup.remove(tank_player2)
					tank_player2.move_right(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
					tanksGroup.add(tank_player2)
					player2_moving = True
				elif key_pressed[pygame.K_KP0]:
					if not tank_player2.bullet.being:
						fire_sound.play()
						tank_player2.shoot()
			# 배경
			screen.blit(bg_img, (0, 0))
			# 돌 벽
			for each in map_stage.brickGroup:
				screen.blit(each.brick, each.rect)
			# 강철 벽
			for each in map_stage.ironGroup:
				screen.blit(each.iron, each.rect)
			# 얼음
			for each in map_stage.iceGroup:
				screen.blit(each.ice, each.rect)
			# 河강
			for each in map_stage.riverGroup:
				screen.blit(each.river, each.rect)
			# 나무
			for each in map_stage.treeGroup:
				screen.blit(each.tree, each.rect)
			time += 1
			if time == 5:
				time = 0
				is_switch_tank = not is_switch_tank
			# 아군 탱크
			if tank_player1 in mytanksGroup:
				if is_switch_tank and player1_moving:
					screen.blit(tank_player1.tank_0, (tank_player1.rect.left, tank_player1.rect.top))
					player1_moving = False
				else:
					screen.blit(tank_player1.tank_1, (tank_player1.rect.left, tank_player1.rect.top))
				if tank_player1.protected:
					screen.blit(tank_player1.protected_mask1, (tank_player1.rect.left, tank_player1.rect.top))
			if num_player > 1:
				if tank_player2 in mytanksGroup:
					if is_switch_tank and player2_moving:
						screen.blit(tank_player2.tank_0, (tank_player2.rect.left, tank_player2.rect.top))
						player1_moving = False
					else:
						screen.blit(tank_player2.tank_1, (tank_player2.rect.left, tank_player2.rect.top))
					if tank_player2.protected:
						screen.blit(tank_player1.protected_mask1, (tank_player2.rect.left, tank_player2.rect.top))
			# 적 탱크
			for each in enemytanksGroup:
				# 出生特效//출생 특수 효과
				if each.born:
					if each.times > 0:
						each.times -= 1
						if each.times <= 10:
							screen.blit(appearances[2], (3+each.x*12*24, 3))
						elif each.times <= 20:
							screen.blit(appearances[1], (3+each.x*12*24, 3))
						elif each.times <= 30:
							screen.blit(appearances[0], (3+each.x*12*24, 3))
						elif each.times <= 40:
							screen.blit(appearances[2], (3+each.x*12*24, 3))
						elif each.times <= 50:
							screen.blit(appearances[1], (3+each.x*12*24, 3))
						elif each.times <= 60:
							screen.blit(appearances[0], (3+each.x*12*24, 3))
						elif each.times <= 70:
							screen.blit(appearances[2], (3+each.x*12*24, 3))
						elif each.times <= 80:
							screen.blit(appearances[1], (3+each.x*12*24, 3))
						elif each.times <= 90:
							screen.blit(appearances[0], (3+each.x*12*24, 3))
					else:
						each.born = False
				else:
					if is_switch_tank:
						screen.blit(each.tank_0, (each.rect.left, each.rect.top))
					else:
						screen.blit(each.tank_1, (each.rect.left, each.rect.top))
					if each.can_move:
						tanksGroup.remove(each)
						each.move(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
						tanksGroup.add(each)
			# 총알
			for tank_player in mytanksGroup:
				if tank_player.bullet.being:
					tank_player.bullet.move()
					screen.blit(tank_player.bullet.bullet, tank_player.bullet.rect)
					# 총알과 총알 충돌
					for each in enemybulletsGroup:
						if each.being:
							if pygame.sprite.collide_rect(tank_player.bullet, each):
								tank_player.bullet.being = False
								each.being = False
								enemybulletsGroup.remove(each)
								break
						else:
							enemybulletsGroup.remove(each)	
					# 적의 탱크와 총알 충돌
					for each in enemytanksGroup:
						if each.being:
							if pygame.sprite.collide_rect(tank_player.bullet, each):
								if each.is_red == True:
									myfood = food.Food()
									myfood.generate()
									myfoodsGroup.add(myfood)
									each.is_red = False
								each.blood -= 1
								each.color -= 1
								if each.blood < 0:
									bang_sound.play()
									each.being = False
									enemytanksGroup.remove(each)
									enemytanks_now -= 1
									tanksGroup.remove(each)
								else:
									each.reload()
								tank_player.bullet.being = False
								break
						else:
							enemytanksGroup.remove(each)
							tanksGroup.remove(each)
					# 총알과 돌 벽 충돌
					if pygame.sprite.spritecollide(tank_player.bullet, map_stage.brickGroup, True, None):
						tank_player.bullet.being = False
					'''
					# 등가 체계(보다 과학적)
					for each in map_stage.brickGroup:
						if pygame.sprite.collide_rect(tank_player.bullet, each):
							tank_player.bullet.being = False
							each.being = False
							map_stage.brickGroup.remove(each)
							break
					'''
					# 총알과 강철 벽 충돌
					if tank_player.bullet.stronger:
						if pygame.sprite.spritecollide(tank_player.bullet, map_stage.ironGroup, True, None):
							tank_player.bullet.being = False
					else:
						if pygame.sprite.spritecollide(tank_player.bullet, map_stage.ironGroup, False, None):
							tank_player.bullet.being = False
					'''
					# 등가체계(보다 과학적)
					for each in map_stage.ironGroup:
						if pygame.sprite.collide_rect(tank_player.bullet, each):
							tank_player.bullet.being = False
							if tank_player.bullet.stronger:
								each.being = False
								map_stage.ironGroup.remove(each)
							break
					'''
					# 총알이 베이스캠프 공격
					if pygame.sprite.collide_rect(tank_player.bullet, myhome):
						tank_player.bullet.being = False
						myhome.set_dead()
						is_gameover = True
			# 총알
			for each in enemytanksGroup:
				if each.being:
					if each.can_move and not each.bullet.being:
						enemybulletsGroup.remove(each.bullet)
						each.shoot()
						enemybulletsGroup.add(each.bullet)
					if not each.born:
						if each.bullet.being:
							each.bullet.move()
							screen.blit(each.bullet.bullet, each.bullet.rect)
							# 총알이 아군 탱크에 충돌
							for tank_player in mytanksGroup:
								if pygame.sprite.collide_rect(each.bullet, tank_player):
									if not tank_player.protected:
										bang_sound.play()
										tank_player.life -= 1
										if tank_player.life < 0:
											mytanksGroup.remove(tank_player)
											tanksGroup.remove(tank_player)
											if len(mytanksGroup) < 1:
												is_gameover = True
										else:
											tank_player.reset()
									each.bullet.being = False
									enemybulletsGroup.remove(each.bullet)
									break
							# 총알과 돌 벽 충돌
							if pygame.sprite.spritecollide(each.bullet, map_stage.brickGroup, True, None):
								each.bullet.being = False
								enemybulletsGroup.remove(each.bullet)
							'''
							# 등가 체계(보다 과학적)
							for one in map_stage.brickGroup:
								if pygame.sprite.collide_rect(each.bullet, one):
									each.bullet.being = False
									one.being = False
									enemybulletsGroup.remove(one)
									break
							'''
							# 총알과 강철 벽 충돌
							if each.bullet.stronger:
								if pygame.sprite.spritecollide(each.bullet, map_stage.ironGroup, True, None):
									each.bullet.being = False
							else:
								if pygame.sprite.spritecollide(each.bullet, map_stage.ironGroup, False, None):
									each.bullet.being = False
							'''
							# 등가체계 (보다 과학적)
							for one in map_stage.ironGroup:
								if pygame.sprite.collide_rect(each.bullet, one):
									each.bullet.being = False
									if each.bullet.stronger:
										one.being = False
										map_stage.ironGroup.remove(one)
									break
							'''
							# 총알이 베이스캠프를 공격
							if pygame.sprite.collide_rect(each.bullet, myhome):
								each.bullet.being = False
								myhome.set_dead()
								is_gameover = True
				else:
					enemytanksGroup.remove(each)
					tanksGroup.remove(each)
			# 집
			screen.blit(myhome.home, myhome.rect)
			# 음식
			for myfood in myfoodsGroup:
				if myfood.being and myfood.time > 0:
					screen.blit(myfood.food, myfood.rect)
					myfood.time -= 1
					for tank_player in mytanksGroup:
						if pygame.sprite.collide_rect(tank_player, myfood):
							# 현재의 모든 적을 파괴하십시오
							if myfood.kind == 0:
								for _ in enemytanksGroup:
									bang_sound.play()
								enemytanksGroup = pygame.sprite.Group()
								enemytanks_total -= enemytanks_now
								enemytanks_now = 0
							# 적이 정지하다
							if myfood.kind == 1:
								for each in enemytanksGroup:
									each.can_move = False
							# 총알 강화
							if myfood.kind == 2:
								add_sound.play()
								tank_player.bullet.stronger = True
							# 베이스캠프의 벽을 강철 벽으로 바꾼다.
							if myfood.kind == 3:
								map_stage.protect_home()
							# 탱크 잠시동안 보호막 얻음.
							if myfood.kind == 4:
								add_sound.play()
								for tank_player in mytanksGroup:
									tank_player.protected = True
							# 탱크 업그레이드
							if myfood.kind == 5:
								add_sound.play()
								tank_player.up_level()
							# 탱크 생명+1
							if myfood.kind == 6:
								add_sound.play()
								tank_player.life += 1
							myfood.being = False
							myfoodsGroup.remove(myfood)
							break
				else:
					myfood.being = False
					myfoodsGroup.remove(myfood)
			pygame.display.flip()
			clock.tick(60)
	if not is_gameover:
		show_end_interface(screen, 630, 630, True)
	else:
		show_end_interface(screen, 630, 630, False)


if __name__ == '__main__':
	main()