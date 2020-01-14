'''配置文件'''
import os


CURPATH = os.getcwd()
SCREENSIZE = (993, 477)
HAMMER_IMAGEPATHS = [os.path.join(CURPATH, 'resources/images/hammer0.png'), os.path.join(CURPATH, 'resources/images/hammer1.png')]
GAME_BEGIN_IMAGEPATHS = [os.path.join(CURPATH, 'resources/images/begin.png'), os.path.join(CURPATH, 'resources/images/begin1.png')]
GAME_AGAIN_IMAGEPATHS = [os.path.join(CURPATH, 'resources/images/again1.png'), os.path.join(CURPATH, 'resources/images/again2.png')]
GAME_BG_IMAGEPATH = os.path.join(CURPATH, 'resources/images/background.png')
GAME_END_IMAGEPATH = os.path.join(CURPATH, 'resources/images/end.png')
MOLE_IMAGEPATHS = [os.path.join(CURPATH, 'resources/images/mole_1.png'), os.path.join(CURPATH, 'resources/images/mole_laugh1.png'),
                   os.path.join(CURPATH, 'resources/images/mole_laugh2.png'), os.path.join(CURPATH, 'resources/images/mole_laugh3.png')]
HOLE_POSITIONS = [(90, -20), (405, -20), (720, -20), (90, 140), (405, 140), (720, 140), (90, 290), (405, 290), (720, 290)]
BGM_PATH = 'resources/audios/bgm.mp3'
COUNT_DOWN_SOUND_PATH = 'resources/audios/count_down.wav'
HAMMERING_SOUND_PATH = 'resources/audios/hammering.wav'
FONT_PATH = 'resources/font/Gabriola.ttf'
BROWN = (150, 75, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
RECORD_PATH = 'score.rec'