'''
Function:
    flappybird小游戏
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


'''游戏初始化'''
def initGame():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((cfg.SCREENWIDTH, cfg.SCREENHEIGHT))
    pygame.display.set_caption('Flappy Bird —— Charles的皮卡丘')
    return screen


'''显示当前分数'''
def showScore(screen, score, number_images):
    digits = list(str(int(score)))
    width = 0
    for d in digits:
        width += number_images.get(d).get_width()
    offset = (cfg.SCREENWIDTH - width) / 2
    for d in digits:
        screen.blit(number_images.get(d), (offset, cfg.SCREENHEIGHT*0.1))
        offset += number_images.get(d).get_width()


'''主函数'''
def main():
    screen = initGame()
    # 加载必要的游戏资源
    # --导入音频
    sounds = dict()
    for key, value in cfg.AUDIO_PATHS.items():
        sounds[key] = pygame.mixer.Sound(value)
    # --导入数字图片
    number_images = dict()
    for key, value in cfg.NUMBER_IMAGE_PATHS.items():
        number_images[key] = pygame.image.load(value).convert_alpha()
    # --管道
    pipe_images = dict()
    pipe_images['bottom'] = pygame.image.load(random.choice(list(cfg.PIPE_IMAGE_PATHS.values()))).convert_alpha()
    pipe_images['top'] = pygame.transform.rotate(pipe_images['bottom'], 180)
    # --小鸟图片
    bird_images = dict()
    for key, value in cfg.BIRD_IMAGE_PATHS[random.choice(list(cfg.BIRD_IMAGE_PATHS.keys()))].items():
        bird_images[key] = pygame.image.load(value).convert_alpha()
    # --背景图片
    backgroud_image = pygame.image.load(random.choice(list(cfg.BACKGROUND_IMAGE_PATHS.values()))).convert_alpha()
    # --其他图片
    other_images = dict()
    for key, value in cfg.OTHER_IMAGE_PATHS.items():
        other_images[key] = pygame.image.load(value).convert_alpha()
    # 游戏开始界面
    game_start_info = startGame(screen, sounds, bird_images, other_images, backgroud_image, cfg)
    # 进入主游戏
    score = 0
    bird_pos, base_pos, bird_idx = list(game_start_info.values())
    base_diff_bg = other_images['base'].get_width() - backgroud_image.get_width()
    clock = pygame.time.Clock()
    # --管道类
    pipe_sprites = pygame.sprite.Group()
    for i in range(2):
        pipe_pos = Pipe.randomPipe(cfg, pipe_images.get('top'))
        pipe_sprites.add(Pipe(image=pipe_images.get('top'), position=(cfg.SCREENWIDTH+200+i*cfg.SCREENWIDTH/2, pipe_pos.get('top')[-1])))
        pipe_sprites.add(Pipe(image=pipe_images.get('bottom'), position=(cfg.SCREENWIDTH+200+i*cfg.SCREENWIDTH/2, pipe_pos.get('bottom')[-1])))
    # --bird类
    bird = Bird(images=bird_images, idx=bird_idx, position=bird_pos)
    # --是否增加pipe
    is_add_pipe = True
    # --游戏是否进行中
    is_game_running = True
    while is_game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    bird.setFlapped()
                    sounds['wing'].play()
        # --碰撞检测
        for pipe in pipe_sprites:
            if pygame.sprite.collide_mask(bird, pipe):
                sounds['hit'].play()
                is_game_running = False
        # --更新小鸟
        boundary_values = [0, base_pos[-1]]
        is_dead = bird.update(boundary_values, float(clock.tick(cfg.FPS))/1000.)
        if is_dead:
            sounds['hit'].play()
            is_game_running = False
        # --移动base实现小鸟往前飞的效果
        base_pos[0] = -((-base_pos[0] + 4) % base_diff_bg)
        # --移动pipe实现小鸟往前飞的效果
        flag = False
        for pipe in pipe_sprites:
            pipe.rect.left -= 4
            if pipe.rect.centerx < bird.rect.centerx and not pipe.used_for_score:
                pipe.used_for_score = True
                score += 0.5
                if '.5' in str(score):
                    sounds['point'].play()
            if pipe.rect.left < 5 and pipe.rect.left > 0 and is_add_pipe:
                pipe_pos = Pipe.randomPipe(cfg, pipe_images.get('top'))
                pipe_sprites.add(Pipe(image=pipe_images.get('top'), position=pipe_pos.get('top')))
                pipe_sprites.add(Pipe(image=pipe_images.get('bottom'), position=pipe_pos.get('bottom')))
                is_add_pipe = False
            elif pipe.rect.right < 0:
                pipe_sprites.remove(pipe)
                flag = True
        if flag: is_add_pipe = True
        # --绑定必要的元素在屏幕上
        screen.blit(backgroud_image, (0, 0))
        pipe_sprites.draw(screen)
        screen.blit(other_images['base'], base_pos)
        showScore(screen, score, number_images)
        bird.draw(screen)
        pygame.display.update()
        clock.tick(cfg.FPS)
    endGame(screen, sounds, showScore, score, number_images, bird, pipe_sprites, backgroud_image, other_images, base_pos, cfg)


'''run'''
if __name__ == '__main__':
    while True:
        main()