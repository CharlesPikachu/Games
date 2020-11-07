'''配置文件'''
import os


'''图片素材路径'''
IMAGE_PATHS = {
    'gold': os.path.join(os.getcwd(), 'resources/images/gold.png'),
    'apple': os.path.join(os.getcwd(), 'resources/images/apple.png'),
    'background': os.path.join(os.getcwd(), 'resources/images/background.jpg'),
    'hero': [os.path.join(os.getcwd(), 'resources/images/%d.png' % i) for i in range(1, 11)],
}
'''音频素材路径'''
AUDIO_PATHS = {
    'bgm': os.path.join(os.getcwd(), 'resources/audios/bgm.mp3'),
    'get': os.path.join(os.getcwd(), 'resources/audios/get.wav'),
}
'''字体路径'''
FONT_PATH = os.path.join(os.getcwd(), 'resources/font/font.TTF')
'''最高分记录的路径'''
HIGHEST_SCORE_RECORD_FILEPATH = 'highest.rec'
'''游戏屏幕大小'''
SCREENSIZE = (800, 600)
'''背景颜色'''
BACKGROUND_COLOR = (0, 160, 233)
'''fps'''
FPS = 30