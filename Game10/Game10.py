'''
Function:
    飞机大战
作者:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import cfg
import pygame
from modules import *


'''游戏界面'''
def GamingInterface(num_player, screen):
    # 初始化
    pygame.mixer.music.load(cfg.SOUNDPATHS['Cool Space Music'])
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    explosion_sound = pygame.mixer.Sound(cfg.SOUNDPATHS['boom'])
    fire_sound = pygame.mixer.Sound(cfg.SOUNDPATHS['shot'])
    font = pygame.font.Font(cfg.FONTPATH, 20)
    # 游戏背景图
    bg_imgs = [cfg.IMAGEPATHS['bg_big'], cfg.IMAGEPATHS['seamless_space'], cfg.IMAGEPATHS['space3']]
    bg_move_dis = 0
    bg_1 = pygame.image.load(bg_imgs[0]).convert()
    bg_2 = pygame.image.load(bg_imgs[1]).convert()
    bg_3 = pygame.image.load(bg_imgs[2]).convert()
    # 玩家, 子弹和小行星精灵组
    player_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    asteroid_group = pygame.sprite.Group()
    # 产生小行星的时间间隔
    asteroid_ticks = 90
    for i in range(num_player):
        player_group.add(Ship(i+1, cfg))
    clock = pygame.time.Clock()
    # 分数
    score_1, score_2 = 0, 0
    # 游戏主循环
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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
            asteroid_group.add(Asteroid(cfg))
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
        clock.tick(60)


'''主函数'''
def main():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('飞机大战 —— Charles的皮卡丘')
    num_player = StartInterface(screen, cfg)
    if num_player == 1:
        while True:
            GamingInterface(num_player=1, screen=screen)
            EndInterface(screen, cfg)
    else:
        while True:
            GamingInterface(num_player=2, screen=screen)
            EndInterface(screen, cfg)


'''run'''
if __name__ == '__main__':
    main()