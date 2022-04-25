'''
Function:
    飞机大战
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import pygame
from ...utils import QuitGame
from ..base import PygameBaseGame
from .modules import Bullet, Ship, Asteroid, StartInterface, EndInterface


'''配置类'''
class Config():
    # 根目录
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # FPS
    FPS = 60
    # 屏幕大小
    SCREENSIZE = (956, 560)
    # 标题
    TITLE = '飞机大战 —— Charles的皮卡丘'
    # 游戏声音路径
    SOUND_PATHS_DICT = {
        'boom': os.path.join(rootdir, 'resources/audios/boom.wav'),
        'shot': os.path.join(rootdir, 'resources/audios/shot.ogg'),
    }
    # 背景音乐路径
    BGM_PATH = os.path.join(rootdir, 'resources/audios/Cool Space Music.mp3')
    # 游戏图片路径
    IMAGE_PATHS_DICT = {
        'asteroid': os.path.join(rootdir, 'resources/images/asteroid.png'),
        'bg_big': os.path.join(rootdir, 'resources/images/bg_big.png'),
        'bullet': os.path.join(rootdir, 'resources/images/bullet.png'),
        'seamless_space': os.path.join(rootdir, 'resources/images/seamless_space.png'),
        'ship': os.path.join(rootdir, 'resources/images/ship.png'),
        'ship_exploded': os.path.join(rootdir, 'resources/images/ship_exploded.png'),
        'space3': os.path.join(rootdir, 'resources/images/space3.jpg'),
    }
    # 字体路径
    FONT_PATHS_DICT = {
        'default_s': {'name': os.path.join(rootdir.replace('aircraftwar', 'base'), 'resources/fonts/simkai.ttf'), 'size': 20},
        'default_l': {'name': os.path.join(rootdir.replace('aircraftwar', 'base'), 'resources/fonts/simkai.ttf'), 'size': 50},
    }


'''飞机大战'''
class AircraftWarGame(PygameBaseGame):
    game_type = 'aircraftwar'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(AircraftWarGame, self).__init__(config=self.cfg, **kwargs)
    '''运行游戏'''
    def run(self):
        # 初始化
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
        # 游戏开始界面
        num_player = StartInterface(screen, cfg, resource_loader)
        # 开始游戏
        if num_player == 1:
            while True:
                self.GamingInterface(num_player=1, screen=screen)
                EndInterface(screen, cfg, resource_loader)
        else:
            while True:
                self.GamingInterface(num_player=2, screen=screen)
                EndInterface(screen, cfg, resource_loader)
    '''游戏界面'''
    def GamingInterface(self, num_player, screen):
        # 初始化
        self.resource_loader.playbgm()
        explosion_sound = self.resource_loader.sounds['boom']
        fire_sound = self.resource_loader.sounds['shot']
        font = self.resource_loader.fonts['default_s']
        # 游戏背景图
        bg_move_dis = 0
        bg_1 = self.resource_loader.images['bg_big'].convert()
        bg_2 = self.resource_loader.images['seamless_space'].convert()
        bg_3 = self.resource_loader.images['space3'].convert()
        # 玩家, 子弹和小行星精灵组
        player_group = pygame.sprite.Group()
        bullet_group = pygame.sprite.Group()
        asteroid_group = pygame.sprite.Group()
        # 产生小行星的时间间隔
        asteroid_ticks = 90
        for i in range(num_player):
            player_group.add(Ship(i+1, self.cfg, self.resource_loader))
        clock = pygame.time.Clock()
        # 分数
        score_1, score_2 = 0, 0
        # 游戏主循环
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
            # --玩家一: ↑↓←→控制, j射击; 玩家二: wsad控制, 空格射击
            pressed_keys = pygame.key.get_pressed()
            for idx, player in enumerate(player_group):
                direction = None
                if idx == 0:
                    if pressed_keys[pygame.K_UP]:
                        direction = 'up'
                    elif pressed_keys[pygame.K_DOWN]:
                        direction = 'down'
                    elif pressed_keys[pygame.K_LEFT]:
                        direction = 'left'
                    elif pressed_keys[pygame.K_RIGHT]:
                        direction = 'right'
                    if direction:
                        player.move(direction)
                    if pressed_keys[pygame.K_j]:
                        if player.cooling_time == 0:
                            fire_sound.play()
                            bullet_group.add(player.shot())
                            player.cooling_time = 20
                elif idx == 1:
                    if pressed_keys[pygame.K_w]:
                        direction = 'up'
                    elif pressed_keys[pygame.K_s]:
                        direction = 'down'
                    elif pressed_keys[pygame.K_a]:
                        direction = 'left'
                    elif pressed_keys[pygame.K_d]:
                        direction = 'right'
                    if direction:
                        player.move(direction)
                    if pressed_keys[pygame.K_SPACE]:
                        if player.cooling_time == 0:
                            fire_sound.play()
                            bullet_group.add(player.shot())
                            player.cooling_time = 20
                if player.cooling_time > 0:
                    player.cooling_time -= 1
            if (score_1 + score_2) < 500:
                background = bg_1
            elif (score_1 + score_2) < 1500:
                background = bg_2
            else:
                background = bg_3
            # --向下移动背景图实现飞船向上移动的效果
            screen.blit(background, (0, -background.get_rect().height + bg_move_dis))
            screen.blit(background, (0, bg_move_dis))
            bg_move_dis = (bg_move_dis + 2) % background.get_rect().height
            # --生成小行星
            if asteroid_ticks == 0:
                asteroid_ticks = 90
                asteroid_group.add(Asteroid(self.cfg, self.resource_loader))
            else:
                asteroid_ticks -= 1
            # --画飞船
            for player in player_group:
                if pygame.sprite.spritecollide(player, asteroid_group, True, None):
                    player.explode_step = 1
                    explosion_sound.play()
                elif player.explode_step > 0:
                    if player.explode_step > 3:
                        player_group.remove(player)
                        if len(player_group) == 0:
                            return
                    else:
                        player.explode(screen)
                else:
                    player.draw(screen)
            # --画子弹
            for bullet in bullet_group:
                bullet.move()
                if pygame.sprite.spritecollide(bullet, asteroid_group, True, None):
                    bullet_group.remove(bullet)
                    if bullet.player_idx == 1:
                        score_1 += 1
                    else:
                        score_2 += 1
                else:
                    bullet.draw(screen)
            # --画小行星
            for asteroid in asteroid_group:
                asteroid.move()
                asteroid.rotate()
                asteroid.draw(screen)
            # --显示分数
            score_1_text = '玩家一得分: %s' % score_1
            score_2_text = '玩家二得分: %s' % score_2
            text_1 = font.render(score_1_text, True, (0, 0, 255))
            text_2 = font.render(score_2_text, True, (255, 0, 0))
            screen.blit(text_1, (2, 5))
            screen.blit(text_2, (2, 35))
            # --屏幕刷新
            pygame.display.update()
            clock.tick(self.cfg.FPS)