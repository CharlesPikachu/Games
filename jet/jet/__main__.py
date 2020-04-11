import pygame
import random

from pygame.locals import (
    RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FPS = 20

ADDENEMY = pygame.USEREVENT + 1
ENEMY_SPEED = 250
ADDCLOUD = pygame.USEREVENT + 2
CLOUD_SPEED = 1000

pygame.mixer.init()
MOVE_UP_SOUND = pygame.mixer.Sound("audio/Rising_putter.ogg")
MOVE_DOWN_SOUND = pygame.mixer.Sound("audio/Falling_putter.ogg")
COLLISION_SOUND = pygame.mixer.Sound("audio/Collision.ogg")
SUCCEED_SOUND = pygame.mixer.Sound('audio/succeed.ogg')

def main():
    pygame.init()

    # Load and play background music
    pygame.mixer.music.load("audio/Apoxode_-_Electric_1.mp3")
    pygame.mixer.music.play(loops=-1)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Custom Events at fixed time interval
    pygame.time.set_timer(ADDENEMY, ENEMY_SPEED)
    pygame.time.set_timer(ADDCLOUD, CLOUD_SPEED)

    # Setup the clock for a decent framerate
    clock = pygame.time.Clock()
    
    player = Player()
    enemies = pygame.sprite.Group()
    clouds = pygame.sprite.Group()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    running = True
    while running:
        for event in pygame.event.get():
            if (event.type == KEYDOWN and event.key == K_ESCAPE) or (event.type == QUIT):
                running = False
            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            elif event.type == ADDCLOUD:
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)
        
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        enemies.update()
        clouds.update()

        screen.fill((135, 206, 250))
        
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        
        if pygame.sprite.spritecollideany(player, enemies):
            MOVE_UP_SOUND.stop()
            MOVE_DOWN_SOUND.stop()
            COLLISION_SOUND.play()
            player.kill()
            pygame.time.wait(5000)
            running = False
        
        if player.rect.right == SCREEN_WIDTH:
            MOVE_UP_SOUND.stop()
            MOVE_DOWN_SOUND.stop()
            SUCCEED_SOUND.play()
            pygame.time.wait(5000)
            running = False

        pygame.display.flip()
        clock.tick(FPS)
    
    # All done! Stop and quit the mixer.
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    pygame.quit()


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("./images/jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
    
    def update(self, keys):
        dist = {
            K_UP: (0, -5), K_DOWN: (0, 5), K_LEFT: (-5, 0), K_RIGHT: (5, 0)
        }
        for dir, dis in dist.items():
            if keys[dir]:
                self.rect.move_ip(dis)
                if dir == K_UP:
                    MOVE_UP_SOUND.play()
                elif dir == K_DOWN:
                    MOVE_DOWN_SOUND.play()
        
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, SCREEN_WIDTH)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, SCREEN_HEIGHT)


class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("./images/missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT - self.surf.get_height())
            )
        )
        self.speed = random.randint(5, 20)
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Cloud(pygame.sprite.Sprite):

    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("./images/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT - self.surf.get_height())
            )
        )
    
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


if __name__ == '__main__':
    main()
