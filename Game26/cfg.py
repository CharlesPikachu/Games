'''配置文件'''
import os


'''图片路径'''
IMAGEPATHS = {
    'pig': [
        os.path.join(os.getcwd(), 'resources/images/pig_1.png'),
        os.path.join(os.getcwd(), 'resources/images/pig_2.png'),
        os.path.join(os.getcwd(), 'resources/images/pig_damaged.png'),
    ],
    'bird': [
        os.path.join(os.getcwd(), 'resources/images/bird.png'),
    ],
    'wall': [
        os.path.join(os.getcwd(), 'resources/images/wall_horizontal.png'),
        os.path.join(os.getcwd(), 'resources/images/wall_vertical.png'),
    ],
    'block': [
        os.path.join(os.getcwd(), 'resources/images/block.png'),
        os.path.join(os.getcwd(), 'resources/images/block_destroyed.png'),
    ]
}
'''字体路径'''
FONTPATH = {
    'Comic_Kings': os.path.join(os.getcwd(), 'resources/fonts/Comic_Kings.ttf'),
    'arfmoochikncheez': os.path.join(os.getcwd(), 'resources/fonts/arfmoochikncheez.ttf'),
}
'''背景音乐路径'''
BGMPATH = os.path.join(os.getcwd(), 'resources/audios/bgm.ogg')
'''屏幕大小'''
SCREENSIZE = (1800, 700)
'''fps'''
FPS = 60
'''一些颜色定义'''
BACKGROUND_COLOR = (51, 51, 51)