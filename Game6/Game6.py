# 作者: Charles
# 公众号: Charles的皮卡丘
# python制作小游戏系列-FlappyBird
import Bird
import Pipe
import pygame
from pygame.locals import *


# 定义一些常量
WIDTH, HEIGHT = 640, 480


# 主函数
def main():
	# 初始化
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
	pygame.display.set_caption('FlappyBird-公众号: Charles的皮卡丘')
	# 载入图片
	background_img = pygame.image.load("./resources/images/background.png")
	gameover_img = pygame.image.load("./resources/images/gameover.png")
	# 载入音乐
	jump_sound = pygame.mixer.Sound("./resources/audios/jump.wav")
	jump_sound.set_volume(6)
	pygame.mixer.music.load('./resources/audios/moonlight.wav')
	pygame.mixer.music.play(-1, 0.0)
	pygame.mixer.music.set_volume(12)
	# 载入字体
	font = pygame.font.Font("./resources/fonts/simkai.ttf", 24)
	# 时钟
	clock = pygame.time.Clock()
	# 小鸟
	bird = Bird.Bird(HEIGHT, WIDTH)
	# 管道
	pipes = []
	# 时间
	time0 = 0
	time_interval = 2
	# 分数
	SCORE = 0
	running = True
	# 主循环
	while running:
		# 画背景
		screen.fill(0)
		for x in range(WIDTH // background_img.get_width() + 1):
			for y in range(HEIGHT // background_img.get_height() + 1):
				screen.blit(background_img, (x * 100, y * 100))
		time_passed = clock.tick() / 1000
		# 事件捕获
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)
			if event.type == pygame.KEYDOWN:
				if event.key == K_SPACE:
					jump_sound.play()
					bird.cur_jump_height = 0
					bird.is_jump = True
		# 画鸟
		bird.update(time_passed)
		screen.blit(bird.rotated_bird, bird.rect)
		if bird.is_dead():
			running = False
		# 画管道
		time1 = pygame.time.get_ticks() / 1000
		if time1 - time0 > time_interval:
			time0 = time1
			pipes.append(Pipe.Pipe(HEIGHT, WIDTH))
		for i, pipe in enumerate(pipes):
			pipe.update(time_passed)
			for p in pipe.pipe:
				screen.blit(p.img, p.rect)
			if bird.rect.left > pipe.x + Pipe.pipeHead().width and not pipe.add_score:
				SCORE += 1
				pipe.add_score = True
			if pipe.x + Pipe.pipeHead().width < 0:
				pipes.pop(i)
			# 碰撞检测
			if pygame.sprite.spritecollide(bird, pipe.pipe, False, None):
				if bird.rect.left < pipe.x + (Pipe.pipeHead().width + Pipe.pipeBody().width) / 2:
					running = False
		# 显示分数
		scoreText = font.render('Score: ' + str(SCORE), True, (0, 0, 0))
		scoreRect = scoreText.get_rect()
		scoreRect.topleft = [10, 10]
		screen.blit(scoreText, scoreRect)
		pygame.display.flip()
		pygame.display.update()
	screen.blit(gameover_img, (0, 0))
	pygame.display.flip()
	pygame.display.update()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)


if __name__ == "__main__":
	main()