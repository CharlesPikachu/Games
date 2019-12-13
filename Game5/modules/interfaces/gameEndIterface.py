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
	color_white = (255, 255, 255)
	color_red = (255, 0, 0)
	font = pygame.font.Font(cfg.FONTPATH, cfg.WIDTH//12)
	# 游戏失败图
	gameover_img = pygame.image.load(cfg.OTHER_IMAGE_PATHS.get('gameover'))
	gameover_img = pygame.transform.scale(gameover_img, (150, 75))
	gameover_img_rect = gameover_img.get_rect()
	gameover_img_rect.midtop = cfg.WIDTH/2, cfg.HEIGHT/8
	gameover_flash_time = 25
	gameover_flash_count = 0
	gameover_show_flag = True
	# 游戏胜利与否的提示
	if is_win:
		font_render = font.render('Congratulations, You win!', True, color_white)
	else:
		font_render = font.render('Sorry, You fail!', True, color_white)
	font_rect = font_render.get_rect()
	font_rect.centerx, font_rect.centery = cfg.WIDTH/2, cfg.HEIGHT/3
	# 用于选择退出或重新开始
	tank_cursor = pygame.image.load(cfg.PLAYER_TANK_IMAGE_PATHS.get('player1')[0]).convert_alpha().subsurface((0, 144), (48, 48))
	tank_rect = tank_cursor.get_rect()
	restart_render_white = font.render('RESTART', True, color_white)
	restart_render_red = font.render('RESTART', True, color_red)
	restart_rect = restart_render_white.get_rect()
	restart_rect.left, restart_rect.top = cfg.WIDTH/2.4, cfg.HEIGHT/2
	quit_render_white = font.render('QUIT', True, color_white)
	quit_render_red = font.render('QUIT', True, color_red)
	quit_rect = quit_render_white.get_rect()
	quit_rect.left, quit_rect.top = cfg.WIDTH/2.4, cfg.HEIGHT/1.6
	is_quit_game = False
	# 主循环
	clock = pygame.time.Clock()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					return is_quit_game
				elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
					is_quit_game = not is_quit_game
		screen.blit(background_img, (0, 0))
		gameover_flash_count += 1
		if gameover_flash_count > gameover_flash_time:
			gameover_show_flag = not gameover_show_flag
			gameover_flash_count = 0
		if gameover_show_flag:
			screen.blit(gameover_img, gameover_img_rect)
		screen.blit(font_render, font_rect)
		if not is_quit_game:
			tank_rect.right, tank_rect.top = restart_rect.left-10, restart_rect.top
			screen.blit(tank_cursor, tank_rect)
			screen.blit(restart_render_red, restart_rect)
			screen.blit(quit_render_white, quit_rect)
		else:
			tank_rect.right, tank_rect.top = quit_rect.left-10, quit_rect.top
			screen.blit(tank_cursor, tank_rect)
			screen.blit(restart_render_white, restart_rect)
			screen.blit(quit_render_red, quit_rect)
		pygame.display.update()
		clock.tick(60)