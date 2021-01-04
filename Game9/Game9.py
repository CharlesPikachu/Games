'''
Function:
    接金币小游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import cfg
import sys
import pygame
import random
from modules import *


'''游戏初始化'''
def initGame():
    # 初始化pygame, 设置展示窗口
    pygame.init()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('catch coins —— Charles的皮卡丘')
    # 加载必要的游戏素材
    game_images = {}
    for key, value in cfg.IMAGE_PATHS.items():
        if isinstance(value, list):
            images = []
            for item in value: images.append(pygame.image.load(item))
            game_images[key] = images
        else:
            game_images[key] = pygame.image.load(value)
    game_sounds = {}
    for key, value in cfg.AUDIO_PATHS.items():
        if key == 'bgm': continue
        game_sounds[key] = pygame.mixer.Sound(value)
    # 返回初始化数据
    return screen, game_images, game_sounds


'''主函数'''
def main():
    # 初始化
    screen, game_images, game_sounds = initGame()
    # 播放背景音乐
    pygame.mixer.music.load(cfg.AUDIO_PATHS['bgm'])
    pygame.mixer.music.play(-1, 0.0)
    # 字体加载
    font = pygame.font.Font(cfg.FONT_PATH, 40)
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
                pygame.quit()
                sys.exit()
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
    return showEndGameInterface(screen, cfg, score, highest_score)


'''run'''
if __name__ == '__main__':
    while main():
        pass