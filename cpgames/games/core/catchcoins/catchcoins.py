'''
Function:
    接金币小游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import pygame
import random
from ...utils import QuitGame
from ..base import PygameBaseGame
from .modules import Hero, Food, ShowEndGameInterface


'''配置类'''
class Config():
    # 根目录
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # 标题
    TITLE = '接金币 —— Charles的皮卡丘'
    # FPS
    FPS = 30
    # 屏幕大小
    SCREENSIZE = (800, 600)
    # 背景颜色
    BACKGROUND_COLOR = (0, 160, 233)
    # 最高分记录的路径
    HIGHEST_SCORE_RECORD_FILEPATH = os.path.join(rootdir, 'highest.rec')
    # 游戏图片路径
    IMAGE_PATHS_DICT = {
        'gold': os.path.join(rootdir, 'resources/images/gold.png'),
        'apple': os.path.join(rootdir, 'resources/images/apple.png'),
        'background': os.path.join(rootdir, 'resources/images/background.jpg'),
        'hero': [],
    }
    for i in range(1, 11):
        IMAGE_PATHS_DICT['hero'].append(os.path.join(rootdir, 'resources/images/%d.png' % i))
    # 背景音乐路径
    BGM_PATH = os.path.join(rootdir, 'resources/audios/bgm.mp3')
     # 游戏声音路径
    SOUND_PATHS_DICT = {
        'get': os.path.join(rootdir, 'resources/audios/get.wav'),
    }
    # 字体路径
    FONT_PATHS_DICT = {
        'default_s': {'name': os.path.join(rootdir.replace('catchcoins', 'base'), 'resources/fonts/Gabriola.ttf'), 'size': 40},
        'default_l': {'name': os.path.join(rootdir.replace('catchcoins', 'base'), 'resources/fonts/Gabriola.ttf'), 'size': 60},
    }


'''接金币小游戏'''
class CatchCoinsGame(PygameBaseGame):
    game_type = 'catchcoins'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(CatchCoinsGame, self).__init__(config=self.cfg, **kwargs)
    '''运行游戏'''
    def run(self):
        flag = True
        while flag:
            # 初始化
            screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
            game_images, game_sounds = resource_loader.images, resource_loader.sounds
            # 播放背景音乐
            resource_loader.playbgm()
            # 字体加载
            font = resource_loader.fonts['default_s']
            # 定义hero
            hero = Hero(game_images['hero'], position=(375, 520))
            # 定义食物组
            food_sprites_group = pygame.sprite.Group()
            generate_food_freq = random.randint(10, 20)
            generate_food_count = 0
            # 当前分数/历史最高分
            score = 0
            highest_score = 0 if not os.path.exists(cfg.HIGHEST_SCORE_RECORD_FILEPATH) else int(open(cfg.HIGHEST_SCORE_RECORD_FILEPATH).read())
            # 游戏主循环
            clock = pygame.time.Clock()
            while True:
                # --填充背景
                screen.fill(0)
                screen.blit(game_images['background'], (0, 0))
                # --倒计时信息
                countdown_text = 'Count down: ' + str((90000 - pygame.time.get_ticks()) // 60000) + ":" + str((90000 - pygame.time.get_ticks()) // 1000 % 60).zfill(2)
                countdown_text = font.render(countdown_text, True, (0, 0, 0))
                countdown_rect = countdown_text.get_rect()
                countdown_rect.topright = [cfg.SCREENSIZE[0]-30, 5]
                screen.blit(countdown_text, countdown_rect)
                # --按键检测
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        QuitGame()
                key_pressed = pygame.key.get_pressed()
                if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
                    hero.move(cfg.SCREENSIZE, 'left')
                if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
                    hero.move(cfg.SCREENSIZE, 'right')
                # --随机生成食物
                generate_food_count += 1
                if generate_food_count > generate_food_freq:
                    generate_food_freq = random.randint(10, 20)
                    generate_food_count = 0
                    food = Food(game_images, random.choice(['gold',] * 10 + ['apple']), cfg.SCREENSIZE)
                    food_sprites_group.add(food)
                # --更新食物
                for food in food_sprites_group:
                    if food.update(): food_sprites_group.remove(food)
                # --碰撞检测
                for food in food_sprites_group:
                    if pygame.sprite.collide_mask(food, hero):
                        game_sounds['get'].play()
                        food_sprites_group.remove(food)
                        score += food.score
                        if score > highest_score: highest_score = score
                # --画hero
                hero.draw(screen)
                # --画食物
                food_sprites_group.draw(screen)
                # --显示得分
                score_text = f'Score: {score}, Highest: {highest_score}'
                score_text = font.render(score_text, True, (0, 0, 0))
                score_rect = score_text.get_rect()
                score_rect.topleft = [5, 5]
                screen.blit(score_text, score_rect)
                # --判断游戏是否结束
                if pygame.time.get_ticks() >= 90000:
                    break
                # --更新屏幕
                pygame.display.flip()
                clock.tick(cfg.FPS)
            # 游戏结束, 记录最高分并显示游戏结束画面
            fp = open(cfg.HIGHEST_SCORE_RECORD_FILEPATH, 'w')
            fp.write(str(highest_score))
            fp.close()
            flag = ShowEndGameInterface(screen, cfg, score, highest_score, resource_loader)