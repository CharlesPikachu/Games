'''配置文件'''
import os


WIDTH = 500
HEIGHT = 500
CURRPATH = os.path.abspath(os.path.dirname(__file__))
RESOURCESDIRPATH = os.path.join(CURRPATH, 'resources')
AUDIOSDIRPATH = os.path.join(RESOURCESDIRPATH, 'audios')
FONTDIRPATH = os.path.join(RESOURCESDIRPATH, 'font')
IMAGESDIRPATH = os.path.join(RESOURCESDIRPATH, 'images')
BALLPICPATH = os.path.join(IMAGESDIRPATH, 'ball.png')
RACKETPICPATH = os.path.join(IMAGESDIRPATH, 'racket.png')
FONTPATH = os.path.join(FONTDIRPATH, 'font.TTF')
GOALSOUNDPATH = os.path.join(AUDIOSDIRPATH, 'goal.wav')
HITSOUNDPATH = os.path.join(AUDIOSDIRPATH, 'hit.wav')
BGMPATH = os.path.join(AUDIOSDIRPATH, 'bgm.mp3')
WHITE = (255, 255, 255)