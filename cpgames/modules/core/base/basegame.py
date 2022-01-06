'''
Function:
    游戏基类
Author: 
    Charles
微信公众号: 
    Charles的皮卡丘
'''
import pygame
from ...utils import InitPygame, PygameResourceLoader


'''Pygame的游戏基类'''
class PygameBaseGame():
    def __init__(self, config, **kwargs):
        # 设置属性
        self.config = config
        # 初始化
        self.initialize()
        # 用户可以覆盖默认参数
        for key, value in kwargs.items():
            if hasattr(self, key): setattr(self, key, value)
    '''运行游戏'''
    def run(self):
        raise NotImplementedError('not to be implemented...')
    '''初始化'''
    def initialize(self):
        self.screen = InitPygame(screensize=self.config.SCREENSIZE, title=self.config.TITLE)
        bgm_path = self.config.BGM_PATH if hasattr(self.config, 'BGM_PATH') else None
        font_paths_dict = self.config.FONT_PATHS_DICT if hasattr(self.config, 'FONT_PATHS_DICT') else None
        image_paths_dict = self.config.IMAGE_PATHS_DICT if hasattr(self.config, 'IMAGE_PATHS_DICT') else None
        sound_paths_dict = self.config.SOUND_PATHS_DICT if hasattr(self.config, 'SOUND_PATHS_DICT') else None
        self.resource_loader = PygameResourceLoader(
            bgm_path=bgm_path,
            font_paths_dict=font_paths_dict, 
            image_paths_dict=image_paths_dict, 
            sound_paths_dict=sound_paths_dict, 
        )