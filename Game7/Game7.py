'''
Function:
    仿谷歌浏览器小恐龙游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import cfg
import sys
import random
import pygame
from modules import *


'''main'''
def main(highest_score):
    # 游戏初始化
    pygame.init()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('T-Rex Rush —— Charles的皮卡丘')
    # 导入所有声音文件
    sounds = {}
    for key, value in cfg.AUDIO_PATHS.items():
        sounds[key] = pygame.mixer.Sound(value)
    # 游戏开始界面
    GameStartInterface(screen, sounds, cfg)
    # 定义一些游戏中必要的元素和变量
    score = 0
    score_board = Scoreboard(cfg.IMAGE_PATHS['numbers'], position=(534, 15), bg_color=cfg.BACKGROUND_COLOR)
    highest_score = highest_score
    highest_score_board = Scoreboard(cfg.IMAGE_PATHS['numbers'], position=(435, 15), bg_color=cfg.BACKGROUND_COLOR, is_highest=True)
    dino = Dinosaur(cfg.IMAGE_PATHS['dino'])
    ground = Ground(cfg.IMAGE_PATHS['ground'], position=(0, cfg.SCREENSIZE[1]))
    cloud_sprites_group = pygame.sprite.Group()
    cactus_sprites_group = pygame.sprite.Group()
    ptera_sprites_group = pygame.sprite.Group()
    add_obstacle_timer = 0
    score_timer = 0
    # 游戏主循环
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    dino.jump(sounds)
                elif event.key == pygame.K_DOWN:
                    dino.duck()
            elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                dino.unduck()
        screen.fill(cfg.BACKGROUND_COLOR)
        # --随机添加云
        if len(cloud_sprites_group) < 5 and random.randrange(0, 300) == 10:
            cloud_sprites_group.add(Cloud(cfg.IMAGE_PATHS['cloud'], position=(cfg.SCREENSIZE[0], random.randrange(30, 75))))
        # --随机添加仙人掌/飞龙
        add_obstacle_timer += 1
        if add_obstacle_timer > random.randrange(50, 150):
            add_obstacle_timer = 0
            random_value = random.randrange(0, 10)
            if random_value >= 5 and random_value <= 7:
                cactus_sprites_group.add(Cactus(cfg.IMAGE_PATHS['cacti']))
            else:
                position_ys = [cfg.SCREENSIZE[1]*0.82, cfg.SCREENSIZE[1]*0.75, cfg.SCREENSIZE[1]*0.60, cfg.SCREENSIZE[1]*0.20]
                ptera_sprites_group.add(Ptera(cfg.IMAGE_PATHS['ptera'], position=(600, random.choice(position_ys))))
        # --更新游戏元素
        dino.update()
        ground.update()
        cloud_sprites_group.update()
        cactus_sprites_group.update()
        ptera_sprites_group.update()
        score_timer += 1
        if score_timer > (cfg.FPS//12):
            score_timer = 0
            score += 1
            score = min(score, 99999)
            if score > highest_score:
                highest_score = score
            if score % 100 == 0:
                sounds['point'].play()
            if score % 1000 == 0:
                ground.speed -= 1
                for item in cloud_sprites_group:
                    item.speed -= 1
                for item in cactus_sprites_group:
                    item.speed -= 1
                for item in ptera_sprites_group:
                    item.speed -= 1
        # --碰撞检测
        for item in cactus_sprites_group:
            if pygame.sprite.collide_mask(dino, item):
                dino.die(sounds)
        for item in ptera_sprites_group:
            if pygame.sprite.collide_mask(dino, item):
                dino.die(sounds)
        # --将游戏元素画到屏幕上
        dino.draw(screen)
        ground.draw(screen)
        cloud_sprites_group.draw(screen)
        cactus_sprites_group.draw(screen)
        ptera_sprites_group.draw(screen)
        score_board.set(score)
        highest_score_board.set(highest_score)
        score_board.draw(screen)
        highest_score_board.draw(screen)
        # --更新屏幕
        pygame.display.update()
        clock.tick(cfg.FPS)
        # --游戏是否结束
        if dino.is_dead:
            break
    # 游戏结束界面
    return GameEndInterface(screen, cfg), highest_score


'''run'''
if __name__ == '__main__':
    highest_score = 0
    while True:
        flag, highest_score = main(highest_score)
        if not flag: break