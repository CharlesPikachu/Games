'''
Function:
    打地鼠(Whac-A-Mole)小游戏
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
from .modules import Mole, Hammer, endInterface, startInterface


'''配置类'''
class Config():
    # 根目录
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # FPS
    FPS = 100
    # 屏幕大小
    SCREENSIZE = (993, 477)
    # 标题
    TITLE = '打地鼠 —— Charles的皮卡丘'
    # 游戏常量参数
    HOLE_POSITIONS = [(90, -20), (405, -20), (720, -20), (90, 140), (405, 140), (720, 140), (90, 290), (405, 290), (720, 290)]
    BROWN = (150, 75, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    RECORD_PATH = os.path.join(rootdir, 'score.rec')
    # 背景音乐路径
    BGM_PATH = os.path.join(rootdir, 'resources/audios/bgm.mp3')
    # 游戏声音路径
    SOUND_PATHS_DICT = {
        'count_down': os.path.join(rootdir, 'resources/audios/count_down.wav'),
        'hammering': os.path.join(rootdir, 'resources/audios/hammering.wav'),
    }
    # 字体路径
    FONT_PATH = os.path.join(rootdir.replace('whacamole', 'base'), 'resources/fonts/Gabriola.ttf')
    # 游戏图片路径
    IMAGE_PATHS_DICT = {
        'hammer': [os.path.join(rootdir, 'resources/images/hammer0.png'), os.path.join(rootdir, 'resources/images/hammer1.png')],
        'begin': [os.path.join(rootdir, 'resources/images/begin.png'), os.path.join(rootdir, 'resources/images/begin1.png')],
        'again': [os.path.join(rootdir, 'resources/images/again1.png'), os.path.join(rootdir, 'resources/images/again2.png')],
        'background': os.path.join(rootdir, 'resources/images/background.png'),
        'end': os.path.join(rootdir, 'resources/images/end.png'),
        'mole': [
            os.path.join(rootdir, 'resources/images/mole_1.png'), os.path.join(rootdir, 'resources/images/mole_laugh1.png'),
            os.path.join(rootdir, 'resources/images/mole_laugh2.png'), os.path.join(rootdir, 'resources/images/mole_laugh3.png')
        ]
    }


'''打地鼠(Whac-A-Mole)小游戏'''
class WhacAMoleGame(PygameBaseGame):
    game_type = 'whacamole'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(WhacAMoleGame, self).__init__(config=self.cfg, **kwargs)
    '''运行游戏'''
    def run(self):
        # 初始化
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg 
        while True:
            is_restart = self.GamingInterface(screen, resource_loader, cfg)
            if not is_restart:
                break 
    '''游戏进行界面'''
    def GamingInterface(self, screen, resource_loader, cfg):
        # 播放背景音乐
        resource_loader.playbgm()
        audios = resource_loader.sounds
        # 加载字体
        font = pygame.font.Font(cfg.FONT_PATH, 40)
        # 加载背景图片
        bg_img = resource_loader.images['background']
        # 开始界面
        startInterface(screen, resource_loader.images['begin'])
        # 地鼠改变位置的计时
        hole_pos = random.choice(cfg.HOLE_POSITIONS)
        change_hole_event = pygame.USEREVENT
        pygame.time.set_timer(change_hole_event, 800)
        # 地鼠
        mole = Mole(resource_loader.images['mole'], hole_pos)
        # 锤子
        hammer = Hammer(resource_loader.images['hammer'], (500, 250))
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
                    QuitGame()
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
        is_restart = endInterface(screen, resource_loader.images['end'], resource_loader.images['again'], score_info, cfg.FONT_PATH, [cfg.WHITE, cfg.RED], cfg.SCREENSIZE)
        return is_restart