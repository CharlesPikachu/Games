'''
Function:
    定义游戏关卡
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import pygame
from .sprites import *


'''定义游戏关卡'''
class GameLevels():
    def __init__(self, cfg, screen):
        self.cfg = cfg
        self.screen = screen
        self.screen_size = (self.cfg.SCREENSIZE[0], self.cfg.SCREENSIZE[1] - 50)
        self.score = 0
        self.num_levels = 15
        self.level_pointer = 1
    '''游戏状态'''
    def status(self, pigs, birds):
        status_codes = {
            'gaming': 0,
            'failure': 1,
            'victory': 2,
        }
        if len(pigs) == 0: return status_codes['victory']
        elif len(birds) == 0: return status_codes['failure']
        else: return status_codes['gaming']
    '''结束游戏'''
    def quitgame(self):
        pygame.quit()
        sys.exit()
    '''所有元素是否已经静止'''
    def still(self, sprites_list, threshold=0.15):
        for sprite in sprites_list:
            if sprite.velocity.magnitude >= threshold:
                return False
        return True
    '''碰撞检测'''
    def collision(self, sprite1, sprite2):
        is_collision = False
        elasticity, block_elasticity = 0.8, 0.7
        if sprite1.type in ['pig', 'bird'] and sprite2.type in ['pig', 'bird']:
            dx, dy = sprite1.loc_info[0] - sprite2.loc_info[0], sprite1.loc_info[1] - sprite2.loc_info[1]
            dist = math.hypot(dx, dy)
            if dist < sprite1.loc_info[2] + sprite2.loc_info[2]:
                tangent = math.atan2(dy, dx)
                angle = 0.5 * math.pi + tangent
                angle1, angle2 = 2 * tangent - sprite1.velocity.angle, 2 * tangent - sprite2.velocity.angle
                magnitude1, magnitude2 = sprite2.velocity.magnitude, sprite1.velocity.magnitude
                sprite1.velocity, sprite2.velocity = VelocityVector(magnitude1, angle1), VelocityVector(magnitude2, angle2)
                sprite1.velocity.magnitude *= elasticity
                sprite2.velocity.magnitude *= elasticity
                overlap = 0.5 * (sprite1.loc_info[2] + sprite2.loc_info[2] - dist + 1)
                sprite1.loc_info[0] += math.sin(angle) * overlap
                sprite1.loc_info[1] -= math.cos(angle) * overlap
                sprite2.loc_info[0] -= math.sin(angle) * overlap
                sprite2.loc_info[1] += math.cos(angle) * overlap
                is_collision = True
        elif sprite1.type in ['pig', 'bird'] and sprite2.type in ['block']:
            dx, dy = sprite1.loc_info[0] - sprite2.loc_info[0], sprite1.loc_info[1] - sprite2.loc_info[1]
            dist = math.hypot(dx, dy)
            if dist < sprite1.loc_info[2] + sprite2.rect.width:
                tangent = math.atan2(dy, dx)
                angle = 0.5 * math.pi + tangent
                angle1, angle2 = 2 * tangent - sprite1.velocity.angle, 2 * tangent - sprite2.velocity.angle
                magnitude1, magnitude2 = sprite2.velocity.magnitude, sprite1.velocity.magnitude
                sprite1.velocity, sprite2.velocity = VelocityVector(magnitude1, angle1), VelocityVector(magnitude2, angle2)
                sprite1.velocity.magnitude *= elasticity
                sprite2.velocity.magnitude *= block_elasticity
                overlap = 0.5 * (sprite1.loc_info[2] + sprite2.rect.width - dist + 1)
                sprite1.loc_info[0] += math.sin(angle) * overlap
                sprite1.loc_info[1] -= math.cos(angle) * overlap
                sprite2.loc_info[0] -= math.sin(angle) * overlap
                sprite2.loc_info[1] += math.cos(angle) * overlap
                is_collision = True
        elif sprite1.type in ['block'] and sprite2.type in ['block']:
            if (sprite1.loc_info[1] + sprite1.rect.height > sprite2.loc_info[1]) and (sprite1.loc_info[1] < sprite2.loc_info[1] + sprite2.rect.height):
                if (sprite1.loc_info[0] < sprite2.loc_info[0] + sprite2.rect.width) and (sprite1.loc_info[0] + sprite1.rect.width > sprite2.loc_info[0] + sprite2.rect.width):
                    sprite1.loc_info[0] = 2 * (sprite2.loc_info[0] + sprite2.rect.width) - sprite1.loc_info[0]
                    sprite1.velocity.angle = -sprite1.velocity.angle
                    sprite1.rotate_angle = -sprite1.velocity.angle
                    sprite1.velocity.magnitude *= block_elasticity
                    sprite2.velocity.angle = -sprite2.velocity.angle
                    sprite2.rotate_angle = -sprite2.velocity.angle
                    sprite2.velocity.magnitude *= block_elasticity
                    is_collision = True
                elif (sprite1.loc_info[0] + sprite1.rect.width > sprite2.loc_info[0]) and (sprite1.loc_info[0] < sprite2.loc_info[0]):
                    sprite1.loc_info[0] = 2 * (sprite2.loc_info[0] - sprite1.rect.width) - sprite1.loc_info[0]
                    sprite1.velocity.angle = -sprite1.velocity.angle
                    sprite1.rotate_angle = -sprite1.velocity.angle
                    sprite1.velocity.magnitude *= block_elasticity
                    sprite2.velocity.angle = -sprite2.velocity.angle
                    sprite2.rotate_angle = -sprite2.velocity.angle
                    sprite2.velocity.magnitude *= block_elasticity
                    is_collision = True
            if (sprite1.loc_info[0] + sprite1.rect.width > sprite2.loc_info[0]) and (sprite1.loc_info[0] < sprite2.loc_info[0] + sprite2.rect.width):
                if (sprite1.loc_info[1] + sprite1.rect.height > sprite2.loc_info[1]) and (sprite1.loc_info[1] < sprite2.loc_info[1]):
                    sprite1.loc_info[1] = 2 * (sprite2.loc_info[1] - sprite1.rect.height) - sprite1.loc_info[1]
                    sprite1.velocity.angle = math.pi - sprite1.velocity.angle
                    sprite1.rotate_angle = math.pi - sprite1.velocity.angle
                    sprite1.velocity.magnitude *= block_elasticity
                    sprite2.velocity.angle = math.pi - sprite2.velocity.angle
                    sprite2.rotate_angle = math.pi - sprite2.velocity.angle
                    sprite2.velocity.magnitude *= block_elasticity
                    is_collision = True
                elif (sprite1.loc_info[1] < sprite2.loc_info[1] + sprite2.rect.height) and (sprite1.loc_info[1] + sprite1.rect.height > sprite2.loc_info[1] + sprite2.rect.height):
                    sprite1.loc_info[1] = 2 * (sprite2.loc_info[1] + sprite2.rect.height) - sprite1.loc_info[1]
                    sprite1.velocity.angle = math.pi - sprite1.velocity.angle
                    sprite1.rotate_angle = math.pi - sprite1.velocity.angle
                    sprite1.velocity.magnitude *= block_elasticity
                    sprite2.velocity.angle = math.pi - sprite2.velocity.angle
                    sprite2.rotate_angle = math.pi - sprite2.velocity.angle
                    sprite2.velocity.magnitude *= block_elasticity
                    is_collision = True
        elif sprite1.type in ['pig', 'bird'] and sprite2.type in ['wall']:
            if (sprite1.loc_info[1] + sprite1.loc_info[2] > sprite2.y) and (sprite1.loc_info[1] < sprite2.y + sprite2.height):
                if (sprite1.loc_info[0] < sprite2.x + sprite2.width) and (sprite1.loc_info[0] + sprite1.loc_info[2] > sprite2.x + sprite2.width):
                    sprite1.loc_info[0] = 2 * (sprite2.x + sprite2.width) - sprite1.loc_info[0]
                    sprite1.velocity.angle = -sprite1.velocity.angle
                    sprite1.velocity.magnitude *= elasticity
                elif (sprite1.loc_info[0] + sprite1.loc_info[2] > sprite2.x) and (sprite1.loc_info[0] < sprite2.x):
                    sprite1.loc_info[0] = 2 * (sprite2.x - sprite1.loc_info[2]) - sprite1.loc_info[0]
                    sprite1.velocity.angle = -sprite1.velocity.angle
                    sprite1.velocity.magnitude *= elasticity
            if (sprite1.loc_info[0] + sprite1.loc_info[2] > sprite2.x) and (sprite1.loc_info[0] < sprite2.x + sprite2.width):
                if (sprite1.loc_info[1] + sprite1.loc_info[2] > sprite2.y) and (sprite1.loc_info[1] < sprite2.y):
                    sprite1.loc_info[1] = 2 * (sprite2.y - sprite1.loc_info[2]) - sprite1.loc_info[1]
                    sprite1.velocity.angle = math.pi - sprite1.velocity.angle
                    sprite1.velocity.magnitude *= elasticity
                elif (sprite1.loc_info[1] < sprite2.y + sprite2.height) and (sprite1.loc_info[1] + sprite1.loc_info[2] > sprite2.y + sprite2.height):
                    sprite1.loc_info[1] = 2 * (sprite2.y + sprite2.height) - sprite1.loc_info[1]
                    sprite1.velocity.angle = math.pi - sprite1.velocity.angle
                    sprite1.velocity.magnitude *= elasticity
        elif sprite1.type in ['block'] and sprite2.type in ['wall']:
            if (sprite1.loc_info[1] + sprite1.rect.height > sprite2.y) and (sprite1.loc_info[1] < sprite2.y + sprite2.height):
                if (sprite1.loc_info[0] < sprite2.x + sprite2.width) and (sprite1.loc_info[0] + sprite1.rect.width > sprite2.x + sprite2.width):
                    sprite1.loc_info[0] = 2 * (sprite2.x + sprite2.width) - sprite1.loc_info[0]
                    sprite1.velocity.angle = -sprite1.velocity.angle
                    sprite1.rotate_angle = -sprite1.velocity.angle
                    sprite1.velocity.magnitude *= elasticity
                elif (sprite1.loc_info[0] + sprite1.rect.width > sprite2.x) and (sprite1.loc_info[0] < sprite2.x):
                    sprite1.loc_info[0] = 2 * (sprite2.x - sprite1.rect.width) - sprite1.loc_info[0]
                    sprite1.velocity.angle = -sprite1.velocity.angle
                    sprite1.rotate_angle = -sprite1.velocity.angle
                    sprite1.velocity.magnitude *= elasticity
            if (sprite1.loc_info[0] + sprite1.rect.width > sprite2.x) and (sprite1.loc_info[0] < sprite2.x + sprite2.width):
                if (sprite1.loc_info[1] + sprite1.rect.height > sprite2.y) and (sprite1.loc_info[1] < sprite2.y):
                    sprite1.loc_info[1] = 2 * (sprite2.y - sprite1.rect.height) - sprite1.loc_info[1]
                    sprite1.velocity.angle = math.pi - sprite1.velocity.angle
                    sprite1.rotate_angle = math.pi - sprite1.velocity.angle
                    sprite1.velocity.magnitude *= elasticity
                elif (sprite1.loc_info[1] < sprite2.y + sprite2.height) and (sprite1.loc_info[1] + sprite1.rect.height > sprite2.y + sprite2.height):
                    sprite1.loc_info[1] = 2 * (sprite2.y + sprite2.height) - sprite1.loc_info[1]
                    sprite1.velocity.angle = math.pi - sprite1.velocity.angle
                    sprite1.rotate_angle = math.pi - sprite1.velocity.angle
                    sprite1.velocity.magnitude *= elasticity
        else:
            raise TypeError('Unsupport detect the collision of %s and %s...' % (sprite1.type, sprite2.type))
        return sprite1, sprite2, is_collision
    '''重玩当前关卡'''
    def replay(self):
        self.level_pointer -= 1
        self.start()
    '''重新开始'''
    def restart(self):
        self.level_pointer = 1
        self.start()
    '''游戏关卡切换界面'''
    def switchlevelinterface(self):
        self.level_pointer += 1
        level_switch_label = Label(self.screen, 700, 100, 400, 200)
        if self.level_pointer <= self.num_levels:
            level_switch_label.addtext(f'LEVEL {str(self.level_pointer - 1)} CLEARED!', 80, self.cfg.FONTPATH['Comic_Kings'], (236, 240, 241))
        else:
            level_switch_label.addtext('ALL LEVELS CLEARED!', 80, self.cfg.FONTPATH['Comic_Kings'], (236, 240, 241))
        score_label = Label(self.screen, 750, 300, 300, 100)
        score_label.addtext(f'SCORE: {self.score}', 55, self.cfg.FONTPATH['Comic_Kings'], (236, 240, 241))
        replay_btn = Button(self.screen, 350, 500, 300, 100, self.replay, (244, 208, 63), (247, 220, 111))
        replay_btn.addtext('PLAY AGAIN', 60, self.cfg.FONTPATH['arfmoochikncheez'], self.cfg.BACKGROUND_COLOR)
        if self.level_pointer <= self.num_levels:
            next_btn = Button(self.screen, 750, 500, 300, 100, self.start, (88, 214, 141), (171, 235, 198))
            next_btn.addtext('NEXT LEVEL', 60, self.cfg.FONTPATH['arfmoochikncheez'], self.cfg.BACKGROUND_COLOR)
        else:
            next_btn = Button(self.screen, 750, 500, 300, 100, self.restart, (88, 214, 141), (171, 235, 198))
            next_btn.addtext('RESTART', 60, self.cfg.FONTPATH['arfmoochikncheez'], self.cfg.BACKGROUND_COLOR)
        quit_btn = Button(self.screen, 1150, 500, 300, 100, self.quitgame, (241, 148, 138), (245, 183, 177))
        quit_btn.addtext('QUIT', 60, self.cfg.FONTPATH['arfmoochikncheez'], self.cfg.BACKGROUND_COLOR)
        charles_label = Label(self.screen, self.screen_size[0] - 270, self.screen_size[1] - 20, 300, 100)
        charles_label.addtext('CHARLES', 60, self.cfg.FONTPATH['arfmoochikncheez'], (113, 125, 126))
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitgame()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.quitgame()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if replay_btn.selected(): replay_btn.action()
                    if next_btn.selected(): next_btn.action()
                    if quit_btn.selected(): quit_btn.action()
            for component in [replay_btn, next_btn, quit_btn, level_switch_label, score_label, charles_label]:
                component.draw()
            pygame.display.update()
            clock.tick(self.cfg.FPS)
    '''游戏失败界面'''
    def failureinterface(self):
        failure_label = Label(self.screen, 700, 100, 400, 200)
        failure_label.addtext('LEVEL FAILED!', 80, self.cfg.FONTPATH['Comic_Kings'], (236, 240, 241))
        score_label = Label(self.screen, 750, 300, 300, 100)
        score_label.addtext(f'SCORE: {self.score}', 55, self.cfg.FONTPATH['Comic_Kings'], (236, 240, 241))
        replay_btn = Button(self.screen, 500, 500, 300, 100, self.start, (244, 208, 63), (247, 220, 111))
        replay_btn.addtext('TRY AGAIN', 60, self.cfg.FONTPATH['arfmoochikncheez'], self.cfg.BACKGROUND_COLOR)
        quit_btn = Button(self.screen, 1000, 500, 300, 100, self.quitgame, (241, 148, 138), (245, 183, 177))
        quit_btn.addtext('QUIT', 60, self.cfg.FONTPATH['arfmoochikncheez'], self.cfg.BACKGROUND_COLOR)
        charles_label = Label(self.screen, self.screen_size[0] - 270, self.screen_size[1] - 20, 300, 100)
        charles_label.addtext('CHARLES', 60, self.cfg.FONTPATH['arfmoochikncheez'], (113, 125, 126))
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitgame()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.quitgame()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if replay_btn.selected(): replay_btn.action()
                    if quit_btn.selected(): quit_btn.action()
            for component in [replay_btn, quit_btn, failure_label, score_label, charles_label]:
                component.draw()
            pygame.display.update()
            clock.tick(self.cfg.FPS)
    '''游戏暂停界面'''
    def pauseinterface(self):
        pause_label = Label(self.screen, 700, 200, 400, 200)
        pause_label.addtext('GAME PAUSED', 70, self.cfg.FONTPATH['Comic_Kings'], (236, 240, 241))
        replay_btn = Button(self.screen, 350, 500, 300, 100, self.start, (244, 208, 63), (247, 220, 111))
        replay_btn.addtext('RESTART', 60, self.cfg.FONTPATH['arfmoochikncheez'], self.cfg.BACKGROUND_COLOR)
        resume_btn = Button(self.screen, 750, 500, 300, 100, None, (88, 214, 141), (171, 235, 198))
        resume_btn.addtext('RESUME', 60, self.cfg.FONTPATH['arfmoochikncheez'], self.cfg.BACKGROUND_COLOR)
        quit_btn = Button(self.screen, 1150, 500, 300, 100, self.quitgame, (241, 148, 138), (245, 183, 177))
        quit_btn.addtext('QUIT', 60, self.cfg.FONTPATH['arfmoochikncheez'], self.cfg.BACKGROUND_COLOR)
        charles_label = Label(self.screen, self.screen_size[0] - 270, self.screen_size[1] - 20, 300, 100)
        charles_label.addtext('CHARLES', 60, self.cfg.FONTPATH['arfmoochikncheez'], (113, 125, 126))
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitgame()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.quitgame()
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if replay_btn.selected(): replay_btn.action()
                    if resume_btn.selected(): return
                    if quit_btn.selected(): quit_btn.action()
            for component in [replay_btn, resume_btn, quit_btn, pause_label, charles_label]:
                component.draw()
            pygame.display.update()
            clock.tick(self.cfg.FPS)
    '''开始游戏'''
    def start(self):
        # 导入所有游戏精灵
        game_sprites = self.loadlevelmap()
        birds, pigs, blocks, walls = game_sprites['birds'], game_sprites['pigs'], game_sprites['blocks'], game_sprites['walls']
        slingshot = Slingshot(self.screen, 200, self.screen_size[1] - 200, 30, 200)
        birds[0].load(slingshot)
        score_label = Label(self.screen, 50, 10, 100, 50)
        score_label.addtext(f'SCORE: {self.score}', 25, self.cfg.FONTPATH['Comic_Kings'], (236, 240, 241))
        birds_remaining_label = Label(self.screen, 120, 50, 100, 50)
        birds_remaining_label.addtext(f"BIRDS REMAINING: {len(birds)}", 25, self.cfg.FONTPATH['Comic_Kings'], (236, 240, 241))
        pigs_remaining_label = Label(self.screen, 110, 90, 100, 50)
        pigs_remaining_label.addtext(f"PIGS REMAINING: {len(pigs)}", 25, self.cfg.FONTPATH['Comic_Kings'], (236, 240, 241))
        charles_label = Label(self.screen, self.screen_size[0] - 270, self.screen_size[1] - 20, 300, 100)
        charles_label.addtext('CHARLES', 60, self.cfg.FONTPATH['arfmoochikncheez'], (113, 125, 126))
        # 游戏主循环
        clock = pygame.time.Clock()
        blocks_to_remove, pigs_to_remove = [], []
        while True:
            # --按键检测
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitgame()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.quitgame()
                    elif event.key == pygame.K_r:
                        self.start()
                    elif event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        self.pauseinterface()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if birds[0].selected():
                        birds[0].is_selected = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if birds[0].is_selected:
                        birds[0].is_selected = False
                        birds[0].start_flying = True
            # --背景颜色填充
            color = self.cfg.BACKGROUND_COLOR
            for i in range(3):
                color = (color[0] + 5, color[1] + 5, color[2] + 5)
                pygame.draw.rect(self.screen, color, (0, i * 300, self.screen_size[0], 300))
            pygame.draw.rect(self.screen, (77, 86, 86), (0, self.screen_size[1], self.screen_size[0], 50))
            # --判断游戏是否结束，若没有则导入新的小鸟
            if (not birds[0].is_loaded) and self.still(pigs + birds + blocks):
                birds.pop(0)
                if self.status(pigs, birds) == 2:
                    self.score += len(birds) * 100
                    self.switchlevelinterface()
                elif self.status(pigs, birds) == 1:
                    self.failureinterface()
                birds[0].load(slingshot)
                birds[0].start_flying = False
            # --重置小鸟的位置
            if birds[0].is_selected:
                birds[0].reposition(slingshot)
            if hasattr(birds[0], 'start_flying') and birds[0].start_flying:
                birds[0].is_loaded = False
            # --弹弓
            slingshot.draw(birds[0])
            # --判断猪是否撞上木桩
            for i in range(len(pigs)):
                for j in range(len(blocks)):
                    pig_magnitude_1, block_magnitude_1 = pigs[i].velocity.magnitude, blocks[j].velocity.magnitude
                    pigs[i], blocks[j], is_collision = self.collision(pigs[i], blocks[j])
                    pig_magnitude_2, block_magnitude_2 = pigs[i].velocity.magnitude, blocks[j].velocity.magnitude
                    if is_collision:
                        if abs(pig_magnitude_2 - pig_magnitude_2) > 2:
                            blocks_to_remove.append(blocks[j])
                            blocks[j].setdestroy()
                        if abs(block_magnitude_2 - block_magnitude_1) > 2:
                            pigs_to_remove.append(pigs[i])
                            pigs[i].setdead()
            # --判断鸟是否撞上木桩
            for i in range(len(birds)):
                if not (birds[i].is_loaded or birds[i].velocity.magnitude == 0):
                    for j in range(len(blocks)):
                        bird_magnitude_1, block_magnitude_1 = birds[i].velocity.magnitude, blocks[j].velocity.magnitude
                        birds[i], blocks[j], is_collision = self.collision(birds[i], blocks[j])
                        bird_magnitude_2, block_magnitude_2 = birds[i].velocity.magnitude, blocks[j].velocity.magnitude
                        if is_collision:
                            if abs(bird_magnitude_1 - bird_magnitude_2) > 2:
                                if blocks[j] not in blocks_to_remove:
                                    blocks_to_remove.append(blocks[j])
                                    blocks[j].setdestroy()
            # --判断猪是否撞上猪或者猪撞墙
            for i in range(len(pigs)):
                pigs[i].move()
                for j in range(i+1, len(pigs)):
                    pig1_magnitude_1, pig2_magnitude_1 = pigs[i].velocity.magnitude, pigs[j].velocity.magnitude
                    pigs[i], pigs[j], is_collision = self.collision(pigs[i], pigs[j])
                    pig1_magnitude_2, pig2_magnitude_2 = pigs[i].velocity.magnitude, pigs[j].velocity.magnitude
                    if abs(pig1_magnitude_1 - pig1_magnitude_2) > 2:
                        if pigs[j] not in pigs_to_remove:
                            pigs_to_remove.append(pigs[j])
                            pigs[j].setdead()
                    if abs(pig2_magnitude_1 - pig2_magnitude_2) > 2:
                        if pigs[i] not in pigs_to_remove:
                            pigs_to_remove.append(pigs[i])
                            pigs[i].setdead()
                for wall in walls: pigs[i] = self.collision(pigs[i], wall)[0]
                pigs[i].draw()
            # --判断鸟是否撞到猪或者鸟是否撞到墙
            for i in range(len(birds)):
                if (not birds[i].is_loaded) and (birds[i].velocity.magnitude):
                    birds[i].move()
                    for j in range(len(pigs)):
                        bird_magnitude_1, pig_magnitude_1 = birds[i].velocity.magnitude, pigs[j].velocity.magnitude
                        birds[i], pigs[j], is_collision = self.collision(birds[i], pigs[j])
                        bird_magnitude_2, pig_magnitude_2 = birds[i].velocity.magnitude, pigs[j].velocity.magnitude
                        if is_collision:
                            if abs(bird_magnitude_2 - bird_magnitude_1) > 2:
                                if pigs[j] not in pigs_to_remove:
                                    pigs_to_remove.append(pigs[j])
                                    pigs[j].setdead()
                if birds[i].is_loaded: birds[i].projectpath()
                for wall in walls: birds[i] = self.collision(birds[i], wall)[0]
                birds[i].draw()
            # --判断木桩是否撞到了木桩或者木桩撞到墙
            for i in range(len(blocks)):
                for j in range(i+1, len(blocks)):
                    block1_magnitude_1, block2_magnitude_1 = blocks[i].velocity.magnitude, blocks[j].velocity.magnitude
                    blocks[i], blocks[j], is_collision = self.collision(blocks[i], blocks[j])
                    block1_magnitude_2, block2_magnitude_2 = blocks[i].velocity.magnitude, blocks[j].velocity.magnitude
                    if is_collision:
                        if abs(block1_magnitude_2 - block1_magnitude_1) > 2:
                            if blocks[j] not in blocks_to_remove:
                                blocks_to_remove.append(blocks[j])
                                blocks[j].setdestroy()
                        if abs(block2_magnitude_2 - block2_magnitude_1) > 2:
                            if blocks[i] not in blocks_to_remove:
                                blocks_to_remove.append(blocks[i])
                                blocks[i].setdestroy()
                blocks[i].move()
                for wall in walls: blocks[i] = self.collision(blocks[i], wall)[0]
                blocks[i].draw()
            # --墙
            for wall in walls: wall.draw()
            # --显示文字
            score_label.addtext(f'SCORE: {self.score}', 25, self.cfg.FONTPATH['Comic_Kings'], (236, 240, 241))
            score_label.draw()
            birds_remaining_label.addtext(f"BIRDS REMAINING: {len(birds)}", 25, self.cfg.FONTPATH['Comic_Kings'], (236, 240, 241))
            birds_remaining_label.draw()
            pigs_remaining_label.addtext(f"PIGS REMAINING: {len(pigs)}", 25, self.cfg.FONTPATH['Comic_Kings'], (236, 240, 241))
            pigs_remaining_label.draw()
            charles_label.draw()
            # --画面刷新
            pygame.display.update()
            clock.tick(self.cfg.FPS)
            # --删除无效的元素
            if self.still(birds + pigs + blocks):
                for pig in pigs_to_remove:
                    if pig in pigs:
                        pigs.remove(pig)
                        self.score += 100
                for block in blocks_to_remove:
                    if block in blocks:
                        blocks.remove(block)
                        self.score += 50
                pigs_to_remove = []
                blocks_to_remove = []
    '''载入当前关卡的游戏地图'''
    def loadlevelmap(self):
        self.score = 0
        birds, pigs, blocks, walls = [], [], [], []
        for i in range(3):
            birds.append(
                Bird(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['bird'], loc_info=(45 * i, self.screen_size[1] - 40, 20))
            )
        if self.level_pointer == 1:
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1100, self.screen_size[1] - 40, 20))
            )
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1500, self.screen_size[1] - 40, 20))
            )
            blocks.append(
                Block(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['block'], loc_info=(1300, self.screen_size[1] - 60, 60))
            )
        elif self.level_pointer == 2:
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1000, self.screen_size[1] - 40, 20))
            )
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1400, self.screen_size[1] - 40, 20))
            )
            blocks.append(
                Block(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['block'], loc_info=(1200, self.screen_size[1] - 60, 60))
            )
            blocks.append(
                Block(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['block'], loc_info=(1200, self.screen_size[1] - 70, 60))
            )
            blocks.append(
                Block(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['block'], loc_info=(1500, self.screen_size[1] - 60, 60))
            )
        elif self.level_pointer == 3:
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1200, self.screen_size[1] - 60, 30))
            )
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1300, self.screen_size[1] - 60, 30))
            )
            blocks.append(
                Block(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['block'], loc_info=(1000, self.screen_size[1] - 100, 100))
            )
            blocks.append(
                Block(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['block'], loc_info=(1000, self.screen_size[1] - 120, 100))
            )
            blocks.append(
                Block(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['block'], loc_info=(1500, self.screen_size[1] - 100, 100))
            )
            blocks.append(
                Block(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['block'], loc_info=(1500, self.screen_size[1] - 120, 100))
            )
        elif self.level_pointer == 4:
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1200, 440, 30))
            )
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1300, self.screen_size[1] - 60, 30))
            )
            walls.append(
                Slab(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['wall'], x=1000, y=450, width=500, height=20)
            )
            blocks.append(
                Block(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['block'], loc_info=(1100, self.screen_size[1] - 100, 100))
            )
        elif self.level_pointer == 5:
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1300, 440, 25))
            )
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1300, self.screen_size[1] - 60, 25))
            )
            walls.append(
                Slab(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['wall'], x=500, y=400, width=100, height=self.screen_size[1]-400)
            )
            walls.append(
                Slab(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['wall'], x=1000, y=450, width=500, height=30)
            )
            blocks.append(
                Block(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['block'], loc_info=(1150, 400, 100))
            )
            blocks.append(
                Block(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['block'], loc_info=(1100, self.screen_size[1] - 100, 100))
            )
        elif self.level_pointer == 6:
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1300, 440, 25))
            )
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1300, self.screen_size[1] - 60, 25))
            )
            walls.append(
                Slab(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['wall'], x=1000, y=0, width=30, height=450)
            )
            walls.append(
                Slab(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['wall'], x=1000, y=450, width=500, height=30)
            )
            blocks.append(
                Block(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['block'], loc_info=(1150, 400, 100))
            )
            blocks.append(
                Block(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['block'], loc_info=(1100, self.screen_size[1] - 100, 100))
            )
        elif self.level_pointer == 7:
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1100, 440, 25))
            )
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1300, 440, 25))
            )
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1200, self.screen_size[1] - 60, 25))
            )
            walls.append(
                Slab(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['wall'], x=1200, y=250, width=30, height=200)
            )
            walls.append(
                Slab(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['wall'], x=1000, y=450, width=500, height=30)
            )
        elif self.level_pointer == 8:
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1100, self.screen_size[1] - 60, 25))
            )
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1200, self.screen_size[1] - 60, 25))
            )
            walls.append(
                Slab(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['wall'], x=700, y=250, width=30, height=self.screen_size[1] - 250)
            )
        elif self.level_pointer == 9:
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1100, self.screen_size[1] - 60, 25))
            )
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1450, self.screen_size[1] - 60, 25))
            )
            blocks.append(
                Block(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['block'], loc_info=(1250, self.screen_size[1] - 100, 100))
            )
            blocks.append(
                Block(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['block'], loc_info=(1250, self.screen_size[1] - 120, 100))
            )
            walls.append(
                Slab(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['wall'], x=700, y=400, width=30, height=self.screen_size[1] - 400)
            )
        elif self.level_pointer == 10:
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1100, self.screen_size[1] - 60, 25))
            )
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1450, self.screen_size[1] - 60, 25))
            )
            blocks.append(
                Block(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['block'], loc_info=(1250, self.screen_size[1] - 100, 100))
            )
            blocks.append(
                Block(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['block'], loc_info=(1250, self.screen_size[1] - 120, 100))
            )
            blocks.append(
                Block(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['block'], loc_info=(900, self.screen_size[1] - 100, 100))
            )
            walls.append(
                Slab(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['wall'], x=900, y=400, width=500, height=30)
            )
        elif self.level_pointer == 11:
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1100, self.screen_size[1] - 60, 25))
            )
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1450, self.screen_size[1] - 60, 25))
            )
            blocks.append(
                Block(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['block'], loc_info=(1250, self.screen_size[1] - 100, 100))
            )
            blocks.append(
                Block(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['block'], loc_info=(1250, self.screen_size[1] - 120, 100))
            )
            walls.append(
                Slab(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['wall'], x=900, y=400, width=500, height=30)
            )
            walls.append(
                Slab(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['wall'], x=900, y=400, width=30, height=self.screen_size[1]-400)
            )
        elif self.level_pointer == 12:
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1100, self.screen_size[1] - 60, 25))
            )
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1450, self.screen_size[1] - 60, 25))
            )
            walls.append(
                Slab(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['wall'], x=900, y=400, width=500, height=30)
            )
            walls.append(
                Slab(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['wall'], x=1200, y=500, width=30, height=self.screen_size[1]-500)
            )
        elif self.level_pointer == 13:
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1100, self.screen_size[1] - 60, 25))
            )
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1200, 340, 25))
            )
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1450, self.screen_size[1] - 60, 25))
            )
            blocks.append(
                Block(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['block'], loc_info=(900, self.screen_size[1] - 100, 100))
            )
            blocks.append(
                Block(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['block'], loc_info=(900, self.screen_size[1] - 120, 100))
            )
            walls.append(
                Slab(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['wall'], x=900, y=400, width=500, height=40)
            )
            walls.append(
                Slab(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['wall'], x=1200, y=500, width=30, height=self.screen_size[1]-500)
            )
        elif self.level_pointer == 14:
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1100, self.screen_size[1] - 60, 25))
            )
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1100, 340, 25))
            )
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1450, self.screen_size[1] - 60, 25))
            )
            blocks.append(
                Block(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['block'], loc_info=(900, self.screen_size[1] - 100, 100))
            )
            blocks.append(
                Block(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['block'], loc_info=(1300, 300, 100))
            )
            walls.append(
                Slab(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['wall'], x=900, y=400, width=500, height=40)
            )
            walls.append(
                Slab(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['wall'], x=900, y=0, width=30, height=400)
            )
        elif self.level_pointer == 15:
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(900, self.screen_size[1] - 60, 25))
            )
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(self.screen_size[0] - 400, 340, 25))
            )
            pigs.append(
                Pig(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['pig'], loc_info=(1700, self.screen_size[1] - 60, 25))
            )
            walls.append(
                Slab(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['wall'], x=800, y=400, width=30, height=self.screen_size[1]-400)
            )
            walls.append(
                Slab(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['wall'], x=1000, y=500, width=30, height=self.screen_size[1]-500)
            )
            walls.append(
                Slab(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['wall'], x=self.screen_size[0]-500, y=400, width=500, height=40)
            )
            walls.append(
                Slab(screen=self.screen, imagepaths=self.cfg.IMAGEPATHS['wall'], x=self.screen_size[0]-500, y=150, width=60, height=250)
            )
        game_sprites = {
            'birds': birds,
            'pigs': pigs,
            'blocks': blocks,
            'walls': walls
        }
        return game_sprites          