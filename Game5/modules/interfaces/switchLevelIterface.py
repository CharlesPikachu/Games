'''
Function:
	关卡切换界面
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import sys
import pygame


'''关卡切换界面'''
def switchLevelIterface(screen, cfg, level_next=1):
	background_img = pygame.image.load(cfg.OTHER_IMAGE_PATHS.get('background'))
	logo_img = pygame.image.load(cfg.OTHER_IMAGE_PATHS.get('logo'))
	logo_img = pygame.transform.scale(logo_img, (446, 70))
	logo_rect = logo_img.get_rect()
	logo_rect.centerx, logo_rect.centery = cfg.WIDTH/2, cfg.HEIGHT//4
	font = pygame.font.Font(cfg.FONTPATH, cfg.WIDTH//25)
	font_render = font.render('Loading game data, You will enter Level-%s' % level_next, True, (255, 255, 255))
	font_rect = font_render.get_rect()
	font_rect.centerx, font_rect.centery = cfg.WIDTH/2, cfg.HEIGHT/2
	delay_event = pygame.constants.USEREVENT
	pygame.time.set_timer(delay_event, 2000)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == delay_event:
				return
		screen.blit(background_img, (0, 0))
		screen.blit(logo_img, logo_rect)
		screen.blit(font_render, font_rect)
		pygame.display.update()