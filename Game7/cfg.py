'''配置文件'''
import os


'''屏幕大小'''
SCREENSIZE = (600, 150)
'''FPS'''
FPS = 60
'''音频素材路径'''
AUDIO_PATHS = {
	'die': os.path.join(os.getcwd(), 'resources/audios/die.wav'),
	'jump': os.path.join(os.getcwd(), 'resources/audios/jump.wav'),
	'point': os.path.join(os.getcwd(), 'resources/audios/point.wav')
}
'''图片素材路径'''
IMAGE_PATHS = {
	'cacti': [os.path.join(os.getcwd(), 'resources/images/cacti-big.png'),
			  os.path.join(os.getcwd(), 'resources/images/cacti-small.png')],
	'cloud': os.path.join(os.getcwd(), 'resources/images/cloud.png'),
	'dino': [os.path.join(os.getcwd(), 'resources/images/dino.png'),
			 os.path.join(os.getcwd(), 'resources/images/dino_ducking.png')],
	'gameover': os.path.join(os.getcwd(), 'resources/images/gameover.png'),
	'ground': os.path.join(os.getcwd(), 'resources/images/ground.png'),
	'numbers': os.path.join(os.getcwd(), 'resources/images/numbers.png'),
	'ptera': os.path.join(os.getcwd(), 'resources/images/ptera.png'),
	'replay': os.path.join(os.getcwd(), 'resources/images/replay.png')
}
'''背景颜色'''
BACKGROUND_COLOR = (235, 235, 235)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)