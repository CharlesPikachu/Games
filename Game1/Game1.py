'''
Function:
    Bunnies and Badgers
Author: 
    Charles
Test
'''
import sys
import cfg
import math
import random
import pygame
from modules import *


'''游戏初始化'''
def initGame():
    # 初始化pygame, 设置展示窗口
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('Bunnies and Badgers —— Charles的皮卡丘')
    # 加载必要的游戏素材
    game_images = {}
    for key, value in cfg.IMAGE_PATHS.items():
        game_images[key] = pygame.image.load(value)
    game_sounds = {}
    for key, value in cfg.SOUNDS_PATHS.items():
        if key != 'moonlight':
            game_sounds[key] = pygame.mixer.Sound(value)
    return screen, game_images, game_sounds


'''主函数'''
def main():
    # 初始化
    screen, game_images, game_sounds = initGame()
    # 播放背景音乐
    pygame.mixer.music.load(cfg.SOUNDS_PATHS['moonlight'])
    pygame.mixer.music.play(-1, 0.0)
    # 字体加载
    font = pygame.font.Font(None, 24)
    # 定义兔子
    bunny = BunnySprite(image=game_images.get('rabbit'), position=(100, 100))
    # 跟踪玩家的精度变量, 记录了射出的箭头数和被击中的獾的数量.
    acc_record = [0., 0.]
    # 生命值
    healthvalue = 194
    # 弓箭
    arrow_sprites_group = pygame.sprite.Group()
    # 獾
    badguy_sprites_group = pygame.sprite.Group()
    badguy = BadguySprite(game_images.get('badguy'), position=(640, 100))
    badguy_sprites_group.add(badguy)
    # 定义了一个定时器, 使得游戏里经过一段时间后就新建一支獾
    badtimer = 100
    badtimer1 = 0
    # 游戏主循环, running变量会跟踪游戏是否结束, exitcode变量会跟踪玩家是否胜利.
    running, exitcode = True, False
    clock = pygame.time.Clock()
    while running:
        # --在给屏幕画任何东西之前用黑色进行填充
        screen.fill(0)
        # --添加的风景也需要画在屏幕上
        for x in range(cfg.SCREENSIZE[0]//game_images['grass'].get_width()+1):
            for y in range(cfg.SCREENSIZE[1]//game_images['grass'].get_height()+1):
                screen.blit(game_images['grass'], (x*100, y*100))
        for i in range(4): screen.blit(game_images['castle'], (0, 30+105*i))
        # --倒计时信息
        countdown_text = font.render(str((90000-pygame.time.get_ticks())//60000)+":"+str((90000-pygame.time.get_ticks())//1000%60).zfill(2), True, (0, 0, 0))
        countdown_rect = countdown_text.get_rect()
        countdown_rect.topright = [635, 5]
        screen.blit(countdown_text, countdown_rect)
        # --按键检测
        # ----退出与射击
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game_sounds['shoot'].play()
                acc_record[1] += 1
                mouse_pos = pygame.mouse.get_pos()
                angle = math.atan2(mouse_pos[1]-(bunny.rotated_position[1]+32), mouse_pos[0]-(bunny.rotated_position[0]+26))
                arrow = ArrowSprite(game_images.get('arrow'), (angle, bunny.rotated_position[0]+32, bunny.rotated_position[1]+26))
                arrow_sprites_group.add(arrow)
        # ----移动兔子
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w]:
            bunny.move(cfg.SCREENSIZE, 'up')
        elif key_pressed[pygame.K_s]:
            bunny.move(cfg.SCREENSIZE, 'down')
        elif key_pressed[pygame.K_a]:
            bunny.move(cfg.SCREENSIZE, 'left')
        elif key_pressed[pygame.K_d]:
            bunny.move(cfg.SCREENSIZE, 'right')
        # --更新弓箭
        for arrow in arrow_sprites_group:
            if arrow.update(cfg.SCREENSIZE):
                arrow_sprites_group.remove(arrow)
        # --更新獾
        if badtimer == 0:
            badguy = BadguySprite(game_images.get('badguy'), position=(640, random.randint(50, 430)))
            badguy_sprites_group.add(badguy)
            badtimer = 100 - (badtimer1 * 2)
            badtimer1 = 20 if badtimer1>=20 else badtimer1+2
        badtimer -= 1
        for badguy in badguy_sprites_group:
            if badguy.update():
                game_sounds['hit'].play()
                healthvalue -= random.randint(4, 8)
                badguy_sprites_group.remove(badguy)
        # --碰撞检测
        for arrow in arrow_sprites_group:
            for badguy in badguy_sprites_group:
                if pygame.sprite.collide_mask(arrow, badguy):
                    game_sounds['enemy'].play()
                    arrow_sprites_group.remove(arrow)
                    badguy_sprites_group.remove(badguy)
                    acc_record[0] += 1
        # --画出弓箭
        arrow_sprites_group.draw(screen)
        # --画出獾
        badguy_sprites_group.draw(screen)
        # --画出兔子
        bunny.draw(screen, pygame.mouse.get_pos())
        # --画出城堡健康值, 首先画了一个全红色的生命值条, 然后根据城堡的生命值往生命条里面添加绿色.
        screen.blit(game_images.get('healthbar'), (5, 5))
        for i in range(healthvalue):
            screen.blit(game_images.get('health'), (i+8, 8))
        # --判断游戏是否结束
        if pygame.time.get_ticks() >= 90000:
            running, exitcode = False, True
        if healthvalue <= 0:
            running, exitcode = False, False
        # --更新屏幕
        pygame.display.flip()
        clock.tick(cfg.FPS)
    # 计算准确率
    accuracy = acc_record[0] / acc_record[1] * 100 if acc_record[1] > 0 else 0
    accuracy = '%.2f' % accuracy
    showEndGameInterface(screen, exitcode, accuracy, game_images)


'''run'''
if __name__ == '__main__':
    main()