'''
Function:
    游戏结束界面
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import pygame


'''游戏结束画面'''
def showEndGameInterface(screen, cfg, score, highest_score):
    # 显示的文本信息设置
    font_big = pygame.font.Font(cfg.FONT_PATH, 60)
    font_small = pygame.font.Font(cfg.FONT_PATH, 40)
    text_title = font_big.render(f"Time is up!", True, (255, 0, 0))
    text_title_rect = text_title.get_rect()
    text_title_rect.centerx = screen.get_rect().centerx
    text_title_rect.centery = screen.get_rect().centery - 100
    text_score = font_small.render(f"Score: {score}, Highest Score: {highest_score}", True, (255, 0, 0))
    text_score_rect = text_score.get_rect()
    text_score_rect.centerx = screen.get_rect().centerx
    text_score_rect.centery = screen.get_rect().centery - 10
    text_tip = font_small.render(f"Enter Q to quit game or Enter R to restart game", True, (255, 0, 0))
    text_tip_rect = text_tip.get_rect()
    text_tip_rect.centerx = screen.get_rect().centerx
    text_tip_rect.centery = screen.get_rect().centery + 60
    text_tip_count = 0
    text_tip_freq = 10
    text_tip_show_flag = True
    # 界面主循环
    clock = pygame.time.Clock()
    while True:
        screen.fill(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                elif event.key == pygame.K_r:
                    return True
        screen.blit(text_title, text_title_rect)
        screen.blit(text_score, text_score_rect)
        if text_tip_show_flag:
            screen.blit(text_tip, text_tip_rect)
        text_tip_count += 1
        if text_tip_count % text_tip_freq == 0:
            text_tip_count = 0
            text_tip_show_flag = not text_tip_show_flag
        pygame.display.flip()
        clock.tick(cfg.FPS)