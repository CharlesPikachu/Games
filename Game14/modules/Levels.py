'''
Function:
    定义关卡
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import pygame
from .Sprites import *


'''关卡数量'''
NUMLEVELS = 1


'''关卡一'''
class Level1():
    def __init__(self):
        self.info = 'level1'
    '''创建墙'''
    def setupWalls(self, wall_color):
        self.wall_sprites = pygame.sprite.Group()
        wall_positions = [
            [0, 0, 6, 600], [0, 0, 600, 6], [0, 600, 606, 6], [600, 0, 6, 606], [300, 0, 6, 66], [60, 60, 186, 6],
            [360, 60, 186, 6], [60, 120, 66, 6], [60, 120, 6, 126], [180, 120, 246, 6], [300, 120, 6, 66],
            [480, 120, 66, 6], [540, 120, 6, 126], [120, 180, 126, 6], [120, 180, 6, 126], [360, 180, 126, 6],
            [480, 180, 6, 126], [180, 240, 6, 126], [180, 360, 246, 6], [420, 240, 6, 126], [240, 240, 42, 6],
            [324, 240, 42, 6], [240, 240, 6, 66], [240, 300, 126, 6], [360, 240, 6, 66], [0, 300, 66, 6],
            [540, 300, 66, 6], [60, 360, 66, 6], [60, 360, 6, 186], [480, 360, 66, 6], [540, 360, 6, 186],
            [120, 420, 366, 6], [120, 420, 6, 66], [480, 420, 6, 66], [180, 480, 246, 6], [300, 480, 6, 66],
            [120, 540, 126, 6], [360, 540, 126, 6]
        ]
        for wall_position in wall_positions:
            wall = Wall(*wall_position, wall_color)
            self.wall_sprites.add(wall)
        return self.wall_sprites
    '''创建门'''
    def setupGate(self, gate_color):
        self.gate_sprites = pygame.sprite.Group()
        self.gate_sprites.add(Wall(282, 242, 42, 2, gate_color))
        return self.gate_sprites
    '''创建角色'''
    def setupPlayers(self, hero_image_path, ghost_images_path):
        self.hero_sprites = pygame.sprite.Group()
        self.ghost_sprites = pygame.sprite.Group()
        self.hero_sprites.add(Player(287, 439, hero_image_path))
        for each in ghost_images_path:
            role_name = each.split('/')[-1].split('.')[0]
            if role_name == 'Blinky':
                player = Player(287, 199, each)
                player.is_move = True
                player.tracks = [
                    [0, -0.5, 4], [0.5, 0, 9], [0, 0.5, 11], [0.5, 0, 3], [0, 0.5, 7], [-0.5, 0, 11], [0, 0.5, 3],
                    [0.5, 0, 15], [0, -0.5, 15], [0.5, 0, 3], [0, -0.5, 11], [-0.5, 0, 3], [0, -0.5, 11], [-0.5, 0, 3],
                    [0, -0.5, 3], [-0.5, 0, 7], [0, -0.5, 3], [0.5, 0, 15], [0, 0.5, 15], [-0.5, 0, 3], [0, 0.5, 3],
                    [-0.5, 0, 3], [0, -0.5, 7], [-0.5, 0, 3], [0, 0.5, 7], [-0.5, 0, 11], [0, -0.5, 7], [0.5, 0, 5]
                ]
                self.ghost_sprites.add(player)
            elif role_name == 'Clyde':
                player = Player(319, 259, each)
                player.is_move = True
                player.tracks = [
                    [-1, 0, 2], [0, -0.5, 4], [0.5, 0, 5], [0, 0.5, 7], [-0.5, 0, 11], [0, -0.5, 7],
                    [-0.5, 0, 3], [0, 0.5, 7], [-0.5, 0, 7], [0, 0.5, 15], [0.5, 0, 15], [0, -0.5, 3],
                    [-0.5, 0, 11], [0, -0.5, 7], [0.5, 0, 3], [0, -0.5, 11], [0.5, 0, 9]
                ]
                self.ghost_sprites.add(player)
            elif role_name == 'Inky':
                player = Player(255, 259, each)
                player.is_move = True
                player.tracks = [
                    [1, 0, 2], [0, -0.5, 4], [0.5, 0, 10], [0, 0.5, 7], [0.5, 0, 3], [0, -0.5, 3],
                    [0.5, 0, 3], [0, -0.5, 15], [-0.5, 0, 15], [0, 0.5, 3], [0.5, 0, 15], [0, 0.5, 11],
                    [-0.5, 0, 3], [0, -0.5, 7], [-0.5, 0, 11], [0, 0.5, 3], [-0.5, 0, 11], [0, 0.5, 7],
                    [-0.5, 0, 3], [0, -0.5, 3], [-0.5, 0, 3], [0, -0.5, 15], [0.5, 0, 15], [0, 0.5, 3],
                    [-0.5, 0, 15], [0, 0.5, 11], [0.5, 0, 3], [0, -0.5, 11], [0.5, 0, 11], [0, 0.5, 3], [0.5, 0, 1]
                ]
                self.ghost_sprites.add(player)
            elif role_name == 'Pinky':
                player = Player(287, 259, each)
                player.is_move = True
                player.tracks = [
                    [0, -1, 4], [0.5, 0, 9], [0, 0.5, 11], [-0.5, 0, 23], [0, 0.5, 7], [0.5, 0, 3],
                    [0, -0.5, 3], [0.5, 0, 19], [0, 0.5, 3], [0.5, 0, 3], [0, 0.5, 3], [0.5, 0, 3],
                    [0, -0.5, 15], [-0.5, 0, 7], [0, 0.5, 3], [-0.5, 0, 19], [0, -0.5, 11], [0.5, 0, 9]
                ]
                self.ghost_sprites.add(player)
        return self.hero_sprites, self.ghost_sprites
    '''创建食物'''
    def setupFood(self, food_color, bg_color):
        self.food_sprites = pygame.sprite.Group()
        for row in range(19):
            for col in range(19):
                if (row == 7 or row == 8) and (col == 8 or col == 9 or col == 10):
                    continue
                else:
                    food = Food(30 * col + 32, 30 * row + 32, 4, 4, food_color, bg_color)
                    is_collide = pygame.sprite.spritecollide(food, self.wall_sprites, False)
                    if is_collide:
                        continue
                    is_collide = pygame.sprite.spritecollide(food, self.hero_sprites, False)
                    if is_collide:
                        continue
                    self.food_sprites.add(food)
        return self.food_sprites