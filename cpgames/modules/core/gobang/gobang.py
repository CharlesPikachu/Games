'''
Function:
    五子棋小游戏-支持人机和局域网对战
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import sys
from .modules import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


'''配置类'''
class Config():
    # 根目录
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # 图标路径
    ICON_FILEPATH = os.path.join(rootdir, 'resources/images/icon/icon.ico')
    # 背景图片路径
    BACKGROUND_IMAGEPATHS = {
        'bg_game': os.path.join(rootdir, 'resources/images/bg/bg_game.png'),
        'bg_start': os.path.join(rootdir, 'resources/images/bg/bg_start.png')
    }
    # 按钮图片路径
    BUTTON_IMAGEPATHS = {
        'online': [
            os.path.join(rootdir, 'resources/images/buttons/online_0.png'),
            os.path.join(rootdir, 'resources/images/buttons/online_1.png'),
            os.path.join(rootdir, 'resources/images/buttons/online_2.png')
        ],
        'ai': [
            os.path.join(rootdir, 'resources/images/buttons/ai_0.png'),
            os.path.join(rootdir, 'resources/images/buttons/ai_1.png'),
            os.path.join(rootdir, 'resources/images/buttons/ai_2.png')
        ],
        'home': [
            os.path.join(rootdir, 'resources/images/buttons/home_0.png'),
            os.path.join(rootdir, 'resources/images/buttons/home_1.png'),
            os.path.join(rootdir, 'resources/images/buttons/home_2.png')
        ],
        'givein': [
            os.path.join(rootdir, 'resources/images/buttons/givein_0.png'),
            os.path.join(rootdir, 'resources/images/buttons/givein_1.png'),
            os.path.join(rootdir, 'resources/images/buttons/givein_2.png')
        ],
        'regret': [
            os.path.join(rootdir, 'resources/images/buttons/regret_0.png'),
            os.path.join(rootdir, 'resources/images/buttons/regret_1.png'),
            os.path.join(rootdir, 'resources/images/buttons/regret_2.png')
        ],
        'startgame': [
            os.path.join(rootdir, 'resources/images/buttons/startgame_0.png'),
            os.path.join(rootdir, 'resources/images/buttons/startgame_1.png'),
            os.path.join(rootdir, 'resources/images/buttons/startgame_2.png')
        ],
        'urge': [
            os.path.join(rootdir, 'resources/images/buttons/urge_0.png'),
            os.path.join(rootdir, 'resources/images/buttons/urge_1.png'),
            os.path.join(rootdir, 'resources/images/buttons/urge_2.png')
        ]
    }
    # 显示胜利图片路径
    WIN_IMAGEPATHS = {
        'black': os.path.join(rootdir, 'resources/images/win/black_win.png'),
        'white': os.path.join(rootdir, 'resources/images/win/white_win.png'),
        'draw': os.path.join(rootdir, 'resources/images/win/draw.png')
    }
    # 棋子图片路径
    CHESSMAN_IMAGEPATHS = {
        'black': os.path.join(rootdir, 'resources/images/chessman/black.png'),
        'white': os.path.join(rootdir, 'resources/images/chessman/white.png'),
        'sign': os.path.join(rootdir, 'resources/images/chessman/sign.png'),
    }
    # 音效
    SOUNDS_PATHS = {
        'drop': os.path.join(rootdir, 'resources/audios/drop.wav'),
        'urge': os.path.join(rootdir, 'resources/audios/urge.wav')
    }
    # 端口号(联机对战时使用)
    PORT = 3333


'''游戏开始界面'''
class GobangGame(QWidget):
    game_type = 'gobang'
    def __init__(self, parent=None, **kwargs):
        super(GobangGame, self).__init__(parent)
        self.cfg = Config
        self.setFixedSize(760, 650)
        self.setWindowTitle('五子棋小游戏 —— Charles的皮卡丘')
        self.setWindowIcon(QIcon(self.cfg.ICON_FILEPATH))
        # 背景图片
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap(self.cfg.BACKGROUND_IMAGEPATHS.get('bg_start'))))
        self.setPalette(palette)
        # 按钮
        # --人机对战
        self.ai_button = PushButton(self.cfg.BUTTON_IMAGEPATHS.get('ai'), self)
        self.ai_button.move(250, 200)
        self.ai_button.show()
        self.ai_button.click_signal.connect(self.playWithAI)
        # --联机对战
        self.online_button = PushButton(self.cfg.BUTTON_IMAGEPATHS.get('online'), self)
        self.online_button.move(250, 350)
        self.online_button.show()
        self.online_button.click_signal.connect(self.playOnline)
    '''人机对战'''
    def playWithAI(self):
        self.close()
        self.gaming_ui = PlayWithAIUI(self.cfg)
        self.gaming_ui.exit_signal.connect(lambda: sys.exit())
        self.gaming_ui.back_signal.connect(self.show)
        self.gaming_ui.show()
    '''联机对战'''
    def playOnline(self):
        self.close()
        self.gaming_ui = PlayOnlineUI(self.cfg, self)
        self.gaming_ui.show()