'''
Function:
	乒乓球小游戏-主函数
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import sys
import config
import pygame
from sprites import *


'''定义按钮'''
def Button(screen, position, text, button_size=(200, 50)):
	left, top = position
	bwidth, bheight = button_size
	pygame.draw.line(screen, (150, 150, 150), (left, top), (left+bwidth, top), 5)
	pygame.draw.line(screen, (150, 150, 150), (left, top-2), (left, top+bheight), 5)
	pygame.draw.line(screen, (50, 50, 50), (left, top+bheight), (left+bwidth, top+bheight), 5)
	pygame.draw.line(screen, (50, 50, 50), (left+bwidth, top+bheight), (left+bwidth, top), 5)
	pygame.draw.rect(screen, (100, 100, 100), (left, top, bwidth, bheight))
	font = pygame.font.Font(config.FONTPATH, 30)
	text_render = font.render(text, 1, (255, 235, 205))
	return screen.blit(text_render, (left+50, top+10))


'''
Function:
	开始界面
Input:
	--screen: 游戏界面
Return:
	--game_mode: 1(单人模式)/2(双人模式)
'''
def startInterface(screen):
	clock = pygame.time.Clock()
	while True:
		screen.fill((41, 36, 33))
		button_1 = Button(screen, (150, 175), '1 Player')
		button_2 = Button(screen, (150, 275), '2 Player')
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if button_1.collidepoint(pygame.mouse.get_pos()):
					return 1
				elif button_2.collidepoint(pygame.mouse.get_pos()):
					return 2
		clock.tick(10)
		pygame.display.update()


'''结束界面'''
def endInterface(screen, score_left, score_right):
	clock = pygame.time.Clock()
	font1 = pygame.font.Font(config.FONTPATH, 30)
	font2 = pygame.font.Font(config.FONTPATH, 20)
	msg = 'Player on left won!' if score_left > score_right else 'Player on right won!'
	texts = [font1.render(msg, True, config.WHITE),
			 font2.render('Press ESCAPE to quit.', True, config.WHITE),
			 font2.render('Press ENTER to continue or play again.', True, config.WHITE)]
	positions = [[120, 200], [155, 270], [80, 300]]
	while True:
		screen.fill((41, 36, 33))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					return
				elif event.key == pygame.K_ESCAPE:
					sys.exit()
					pygame.quit()
		for text, pos in zip(texts, positions):
			screen.blit(text, pos)
		clock.tick(10)
		pygame.display.update()


'''运行游戏Demo'''
def runDemo(screen):
	# 加载游戏素材
	hit_sound = pygame.mixer.Sound(config.HITSOUNDPATH)
	goal_sound = pygame.mixer.Sound(config.GOALSOUNDPATH)
	pygame.mixer.music.load(config.BGMPATH)
	pygame.mixer.music.play(-1, 0.0)
	font = pygame.font.Font(config.FONTPATH, 50)
	# 开始界面
	game_mode = startInterface(screen)
	# 游戏主循环
	# --左边球拍(ws控制, 仅双人模式时可控制)
	score_left = 0
	racket_left = Racket(config.RACKETPICPATH, 'LEFT')
	# --右边球拍(↑↓控制)
	score_right = 0
	racket_right = Racket(config.RACKETPICPATH, 'RIGHT')
	# --球
	ball = Ball(config.BALLPICPATH)
	clock = pygame.time.Clock()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit(-1)
		screen.fill((41, 36, 33))
		# 玩家操作
		pressed_keys = pygame.key.get_pressed()
		if pressed_keys[pygame.K_UP]:
			racket_right.move('UP')
		elif pressed_keys[pygame.K_DOWN]:
			racket_right.move('DOWN')
		if game_mode == 2:
			if pressed_keys[pygame.K_w]:
				racket_left.move('UP')
			elif pressed_keys[pygame.K_s]:
				racket_left.move('DOWN')
		else:
			racket_left.automove(ball)
		# 球运动
		scores = ball.move(ball, racket_left, racket_right, hit_sound, goal_sound)
		score_left += scores[0]
		score_right += scores[1]
		# 显示
		# --分隔线
		pygame.draw.rect(screen, config.WHITE, (247, 0, 6, 500))
		# --球
		ball.draw(screen)
		# --拍
		racket_left.draw(screen)
		racket_right.draw(screen)
		# --得分
		screen.blit(font.render(str(score_left), False, config.WHITE), (150, 10))
		screen.blit(font.render(str(score_right), False, config.WHITE), (300, 10))
		if score_left == 11 or score_right == 11:
			return score_left, score_right
		clock.tick(100)
		pygame.display.update()


'''主函数'''
def main():
	# 初始化
	pygame.init()
	pygame.mixer.init()
	screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
	pygame.display.set_caption('pingpong - 微信公众号: Charles的皮卡丘')
	# 开始游戏
	while True:
		score_left, score_right = runDemo(screen)
		endInterface(screen, score_left, score_right)


'''run'''
if __name__ == '__main__':
	main()