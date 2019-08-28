'''
Function:
	炸弹人小游戏
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import sys
import cfg
import random
import pygame
from modules.MAP import *
from modules.misc import *
from modules.Sprites import *


'''游戏主程序'''
def main(cfg):
	# 初始化
	pygame.init()
	pygame.mixer.init()
	pygame.mixer.music.load(cfg.BGMPATH)
	pygame.mixer.music.play(-1, 0.0)
	screen = pygame.display.set_mode(cfg.SCREENSIZE)
	pygame.display.set_caption('Bomber Man - 微信公众号: Charles的皮卡丘')
	# 开始界面
	Interface(screen, cfg, mode='game_start')
	# 游戏主循环
	font = pygame.font.SysFont('Consolas', 15)
	for gamemap_path in cfg.GAMEMAPPATHS:
		# -地图
		map_parser = mapParser(gamemap_path, bg_paths=cfg.BACKGROUNDPATHS, wall_paths=cfg.WALLPATHS, blocksize=cfg.BLOCKSIZE)
		# -水果
		fruit_sprite_group = pygame.sprite.Group()
		used_spaces = []
		for i in range(5):
			coordinate = map_parser.randomGetSpace(used_spaces)
			used_spaces.append(coordinate)
			fruit_sprite_group.add(Fruit(random.choice(cfg.FRUITPATHS), coordinate=coordinate, blocksize=cfg.BLOCKSIZE))
		# -我方Hero
		coordinate = map_parser.randomGetSpace(used_spaces)
		used_spaces.append(coordinate)
		ourhero = Hero(imagepaths=cfg.HEROZELDAPATHS, coordinate=coordinate, blocksize=cfg.BLOCKSIZE, map_parser=map_parser, hero_name='ZELDA')
		# -电脑Hero
		aihero_sprite_group = pygame.sprite.Group()
		coordinate = map_parser.randomGetSpace(used_spaces)
		aihero_sprite_group.add(Hero(imagepaths=cfg.HEROBATMANPATHS, coordinate=coordinate, blocksize=cfg.BLOCKSIZE, map_parser=map_parser, hero_name='BATMAN'))
		used_spaces.append(coordinate)
		coordinate = map_parser.randomGetSpace(used_spaces)
		aihero_sprite_group.add(Hero(imagepaths=cfg.HERODKPATHS, coordinate=coordinate, blocksize=cfg.BLOCKSIZE, map_parser=map_parser, hero_name='DK'))
		used_spaces.append(coordinate)
		# -炸弹bomb
		bomb_sprite_group = pygame.sprite.Group()
		# -用于判断游戏胜利或者失败的flag
		is_win_flag = False
		# -主循环
		screen = pygame.display.set_mode(map_parser.screen_size)
		clock = pygame.time.Clock()
		while True:
			dt = clock.tick(cfg.FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit(-1)
				# --↑↓←→键控制上下左右, 空格键丢炸弹
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP:
						ourhero.move('up')
					elif event.key == pygame.K_DOWN:
						ourhero.move('down')
					elif event.key == pygame.K_LEFT:
						ourhero.move('left')
					elif event.key == pygame.K_RIGHT:
						ourhero.move('right')
					elif event.key == pygame.K_SPACE:
						if ourhero.bomb_cooling_count <= 0:
							bomb_sprite_group.add(ourhero.generateBomb(imagepath=cfg.BOMBPATH, digitalcolor=cfg.YELLOW, explode_imagepath=cfg.FIREPATH))
			screen.fill(cfg.WHITE)
			# --电脑Hero随机行动
			for hero in aihero_sprite_group:
				action, flag = hero.randomAction(dt)
				if flag and action == 'dropbomb':
					bomb_sprite_group.add(hero.generateBomb(imagepath=cfg.BOMBPATH, digitalcolor=cfg.YELLOW, explode_imagepath=cfg.FIREPATH))
			# --吃到水果加生命值(只要是Hero, 都能加)
			ourhero.eatFruit(fruit_sprite_group)
			for hero in aihero_sprite_group:
				hero.eatFruit(fruit_sprite_group)
			# --游戏元素都绑定到屏幕上
			map_parser.draw(screen)
			for bomb in bomb_sprite_group:
				if not bomb.is_being:
					bomb_sprite_group.remove(bomb)
				explode_area = bomb.draw(screen, dt, map_parser)
				if explode_area:
					# --爆炸火焰范围内的Hero生命值将持续下降
					if ourhero.coordinate in explode_area:
						ourhero.health_value -= bomb.harm_value
					for hero in aihero_sprite_group:
						if hero.coordinate in explode_area:
							hero.health_value -= bomb.harm_value
			fruit_sprite_group.draw(screen)
			for hero in aihero_sprite_group:
				hero.draw(screen, dt)
			ourhero.draw(screen, dt)
			# --左上角显示生命值
			pos_x = showText(screen, font, text=ourhero.hero_name+'(our):'+str(ourhero.health_value), color=cfg.YELLOW, position=[5, 5])
			for hero in aihero_sprite_group:
				pos_x, pos_y = pos_x+15, 5
				pos_x = showText(screen, font, text=hero.hero_name+'(ai):'+str(hero.health_value), color=cfg.YELLOW, position=[pos_x, pos_y])
			# --我方玩家生命值小于等于0/电脑方玩家生命值均小于等于0则判断游戏结束
			if ourhero.health_value <= 0:
				is_win_flag = False
				break
			for hero in aihero_sprite_group:
				if hero.health_value <= 0:
					aihero_sprite_group.remove(hero)
			if len(aihero_sprite_group) == 0:
				is_win_flag = True
				break
			pygame.display.update()
			clock.tick(cfg.FPS)
		if is_win_flag:
			Interface(screen, cfg, mode='game_switch')
		else:
			break
	Interface(screen, cfg, mode='game_end')


'''run'''
if __name__ == '__main__':
	while True:
		main(cfg)