'''
Function:
    魔塔小游戏主要逻辑实现
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import pygame
from .sprites import Hero
from .maps import MapParser


'''魔塔小游戏主要逻辑实现'''
class GameLevels():
    def __init__(self, cfg):
        self.cfg = cfg
        # 加载游戏地图中的所有图片
        self.map_element_images = {}
        for key, value in self.cfg.MAPELEMENTSPATHS.items():
            self.map_element_images[key] = [
                pygame.image.load(value[0]),
                pygame.image.load(value[1]),
            ]
        # 加载游戏背景图片
        self.background_images = {}
        for key, value in cfg.BACKGROUNDPATHS.items():
            if key == 'gamebg':
                self.background_images[key] = pygame.transform.scale(pygame.image.load(value), cfg.SCREENSIZE)
            elif key == 'battlebg':
                self.background_images[key] = pygame.transform.scale(pygame.image.load(value), (932, 407))
            else:
                self.background_images[key] = pygame.image.load(value)
        # 游戏地图解析类
        self.map_level_pointer = 0
        self.loadmap()
        # 英雄类
        self.hero = Hero(
            imagepaths=cfg.HEROPATHS,
            blocksize=cfg.BLOCKSIZE,
            block_position=self.map_parser.getheroposition(),
            offset=(325, 55),
            fontpath=cfg.FONTPATH_CN,
            background_images=self.background_images,
            cfg=cfg,
        )
    '''导入地图'''
    def loadmap(self):
        self.map_parser = MapParser(
            blocksize=self.cfg.BLOCKSIZE, 
            filepath=self.cfg.MAPPATHS[self.map_level_pointer], 
            element_images=self.map_element_images,
            offset=(325, 55),
        )
    '''运行'''
    def run(self, screen):
        # 游戏主循环
        clock, is_running = pygame.time.Clock(), True
        while is_running:
            screen.fill((0, 0, 0))
            screen.blit(self.background_images['gamebg'], (0, 0))
            # --按键检测
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            key_pressed = pygame.key.get_pressed()
            move_events = []
            if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
                move_events = self.hero.move('up', self.map_parser, screen)
            elif key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
                move_events = self.hero.move('down', self.map_parser, screen)
            elif key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
                move_events = self.hero.move('left', self.map_parser, screen)
            elif key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
                move_events = self.hero.move('right', self.map_parser, screen)
            if not move_events: move_events = []
            # --画游戏地图
            self.map_parser.draw(screen)
            # --左侧面板栏
            font = pygame.font.Font(self.cfg.FONTPATH_CN, 20)
            font_renders = [
                self.hero.font.render(str(self.map_level_pointer), True, (255, 255, 255)),
                font.render('游戏时间: ' + str(pygame.time.get_ticks() // 60000) + ' 分 ' + str(pygame.time.get_ticks() // 1000 % 60) + ' 秒', True, (255, 255, 255)),
            ]
            rects = [fr.get_rect() for fr in font_renders]
            rects[0].topleft = (150, 530)
            rects[1].topleft = (75, 630)
            for fr, rect in zip(font_renders, rects):
                screen.blit(fr, rect)
            # --画英雄
            self.hero.draw(screen)
            self.hero.cur_scenes = [
                [font_renders[0], rects[0]], [font_renders[1], rects[1]]
            ]
            # --触发游戏事件
            for event in move_events:
                if event == 'upstairs':
                    self.map_level_pointer += 1
                    self.loadmap()
                    self.hero.placenexttostairs(self.map_parser, 'down')
                elif event == 'downstairs':
                    self.map_level_pointer -= 1
                    self.loadmap()
                    self.hero.placenexttostairs(self.map_parser, 'up')
                elif event == 'conversation_hero_and_fairy':
                    self.showconversationheroandfairy(screen, self.hero.cur_scenes)
            # --刷新
            pygame.display.flip()
            clock.tick(self.cfg.FPS)
    '''仙女和勇士对话'''
    def showconversationheroandfairy(self, screen, scenes):
        # 对话框指针
        conversation_pointer = 0
        # 定义所有对话
        conversations = [
            ['......'], 
            ['你醒了!'], 
            ['......', '你是谁? 我在哪里?'],
            ['我是这里的仙子, 刚才你被这里的', '小怪打晕了.'],
            ['......', '剑, 剑, 我的剑呢?'],
            ['你的剑被他们抢走了, 我只来得及', '将你救出来.'],
            ['那, 公主呢? 我是来救公主的.'],
            ['公主还在里面, 你这样进去是打不', '过里面的小怪的.'],
            ['那我怎么办, 我答应了国王一定要', '把公主救出来的，那我现在应该怎', '么办呢?'],
            ['放心吧, 我把我的力量借给你, 你', '就可以打赢那些小怪了. 不过, 你', '得先去帮我去找一样东西，找到', '了再来这里找我.'],
            ['找东西? 找什么东西?'],
            ['是一个十字架, 中间有一颗红色的', '宝石.'],
            ['那个东西有什么用吗?'],
            ['我本是这座塔守护者, 可不久前, ', '从北方来了一批恶魔, 他们占领了', '这座塔，并将我的魔力封在了这', '个十字架里面, 如果你能将它带出', '塔来, 那我的魔力便会慢慢地恢复, ', '到那时我便可以把力量借给你去', '救公主了. 要记住, 只有用我的魔力', '才可以打开二十一层的门.'],
            ['......', '好吧，我试试看'],
            ['刚才我去看过了, 你的剑被放在三', '楼, 你的盾在五楼上, 而那个十字', '架被放在七楼. 要到七楼, 你得', '先取回你的剑和盾. 另外在塔里的', '其他楼层上, 还有一些存放了好几百', '年的宝剑和宝物，如果得到它们,', '对于你对付这里面的怪物将有很大', '的帮助.'],
            ['可是, 我怎么进去呢?'],
            ['我这里有三把钥匙, 你先拿去, 在', '塔里面还有很多这样的钥匙, 你一', '定要珍惜使用. 勇敢的去吧，勇士!']
        ]
        # 主循环
        clock = pygame.time.Clock()
        font = pygame.font.Font(self.cfg.FONTPATH_CN, 20)
        while True:
            screen.fill((0, 0, 0))
            screen.blit(self.background_images['gamebg'], (0, 0))
            self.map_parser.draw(screen)
            for scene in scenes:
                screen.blit(scene[0], scene[1])
            self.hero.draw(screen)
            # --按键检测
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        conversation_pointer += 1
                        if conversation_pointer >= len(conversations): return
            # --画对话框
            conversation = conversations[conversation_pointer]
            # ----勇士
            if conversation_pointer % 2 == 0:
                left, top, width, height = 510, 430, 7, 2
                pygame.draw.rect(screen, (199, 97, 20), (left - 4, top - 4, self.cfg.BLOCKSIZE * width + 8, self.cfg.BLOCKSIZE * height + 8), 7)
                id_image = self.hero.images['down']
            # ----仙子
            else:
                left, top, width, height = 300, 250, 7, 2
                if len(conversation) > 3: height = 3
                if len(conversation) > 5: height = 4
                if len(conversation) > 7: height = 5
                pygame.draw.rect(screen, (199, 97, 20), (left - 4, top - 4, self.cfg.BLOCKSIZE * width + 8, self.cfg.BLOCKSIZE * height + 8), 7)
                id_image = pygame.image.load(self.cfg.MAPELEMENTSPATHS['24'][0])
            # ----底色
            filepath = self.cfg.MAPELEMENTSPATHS['0'][0]
            for col in range(width):
                for row in range(height):
                    image = pygame.image.load(filepath)
                    image = pygame.transform.scale(image, (self.cfg.BLOCKSIZE, self.cfg.BLOCKSIZE))
                    screen.blit(image, (left + col * self.cfg.BLOCKSIZE, top + row * self.cfg.BLOCKSIZE))
            # ----左上角图标
            screen.blit(id_image, (left + 10, top + 10))
            # ----对话框中的文字
            for idx, text in enumerate(conversation):
                font_render = font.render(text, True, (255, 255, 255))
                rect = font_render.get_rect()
                rect.left, rect.top = left + self.cfg.BLOCKSIZE + 20, top + 10 + idx * 30
                screen.blit(font_render, rect)
            # --刷新
            pygame.display.flip()
            clock.tick(self.cfg.FPS)