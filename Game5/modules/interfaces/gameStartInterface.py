'''
Function:
	游戏开始界面
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import sys
import pygame


'''游戏开始界面'''
def gameStartInterface(screen, cfg):
	background_img = pygame.image.load(cfg.OTHER_IMAGE_PATHS.get('background'))
	color_white = (255, 255, 255)
	color_red = (255, 0, 0)
	font = pygame.font.Font(cfg.FONTPATH, cfg.WIDTH//12)
	logo_img = pygame.image.load(cfg.OTHER_IMAGE_PATHS.get('logo'))
	logo_img = pygame.transform.scale(logo_img, (446, 70))
	logo_rect = logo_img.get_rect()
	logo_rect.centerx, logo_rect.centery = cfg.WIDTH/2, cfg.HEIGHT//4
	tank_cursor = pygame.image.load(cfg.PLAYER_TANK_IMAGE_PATHS.get('player1')[0]).convert_alpha().subsurface((0, 144), (48, 48))
	tank_rect = tank_cursor.get_rect()
	# 玩家数量选择
	player_render_white = font.render('1 PLAYER', True, color_white)
	player_render_red = font.render('1 PLAYER', True, color_red)
	player_rect = player_render_white.get_rect()
	player_rect.left, player_rect.top = cfg.WIDTH/2.8, cfg.HEIGHT/2.5
	players_render_white = font.render('2 PLAYERS', True, color_white)
	players_render_red = font.render('2 PLAYERS', True, color_red)
	players_rect = players_render_white.get_rect()
	players_rect.left, players_rect.top = cfg.WIDTH/2.8, cfg.HEIGHT/2
	# 游戏提示
	game_tip = font.render('press <Enter> to start', True, color_white)
	game_tip_rect = game_tip.get_rect()
	game_tip_rect.centerx, game_tip_rect.top = cfg.WIDTH/2, cfg.HEIGHT/1.4
	game_tip_flash_time = 25
	game_tip_flash_count = 0
	game_tip_show_flag = True
	# 主循环
	clock = pygame.time.Clock()
	is_dual_mode = False
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					return is_dual_mode
				elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
					is_dual_mode = not is_dual_mode
		screen.blit(background_img, (0, 0))
		screen.blit(logo_img, logo_rect)
		game_tip_flash_count += 1
		if game_tip_flash_count > game_tip_flash_time:
			game_tip_show_flag = not game_tip_show_flag
			game_tip_flash_count = 0
		if game_tip_show_flag:
			screen.blit(game_tip, game_tip_rect)
		if not is_dual_mode:
			tank_rect.right, tank_rect.top = player_rect.left-10, player_rect.top
			screen.blit(tank_cursor, tank_rect)
			screen.blit(player_render_red, player_rect)
			screen.blit(players_render_white, players_rect)
		else:
			tank_rect.right, tank_rect.top = players_rect.left-10, players_rect.top
			screen.blit(tank_cursor, tank_rect)
			screen.blit(player_render_white, player_rect)
			screen.blit(players_render_red, players_rect)
		pygame.display.update()
		clock.tick(60)