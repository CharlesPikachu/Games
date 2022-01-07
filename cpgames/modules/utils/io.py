'''
Function:
    IO读取相关的工具
Author: 
    Charles
微信公众号: 
    Charles的皮卡丘
'''
import pygame


'''基于pygame的游戏导入游戏素材'''
class PygameResourceLoader():
    def __init__(self, image_paths_dict=None, sound_paths_dict=None, font_paths_dict=None, bgm_path=None, **kwargs):
        # 设置属性
        self.bgm_path = bgm_path
        self.font_paths_dict = font_paths_dict
        self.image_paths_dict = image_paths_dict
        self.sound_paths_dict = sound_paths_dict
        # 导入字体
        self.fonts = self.fontload(font_paths_dict)
        # 导入图像
        self.images = self.defaultload(image_paths_dict, pygame.image.load)
        # 导入声音
        self.sounds = self.defaultload(sound_paths_dict, pygame.mixer.Sound)
    '''默认的素材导入函数'''
    def defaultload(self, resources_dict, load_func):
        if resources_dict is None: return dict()
        assert isinstance(resources_dict, dict)
        resources = dict()
        for key, value in resources_dict.items():
            if isinstance(value, dict):
                resources[key] = self.defaultload(value, load_func)
            elif isinstance(value, list):
                resources[key] = list()
                for path in value: resources[key].append(load_func(path))
            else:
                resources[key] = load_func(value)
        return resources
    '''导入字体'''
    def fontload(self, font_paths_dict):
        if font_paths_dict is None: return dict()
        assert isinstance(font_paths_dict, dict)
        fonts = dict()
        for key, value in font_paths_dict.items():
            if not value.get('system_font', False):
                fonts[key] = pygame.font.Font(value['name'], value['size'])
            else:
                fonts[key] = pygame.font.SysFont(value['name'], value['size'])
        return fonts
    '''播放背景音乐'''
    def playbgm(self):
        pygame.mixer.music.load(self.bgm_path)
        pygame.mixer.music.play(-1, 0.0)