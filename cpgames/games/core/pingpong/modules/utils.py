'''
Function:
    工具函数
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import pygame


'''导入图片'''
def loadImage(imgpath, transparent=True):
    img = pygame.image.load(imgpath)
    img = img.convert()
    if transparent:
        color = img.get_at((0, 0))
        img.set_colorkey(color, pygame.RLEACCEL)
    return img