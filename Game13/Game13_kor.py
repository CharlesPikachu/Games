'''
Function:
	외계인 침공 게임
Author:
	Charles
닉네임:
	Charles의 피카츄
'''
import os
import sys
import random
import pygame
from utils import *
	

	

'''약간의 상량'''
WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 250, 5)
RED = (255, 0, 0)
FPS = 60
	

	

'''
Function:
	게임 시작
'''
def startGame(screen):
	clock = pygame.time.Clock()
	# 글꼴 추가로 적재
	font = pygame.font.SysFont('arial', 18)
	if not os.path.isfile('score'):
		f = open('score', 'w')
		f.write('0')
		f.close()
	with open('score', 'r') as f:
		highest_score = int(f.read().strip())
	# 적측
	enemies_group = pygame.sprite.Group()
	for i in range(55):
		if i < 11:
			enemy = enemySprite('small', i, WHITE, WHITE)
		elif i < 33:
			enemy = enemySprite('medium', i, WHITE, WHITE)
		else:
			enemy = enemySprite('large', i, WHITE, WHITE)
		enemy.rect.x = 85 + (i % 11) * 50
		enemy.rect.y = 120 + (i // 11) * 45
		enemies_group.add(enemy)
	boomed_enemies_group = pygame.sprite.Group()
	en_bullets_group = pygame.sprite.Group()
	ufo = ufoSprite(color=RED)
	# 우리측
	myaircraft = aircraftSprite(color=GREEN, bullet_color=WHITE)
	my_bullets_group = pygame.sprite.Group()
	# 적의 위치 업데이트를 제어하는데 사용
	# 	한 줄 이동
	enemy_move_count = 24
	enemy_move_interval = 24
	enemy_move_flag = False
	# 	이동 방향 변경(방향 변경과 동시에 집단으로 한번 하강)
	enemy_change_direction_count = 0
	enemy_change_direction_interval = 60
	enemy_need_down = False
	enemy_move_right = True
	enemy_need_move_row = 6
	enemy_max_row = 5
	# 적의 탄알 발사를 통제하는데 사용
	enemy_shot_interval = 20
	enemy_shot_count = 0
	enemy_shot_flag = False
	# 게임 진행 중
	running = True
	is_win = False
	# 메인 사이클
	while running:
		screen.fill(BLACK)
		for event in pygame.event.get():
			# 오른쪽 상단 모서리에 있는 X를 켜거나 Esc키를 눌러 게임에서 로그아웃
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
			# 사격
			if event.type == pygame.MOUSEBUTTONDOWN:
				my_bullet = myaircraft.shot()
				if my_bullet:
					my_bullets_group.add(my_bullet)
		# 우리측 총알이 적/UFO와 충돌하여 감지
		for enemy in enemies_group:
			if pygame.sprite.spritecollide(enemy, my_bullets_group, True, None):
				boomed_enemies_group.add(enemy)
				enemies_group.remove(enemy)
				myaircraft.score += enemy.reward
		if pygame.sprite.spritecollide(ufo, my_bullets_group, True, None):
			ufo.is_dead = True
			myaircraft.score += ufo.reward
		# 적측 업데이트와 그리기
		# 	적의 총알
		enemy_shot_count += 1
		if enemy_shot_count > enemy_shot_interval:
			enemy_shot_flag = True
			enemies_survive_list = [enemy.number for enemy in enemies_group]
			shot_number = random.choice(enemies_survive_list)
			enemy_shot_count = 0
		# 	적의 이동
		enemy_move_count += 1
		if enemy_move_count > enemy_move_interval:
			enemy_move_count = 0
			enemy_move_flag = True
			enemy_need_move_row -= 1
			if enemy_need_move_row == 0:
				enemy_need_move_row = enemy_max_row
				enemy_change_direction_count += 1
			if enemy_change_direction_count > enemy_change_direction_interval:
				enemy_change_direction_count = 1
				enemy_move_right = not enemy_move_right
				enemy_need_down = True
				# 매번 하강할 때마다 이동과 사격 속도 향상
				enemy_move_interval = max(15, enemy_move_interval-3)
				enemy_shot_interval = max(50, enemy_move_interval-10)
		# 	여러 차례에 걸쳐 갱신
		for enemy in enemies_group:
			if enemy_shot_flag:
				if enemy.number == shot_number:
					en_bullet = enemy.shot()
					en_bullets_group.add(en_bullet)
			if enemy_move_flag:
				if enemy.number in range((enemy_need_move_row-1)*11, enemy_need_move_row*11):
					if enemy_move_right:
						enemy.update('right', HEIGHT)
					else:
						enemy.update('left', HEIGHT)
			else:
				enemy.update(None, HEIGHT)
			if enemy_need_down:
				if enemy.update('down', HEIGHT):
					running = False
					is_win = False
				enemy.change_count -= 1
			enemy.draw(screen)
		enemy_move_flag = False
		enemy_need_down = False
		enemy_shot_flag = False
		# 	적의 폭발 특효
		for boomed_enemy in boomed_enemies_group:
			if boomed_enemy.boom(screen):
				boomed_enemies_group.remove(boomed_enemy)
				del boomed_enemy
		# 적의 총탄이 우리측 비행선과 충돌하여 감지됨
		if not myaircraft.one_dead:
			if pygame.sprite.spritecollide(myaircraft, en_bullets_group, True, None):
				myaircraft.one_dead = True
		if myaircraft.one_dead:
			if myaircraft.boom(screen):
				myaircraft.resetBoom()
				myaircraft.num_life -= 1
				if myaircraft.num_life < 1:
					running = False
					is_win = False
		else:
			# 비행선 갱신
			myaircraft.update(WIDTH)
			# 비행선 그리기
			myaircraft.draw(screen)
		if (not ufo.has_boomed) and (ufo.is_dead):
			if ufo.boom(screen):
				ufo.has_boomed = True
		else:
			# UFO 갱신
			ufo.update(WIDTH)
			# UFO 그림
			ufo.draw(screen)
		# 우리측 비행선 총알 그리기
		for bullet in my_bullets_group:
			if bullet.update():
				my_bullets_group.remove(bullet)
				del bullet
			else:
				bullet.draw(screen)
		# 적의 탄알 그리기
		for bullet in en_bullets_group:
			if bullet.update(HEIGHT):
				en_bullets_group.remove(bullet)
				del bullet
			else:
				bullet.draw(screen)
		if myaircraft.score > highest_score:
			highest_score = myaircraft.score
		# 점수가 2000점 늘어날 때마다 우리 비행선은 생명 하나 더 늘림
		if (myaircraft.score % 2000 == 0) and (myaircraft.score > 0) and (myaircraft.score != myaircraft.old_score):
			myaircraft.old_score = myaircraft.score
			myaircraft.num_life = min(myaircraft.num_life + 1, myaircraft.max_num_life)
		# 적들이 다 죽으면 승리
		if len(enemies_group) < 1:
			is_win = True
			running = False
		# 문자 표시
		# 	현재득점
		showText(screen, 'SCORE: ', WHITE, font, 200, 8)
		showText(screen, str(myaircraft.score), WHITE, font, 200, 24)
		# 	적의 수
		showText(screen, 'ENEMY: ', WHITE, font, 370, 8)
		showText(screen, str(len(enemies_group)), WHITE, font, 370, 24)
		# 	역대 최고 점수
		showText(screen, 'HIGHEST: ', WHITE, font, 540, 8)
		showText(screen, str(highest_score), WHITE, font, 540, 24)
		# 	FPS
		showText(screen, 'FPS: ' + str(int(clock.get_fps())), RED, font, 8, 8)
		# 남은 생명 수
		showLife(screen, myaircraft.num_life, GREEN)
		pygame.display.update()
		clock.tick(FPS)
	with open('score', 'w') as f:
		f.write(str(highest_score))
	return is_win
	

	

	'''메인 함수'''
	def main():
		# 초기화
		pygame.init()
		pygame.display.set_caption(u'닉네임-Charles의 피카츄')
		screen = pygame.display.set_mode([WIDTH, HEIGHT])
		pygame.mixer.init()
		pygame.mixer.music.load('./music/bg.mp3')
		pygame.mixer.music.set_volume(0.4)
		pygame.mixer.music.play(-1)
		while True:
			is_win = startGame(screen)
			endInterface(screen, BLACK, is_win)
	

	

	if __name__ == '__main__':
		main()

