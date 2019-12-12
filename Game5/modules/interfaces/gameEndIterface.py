'''
Function:
	游戏结束界面
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import sys
import pygame


'''游戏结束界面'''
def gameEndIterface(screen, cfg, is_win=True):
	background_img = pygame.image.load(cfg.OTHER_IMAGE_PATHS.get('background'))
	gameover_img = pygame.image.load(cfg.OTHER_IMAGE_PATHS.get('gameover'))
	gameover_img = pygame.transform.scale(gameover_img, (256, 128))
	gameover_img_rect = gameover_img.get_rect()
	gameover_img_rect.midtop = cfg.WIDTH/2, cfg.HEIGHT/4.5
	font = pygame.font.Font(cfg.FONTPATH, cfg.WIDTH//20)
	if is_win:
		font_render = font.render('Congratulations, You win!', True, (255, 255, 255))
	else:
		font_render = font.render('Sorry, You fail!', True, (255, 255, 255))
	font_rect = font_render.get_rect()
	font_rect.centerx, font_rect.centery = cfg.WIDTH/2, cfg.HEIGHT/1.8
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		screen.blit(background_img, (0, 0))
		screen.blit(gameover_img, gameover_img_rect)
		screen.blit(font_render, font_rect)
		pygame.display.update()