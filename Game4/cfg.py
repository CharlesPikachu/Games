'''配置文件'''
import os


'''FPS'''
FPS = 40
'''游戏屏幕大小'''
SCREENSIZE = (640, 640)
'''图片路径'''
SKIER_IMAGE_PATHS = [
    os.path.join(os.getcwd(), 'resources/images/skier_forward.png'),
    os.path.join(os.getcwd(), 'resources/images/skier_right1.png'),
    os.path.join(os.getcwd(), 'resources/images/skier_right2.png'),
    os.path.join(os.getcwd(), 'resources/images/skier_left2.png'),
    os.path.join(os.getcwd(), 'resources/images/skier_left1.png'),
    os.path.join(os.getcwd(), 'resources/images/skier_fall.png')
]
OBSTACLE_PATHS = {
    'tree': os.path.join(os.getcwd(), 'resources/images/tree.png'),
    'flag': os.path.join(os.getcwd(), 'resources/images/flag.png')
}
'''背景音乐路径'''
BGMPATH = os.path.join(os.getcwd(), 'resources/music/bgm.mp3')
'''字体路径'''
FONTPATH = os.path.join(os.getcwd(), 'resources/font/FZSTK.TTF')