'''
Function:
    定义人机对战
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import pygame
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from itertools import product
from modules.misc.utils import *
from modules.misc.Buttons import *
from modules.misc.Chessman import *
from modules.ai.aiGobang import aiGobang


'''人机对战'''
class playWithAIUI(QWidget):
    back_signal = pyqtSignal()
    exit_signal = pyqtSignal()
    send_back_signal = False
    def __init__(self, cfg, parent=None, **kwargs):
        super(playWithAIUI, self).__init__(parent)
        self.cfg = cfg
        self.setFixedSize(760, 650)
        self.setWindowTitle('五子棋-微信公众号: Charles的皮卡丘')
        self.setWindowIcon(QIcon(cfg.ICON_FILEPATH))
        # 背景图片
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap(cfg.BACKGROUND_IMAGEPATHS.get('bg_game'))))
        self.setPalette(palette)
        # 按钮
        self.home_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('home'), self)
        self.home_button.click_signal.connect(self.goHome)
        self.home_button.move(680, 10)
        self.startgame_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('startgame'), self)
        self.startgame_button.click_signal.connect(self.startgame)
        self.startgame_button.move(640, 240)
        self.regret_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('regret'), self)
        self.regret_button.click_signal.connect(self.regret)
        self.regret_button.move(640, 310)
        self.givein_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('givein'), self)
        self.givein_button.click_signal.connect(self.givein)
        self.givein_button.move(640, 380)
        # 落子标志
        self.chessman_sign = QLabel(self)
        sign = QPixmap(cfg.CHESSMAN_IMAGEPATHS.get('sign'))
        self.chessman_sign.setPixmap(sign)
        self.chessman_sign.setFixedSize(sign.size())
        self.chessman_sign.show()
        self.chessman_sign.hide()
        # 棋盘(19*19矩阵)
        self.chessboard = [[None for i in range(19)] for _ in range(19)]
        # 历史记录(悔棋用)
        self.history_record = []
        # 是否在游戏中
        self.is_gaming = True
        # 胜利方
        self.winner = None
        self.winner_info_label = None
        # 颜色分配and目前轮到谁落子
        self.player_color = 'white'
        self.ai_color = 'black'
        self.whoseround = self.player_color
        # 实例化ai
        self.ai_player = aiGobang(self.ai_color, self.player_color)
        # 落子声音加载
        pygame.mixer.init()
        self.drop_sound = pygame.mixer.Sound(cfg.SOUNDS_PATHS.get('drop'))
    '''鼠标左键点击事件-玩家回合'''
    def mousePressEvent(self, event):
        if (event.buttons() != QtCore.Qt.LeftButton) or (self.winner is not None) or (self.whoseround != self.player_color) or (not self.is_gaming):
            return
        # 保证只在棋盘范围内响应
        if event.x() >= 50 and event.x() <= 50 + 30 * 18 + 14 and event.y() >= 50 and event.y() <= 50 + 30 * 18 + 14:
            pos = Pixel2Chesspos(event)
            # 保证落子的地方本来没有人落子
            if self.chessboard[pos[0]][pos[1]]:
                return
            # 实例化一个棋子并显示
            c = Chessman(self.cfg.CHESSMAN_IMAGEPATHS.get(self.whoseround), self)
            c.move(event.pos())
            c.show()
            self.chessboard[pos[0]][pos[1]] = c
            # 落子声音响起
            self.drop_sound.play()
            # 最后落子位置标志对落子位置进行跟随
            self.chessman_sign.show()
            self.chessman_sign.move(c.pos())
            self.chessman_sign.raise_()
            # 记录这次落子
            self.history_record.append([*pos, self.whoseround])
            # 是否胜利了
            self.winner = checkWin(self.chessboard)
            if self.winner:
                self.showGameEndInfo()
                return
            # 切换回合方(其实就是改颜色)
            self.nextRound()
    '''鼠标左键释放操作-调用电脑回合'''
    def mouseReleaseEvent(self, event):
        if (self.winner is not None) or (self.whoseround != self.ai_color) or (not self.is_gaming):
            return
        self.aiAct()
    '''电脑自动下-AI回合'''
    def aiAct(self):
        if (self.winner is not None) or (self.whoseround == self.player_color) or (not self.is_gaming):
            return
        next_pos = self.ai_player.act(self.history_record)
        # 实例化一个棋子并显示
        c = Chessman(self.cfg.CHESSMAN_IMAGEPATHS.get(self.whoseround), self)
        c.move(QPoint(*Chesspos2Pixel(next_pos)))
        c.show()
        self.chessboard[next_pos[0]][next_pos[1]] = c
        # 落子声音响起
        self.drop_sound.play()
        # 最后落子位置标志对落子位置进行跟随
        self.chessman_sign.show()
        self.chessman_sign.move(c.pos())
        self.chessman_sign.raise_()
        # 记录这次落子
        self.history_record.append([*next_pos, self.whoseround])
        # 是否胜利了
        self.winner = checkWin(self.chessboard)
        if self.winner:
            self.showGameEndInfo()
            return
        # 切换回合方(其实就是改颜色)
        self.nextRound()
    '''改变落子方'''
    def nextRound(self):
        self.whoseround = self.player_color if self.whoseround == self.ai_color else self.ai_color
    '''显示游戏结束结果'''
    def showGameEndInfo(self):
        self.is_gaming = False
        info_img = QPixmap(self.cfg.WIN_IMAGEPATHS.get(self.winner))
        self.winner_info_label = QLabel(self)
        self.winner_info_label.setPixmap(info_img)
        self.winner_info_label.resize(info_img.size())
        self.winner_info_label.move(50, 50)
        self.winner_info_label.show()
    '''认输'''
    def givein(self):
        if self.is_gaming and (self.winner is None) and (self.whoseround == self.player_color):
            self.winner = self.ai_color
            self.showGameEndInfo()
    '''悔棋-只有我方回合的时候可以悔棋'''
    def regret(self):
        if (self.winner is not None) or (len(self.history_record) == 0) or (not self.is_gaming) and (self.whoseround != self.player_color):
            return
        for _ in range(2):
            pre_round = self.history_record.pop(-1)
            self.chessboard[pre_round[0]][pre_round[1]].close()
            self.chessboard[pre_round[0]][pre_round[1]] = None
        self.chessman_sign.hide()
    '''开始游戏-之前的对弈必须已经结束才行'''
    def startgame(self):
        if self.is_gaming:
            return
        self.is_gaming = True
        self.whoseround = self.player_color
        for i, j in product(range(19), range(19)):
            if self.chessboard[i][j]:
                self.chessboard[i][j].close()
                self.chessboard[i][j] = None
        self.winner = None
        self.winner_info_label.close()
        self.winner_info_label = None
        self.history_record.clear()
        self.chessman_sign.hide()
    '''关闭窗口事件'''
    def closeEvent(self, event):
        if not self.send_back_signal:
            self.exit_signal.emit()
    '''返回游戏主页面'''
    def goHome(self):
        self.send_back_signal = True
        self.close()
        self.back_signal.emit()