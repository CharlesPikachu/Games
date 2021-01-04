'''
Function:
    定义游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import time
import random
import pygame


'''拼图精灵类'''
class gemSprite(pygame.sprite.Sprite):
    def __init__(self, img_path, size, position, downlen, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_path)
        self.image = pygame.transform.smoothscale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.downlen = downlen
        self.target_x = position[0]
        self.target_y = position[1] + downlen
        self.type = img_path.split('/')[-1].split('.')[0]
        self.fixed = False
        self.speed_x = 10
        self.speed_y = 10
        self.direction = 'down'
    '''拼图块移动'''
    def move(self):
        if self.direction == 'down':
            self.rect.top = min(self.target_y, self.rect.top+self.speed_y)
            if self.target_y == self.rect.top:
                self.fixed = True
        elif self.direction == 'up':
            self.rect.top = max(self.target_y, self.rect.top-self.speed_y)
            if self.target_y == self.rect.top:
                self.fixed = True
        elif self.direction == 'left':
            self.rect.left = max(self.target_x, self.rect.left-self.speed_x)
            if self.target_x == self.rect.left:
                self.fixed = True
        elif self.direction == 'right':
            self.rect.left = min(self.target_x, self.rect.left+self.speed_x)
            if self.target_x == self.rect.left:
                self.fixed = True
    '''获取坐标'''
    def getPosition(self):
        return self.rect.left, self.rect.top
    '''设置坐标'''
    def setPosition(self, position):
        self.rect.left, self.rect.top = position


'''游戏类'''
class gemGame():
    def __init__(self, screen, sounds, font, gem_imgs, cfg, **kwargs):
        self.info = 'Gemgem —— Charles的皮卡丘'
        self.screen = screen
        self.sounds = sounds
        self.font = font
        self.gem_imgs = gem_imgs
        self.cfg = cfg
        self.reset()
    '''开始游戏'''
    def start(self):
        clock = pygame.time.Clock()
        # 遍历整个游戏界面更新位置
        overall_moving = True
        # 指定某些对象个体更新位置
        individual_moving = False
        # 定义一些必要的变量
        gem_selected_xy = None
        gem_selected_xy2 = None
        swap_again = False
        add_score = 0
        add_score_showtimes = 10
        time_pre = int(time.time())
        # 游戏主循环
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if (not overall_moving) and (not individual_moving) and (not add_score):
                        position = pygame.mouse.get_pos()
                        if gem_selected_xy is None:
                            gem_selected_xy = self.checkSelected(position)
                        else:
                            gem_selected_xy2 = self.checkSelected(position)
                            if gem_selected_xy2:
                                if self.swapGem(gem_selected_xy, gem_selected_xy2):
                                    individual_moving = True
                                    swap_again = False
                                else:
                                    gem_selected_xy = None
            if overall_moving:
                overall_moving = not self.dropGems(0, 0)
                # 移动一次可能可以拼出多个3连块
                if not overall_moving:
                    res_match = self.isMatch()
                    add_score = self.removeMatched(res_match)
                    if add_score > 0:
                        overall_moving = True
            if individual_moving:
                gem1 = self.getGemByPos(*gem_selected_xy)
                gem2 = self.getGemByPos(*gem_selected_xy2)
                gem1.move()
                gem2.move()
                if gem1.fixed and gem2.fixed:
                    res_match = self.isMatch()
                    if res_match[0] == 0 and not swap_again:
                        swap_again = True
                        self.swapGem(gem_selected_xy, gem_selected_xy2)
                        self.sounds['mismatch'].play()
                    else:
                        add_score = self.removeMatched(res_match)
                        overall_moving = True
                        individual_moving = False
                        gem_selected_xy = None
                        gem_selected_xy2 = None
            self.screen.fill((135, 206, 235))
            self.drawGrids()
            self.gems_group.draw(self.screen)
            if gem_selected_xy:
                self.drawBlock(self.getGemByPos(*gem_selected_xy).rect)
            if add_score:
                if add_score_showtimes == 10:
                    random.choice(self.sounds['match']).play()
                self.drawAddScore(add_score)
                add_score_showtimes -= 1
                if add_score_showtimes < 1:
                    add_score_showtimes = 10
                    add_score = 0
            self.remaining_time -= (int(time.time()) - time_pre)
            time_pre = int(time.time())
            self.showRemainingTime()
            self.drawScore()
            if self.remaining_time <= 0:
                return self.score
            pygame.display.update()
            clock.tick(self.cfg.FPS)
    '''初始化'''
    def reset(self):
        # 随机生成各个块(即初始化游戏地图各个元素)
        while True:
            self.all_gems = []
            self.gems_group = pygame.sprite.Group()
            for x in range(self.cfg.NUMGRID):
                self.all_gems.append([])
                for y in range(self.cfg.NUMGRID):
                    gem = gemSprite(img_path=random.choice(self.gem_imgs), size=(self.cfg.GRIDSIZE, self.cfg.GRIDSIZE), position=[self.cfg.XMARGIN+x*self.cfg.GRIDSIZE, self.cfg.YMARGIN+y*self.cfg.GRIDSIZE-self.cfg.NUMGRID*self.cfg.GRIDSIZE], downlen=self.cfg.NUMGRID*self.cfg.GRIDSIZE)
                    self.all_gems[x].append(gem)
                    self.gems_group.add(gem)
            if self.isMatch()[0] == 0:
                break
        # 得分
        self.score = 0
        # 拼出一个的奖励
        self.reward = 10
        # 时间
        self.remaining_time = 300
    '''显示剩余时间'''
    def showRemainingTime(self):
        remaining_time_render = self.font.render('CountDown: %ss' % str(self.remaining_time), 1, (85, 65, 0))
        rect = remaining_time_render.get_rect()
        rect.left, rect.top = (self.cfg.SCREENSIZE[0]-201, 6)
        self.screen.blit(remaining_time_render, rect)
    '''显示得分'''
    def drawScore(self):
        score_render = self.font.render('SCORE:'+str(self.score), 1, (85, 65, 0))
        rect = score_render.get_rect()
        rect.left, rect.top = (10, 6)
        self.screen.blit(score_render, rect)
    '''显示加分'''
    def drawAddScore(self, add_score):
        score_render = self.font.render('+'+str(add_score), 1, (255, 100, 100))
        rect = score_render.get_rect()
        rect.left, rect.top = (250, 250)
        self.screen.blit(score_render, rect)
    '''生成新的拼图块'''
    def generateNewGems(self, res_match):
        if res_match[0] == 1:
            start = res_match[2]
            while start > -2:
                for each in [res_match[1], res_match[1]+1, res_match[1]+2]:
                    gem = self.getGemByPos(*[each, start])
                    if start == res_match[2]:
                        self.gems_group.remove(gem)
                        self.all_gems[each][start] = None
                    elif start >= 0:
                        gem.target_y += self.cfg.GRIDSIZE
                        gem.fixed = False
                        gem.direction = 'down'
                        self.all_gems[each][start+1] = gem
                    else:
                        gem = gemSprite(img_path=random.choice(self.gem_imgs), size=(self.cfg.GRIDSIZE, self.cfg.GRIDSIZE), position=[self.cfg.XMARGIN+each*self.cfg.GRIDSIZE, self.cfg.YMARGIN-self.cfg.GRIDSIZE], downlen=self.cfg.GRIDSIZE)
                        self.gems_group.add(gem)
                        self.all_gems[each][start+1] = gem
                start -= 1
        elif res_match[0] == 2:
            start = res_match[2]
            while start > -4:
                if start == res_match[2]:
                    for each in range(0, 3):
                        gem = self.getGemByPos(*[res_match[1], start+each])
                        self.gems_group.remove(gem)
                        self.all_gems[res_match[1]][start+each] = None
                elif start >= 0:
                    gem = self.getGemByPos(*[res_match[1], start])
                    gem.target_y += self.cfg.GRIDSIZE * 3
                    gem.fixed = False
                    gem.direction = 'down'
                    self.all_gems[res_match[1]][start+3] = gem
                else:
                    gem = gemSprite(img_path=random.choice(self.gem_imgs), size=(self.cfg.GRIDSIZE, self.cfg.GRIDSIZE), position=[self.cfg.XMARGIN+res_match[1]*self.cfg.GRIDSIZE, self.cfg.YMARGIN+start*self.cfg.GRIDSIZE], downlen=self.cfg.GRIDSIZE*3)
                    self.gems_group.add(gem)
                    self.all_gems[res_match[1]][start+3] = gem
                start -= 1
    '''移除匹配的gem'''
    def removeMatched(self, res_match):
        if res_match[0] > 0:
            self.generateNewGems(res_match)
            self.score += self.reward
            return self.reward
        return 0
    '''游戏界面的网格绘制'''
    def drawGrids(self):
        for x in range(self.cfg.NUMGRID):
            for y in range(self.cfg.NUMGRID):
                rect = pygame.Rect((self.cfg.XMARGIN+x*self.cfg.GRIDSIZE, self.cfg.YMARGIN+y*self.cfg.GRIDSIZE, self.cfg.GRIDSIZE, self.cfg.GRIDSIZE))
                self.drawBlock(rect, color=(0, 0, 255), size=1)
    '''画矩形block框'''
    def drawBlock(self, block, color=(255, 0, 255), size=4):
        pygame.draw.rect(self.screen, color, block, size)
    '''下落特效'''
    def dropGems(self, x, y):
        if not self.getGemByPos(x, y).fixed:
            self.getGemByPos(x, y).move()
        if x < self.cfg.NUMGRID - 1:
            x += 1
            return self.dropGems(x, y)
        elif y < self.cfg.NUMGRID - 1:
            x = 0
            y += 1
            return self.dropGems(x, y)
        else:
            return self.isFull()
    '''是否每个位置都有拼图块了'''
    def isFull(self):
        for x in range(self.cfg.NUMGRID):
            for y in range(self.cfg.NUMGRID):
                if not self.getGemByPos(x, y).fixed:
                    return False
        return True
    '''检查有无拼图块被选中'''
    def checkSelected(self, position):
        for x in range(self.cfg.NUMGRID):
            for y in range(self.cfg.NUMGRID):
                if self.getGemByPos(x, y).rect.collidepoint(*position):
                    return [x, y]
        return None
    '''是否有连续一样的三个块(无--返回0/水平--返回1/竖直--返回2)'''
    def isMatch(self):
        for x in range(self.cfg.NUMGRID):
            for y in range(self.cfg.NUMGRID):
                if x + 2 < self.cfg.NUMGRID:
                    if self.getGemByPos(x, y).type == self.getGemByPos(x+1, y).type == self.getGemByPos(x+2, y).type:
                        return [1, x, y]
                if y + 2 < self.cfg.NUMGRID:
                    if self.getGemByPos(x, y).type == self.getGemByPos(x, y+1).type == self.getGemByPos(x, y+2).type:
                        return [2, x, y]
        return [0, x, y]
    '''根据坐标获取对应位置的拼图对象'''
    def getGemByPos(self, x, y):
        return self.all_gems[x][y]
    '''交换拼图'''
    def swapGem(self, gem1_pos, gem2_pos):
        margin = gem1_pos[0] - gem2_pos[0] + gem1_pos[1] - gem2_pos[1]
        if abs(margin) != 1:
            return False
        gem1 = self.getGemByPos(*gem1_pos)
        gem2 = self.getGemByPos(*gem2_pos)
        if gem1_pos[0] - gem2_pos[0] == 1:
            gem1.direction = 'left'
            gem2.direction = 'right'
        elif gem1_pos[0] - gem2_pos[0] == -1:
            gem2.direction = 'left'
            gem1.direction = 'right'
        elif gem1_pos[1] - gem2_pos[1] == 1:
            gem1.direction = 'up'
            gem2.direction = 'down'
        elif gem1_pos[1] - gem2_pos[1] == -1:
            gem2.direction = 'up'
            gem1.direction = 'down'
        gem1.target_x = gem2.rect.left
        gem1.target_y = gem2.rect.top
        gem1.fixed = False
        gem2.target_x = gem1.rect.left
        gem2.target_y = gem1.rect.top
        gem2.fixed = False
        self.all_gems[gem2_pos[0]][gem2_pos[1]] = gem1
        self.all_gems[gem1_pos[0]][gem1_pos[1]] = gem2
        return True
    '''info'''
    def __repr__(self):
        return self.info