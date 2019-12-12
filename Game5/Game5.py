'''
Function:
	经典坦克大战小游戏
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import os
import cfg
import pygame
from modules import *


'''主函数'''
def main(cfg):
	# 游戏初始化
	pygame.init()
	pygame.mixer.init()
	screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
	pygame.display.set_caption(cfg.TITLE)
	# 加载游戏素材
	sounds = {}
	for key, value in cfg.AUDIO_PATHS.items():
		sounds[key] = pygame.mixer.Sound(value)
		sounds[key].set_volume(1)
	# 开始界面
	is_dual_mode = gameStartInterface(screen, cfg)
	# 关卡数
	levelfilepaths = [os.path.join(cfg.LEVELFILEDIR, filename) for filename in sorted(os.listdir(cfg.LEVELFILEDIR))]
	# 主循环
	for idx, levelfilepath in enumerate(levelfilepaths):
		switchLevelIterface(screen, cfg, idx+1)
		game_level = GameLevel(levelfilepath, sounds, is_dual_mode, cfg)
		is_win = game_level.start(screen)
		if not is_win: break
	gameEndIterface(screen, cfg, is_win)


'''run'''
if __name__ == '__main__':
	main(cfg)