'''
Function:
    打地鼠(Whac-A-Mole)小游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import cfg
import sys
import pygame
import random
from modules import *


'''游戏初始化'''
def initGame():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('打地鼠 —— Charles的皮卡丘')
    return screen


'''主函数'''
def main():
    # 初始化
    screen = initGame()
    # 加载背景音乐和其他音效
    pygame.mixer.music.load(cfg.BGM_PATH)
    pygame.mixer.music.play(-1)
    audios = {
        'count_down': pygame.mixer.Sound(cfg.COUNT_DOWN_SOUND_PATH),
        'hammering': pygame.mixer.Sound(cfg.HAMMERING_SOUND_PATH)
    }
    # 加载字体
    font = pygame.font.Font(cfg.FONT_PATH, 40)
    # 加载背景图片
    bg_img = pygame.image.load(cfg.GAME_BG_IMAGEPATH)
    # 开始界面
    startInterface(screen, cfg.GAME_BEGIN_IMAGEPATHS)
    # 地鼠改变位置的计时
    hole_pos = random.choice(cfg.HOLE_POSITIONS)
    change_hole_event = pygame.USEREVENT
    pygame.time.set_timer(change_hole_event, 800)
    # 地鼠
    mole = Mole(cfg.MOLE_IMAGEPATHS, hole_pos)
    # 锤子
    hammer = Hammer(cfg.HAMMER_IMAGEPATHS, (500, 250))
    # 时钟
    clock = pygame.time.Clock()
    # 分数
    your_score = 0
    flag = False
    # 初始时间
    init_time = pygame.time.get_ticks()
    # 游戏主循环
    while True:
        # --游戏时间为60s
        time_remain = round((61000 - (pygame.time.get_ticks() - init_time)) / 1000.)
        # --游戏时间减少, 地鼠变位置速度变快
        if time_remain == 40 and not flag:
            hole_pos = random.choice(cfg.HOLE_POSITIONS)
            mole.reset()
            mole.setPosition(hole_pos)
            pygame.time.set_timer(change_hole_event, 650)
            flag = True
        elif time_remain == 20 and flag:
            hole_pos = random.choice(cfg.HOLE_POSITIONS)
            mole.reset()
            mole.setPosition(hole_pos)
            pygame.time.set_timer(change_hole_event, 500)
            flag = False
        # --倒计时音效
        if time_remain == 10:
            audios['count_down'].play()
        # --游戏结束
        if time_remain < 0: break
        count_down_text = font.render('Time: '+str(time_remain), True, cfg.WHITE)
        # --按键检测
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                hammer.setPosition(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    hammer.setHammering()
            elif event.type == change_hole_event:
                hole_pos = random.choice(cfg.HOLE_POSITIONS)
                mole.reset()
                mole.setPosition(hole_pos)
        # --碰撞检测
        if hammer.is_hammering and not mole.is_hammer:
            is_hammer = pygame.sprite.collide_mask(hammer, mole)
            if is_hammer:
                audios['hammering'].play()
                mole.setBeHammered()
                your_score += 10
        # --分数
        your_score_text = font.render('Score: '+str(your_score), True, cfg.BROWN)
        # --绑定必要的游戏元素到屏幕(注意顺序)
        screen.blit(bg_img, (0, 0))
        screen.blit(count_down_text, (875, 8))
        screen.blit(your_score_text, (800, 430))
        mole.draw(screen)
        hammer.draw(screen)
        # --更新
        pygame.display.flip()
        clock.tick(60)
    # 读取最佳分数(try块避免第一次游戏无.rec文件)
    try:
        best_score = int(open(cfg.RECORD_PATH).read())
    except:
        best_score = 0
    # 若当前分数大于最佳分数则更新最佳分数
    if your_score > best_score:
        f = open(cfg.RECORD_PATH, 'w')
        f.write(str(your_score))
        f.close()
    # 结束界面
    score_info = {'your_score': your_score, 'best_score': best_score}
    is_restart = endInterface(screen, cfg.GAME_END_IMAGEPATH, cfg.GAME_AGAIN_IMAGEPATHS, score_info, cfg.FONT_PATH, [cfg.WHITE, cfg.RED], cfg.SCREENSIZE)
    return is_restart


'''run'''
if __name__ == '__main__':
    while True:
        is_restart = main()
        if not is_restart:
            break