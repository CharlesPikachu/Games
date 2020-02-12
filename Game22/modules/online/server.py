'''
Function:
    联机对战服务器端
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import socket
import pygame
import random
import threading
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from itertools import product
from modules.misc.utils import *
from modules.misc.Buttons import *
from modules.misc.Chessman import *


'''服务器端'''
class gobangSever(QWidget):
    back_signal = pyqtSignal()
    exit_signal = pyqtSignal()
    receive_signal = pyqtSignal(dict, name='data')
    send_back_signal = False
    def __init__(self, cfg, nickname, parent=None, **kwargs):
        super(gobangSever, self).__init__(parent)
        # 预定义一些必要的变量
        self.cfg = cfg
        self.nickname = nickname
        self.opponent_nickname = None
        self.client_ipport = None
        self.is_gaming = False
        self.chessboard = [[None for i in range(19)] for _ in range(19)]
        self.history_record = []
        self.winner = None
        self.winner_info_label = None
        self.player_color = 'white'
        self.opponent_player_color = 'black'
        self.whoseround = None
        # 当前窗口的基本设置
        self.setFixedSize(760, 650)
        self.setWindowTitle('五子棋-微信公众号: Charles的皮卡丘')
        self.setWindowIcon(QIcon(cfg.ICON_FILEPATH))
        # 背景图片
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap(cfg.BACKGROUND_IMAGEPATHS.get('bg_game'))))
        self.setPalette(palette)
        # 显示你的昵称
        self.nickname_label = QLabel('您是%s' % self.nickname, self)
        self.nickname_label.resize(200, 40)
        self.nickname_label.move(640, 180)
        # 落子标志
        self.chessman_sign = QLabel(self)
        sign = QPixmap(cfg.CHESSMAN_IMAGEPATHS.get('sign'))
        self.chessman_sign.setPixmap(sign)
        self.chessman_sign.setFixedSize(sign.size())
        self.chessman_sign.show()
        self.chessman_sign.hide()
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
        self.urge_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('urge'), self)
        self.urge_button.click_signal.connect(self.urge)
        self.urge_button.move(640, 450)
        # 落子和催促声音加载
        pygame.mixer.init()
        self.drop_sound = pygame.mixer.Sound(cfg.SOUNDS_PATHS.get('drop'))
        self.urge_sound = pygame.mixer.Sound(cfg.SOUNDS_PATHS.get('urge'))
        # 接收数据信号绑定到responseForReceiveData函数
        self.receive_signal.connect(self.responseForReceiveData)
        # TCP/IP服务器
        self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server.bind(('0.0.0.0', cfg.PORT))
        self.tcp_server.listen(1)
        # TCP/IP的socket
        self.tcp_socket = None
        # 开一个线程进行监听
        threading.Thread(target=self.startListen).start()
    '''返回游戏主界面'''
    def goHome(self):
        self.send_back_signal = True
        self.close()
        self.back_signal.emit()
    '''开始游戏'''
    def startgame(self):
        if self.tcp_socket is None:
            QMessageBox.information(self, '提示', '对方未连接, 请耐心等待')
        else:
            self.randomAssignColor()
            data = {'type': 'action', 'detail': 'startgame', 'data': [self.player_color, self.opponent_player_color]}
            self.tcp_socket.sendall(packSocketData(data))
            QMessageBox.information(self, '提示', '游戏开始请求已发送, 等待对方确定中')
    '''认输'''
    def givein(self):
        if self.tcp_socket and self.is_gaming and (self.winner is None) and (self.whoseround == self.player_color):
            self.winner = self.opponent_player_color
            self.showGameEndInfo()
            data = {'type': 'action', 'detail': 'givein'}
            self.tcp_socket.sendall(packSocketData(data))
    '''悔棋-只有在对方回合才能悔棋'''
    def regret(self):
        if self.tcp_socket and self.is_gaming and (self.winner is None) and (self.whoseround == self.opponent_player_color):
            data = {'type': 'action', 'detail': 'regret'}
            self.tcp_socket.sendall(packSocketData(data))
    '''催促'''
    def urge(self):
        if self.tcp_socket and self.is_gaming and (self.winner is None) and (self.whoseround == self.opponent_player_color):
            data = {'type': 'action', 'detail': 'urge'}
            self.tcp_socket.sendall(packSocketData(data))
            self.urge_sound.play()
    '''鼠标左键点击事件-玩家回合'''
    def mousePressEvent(self, event):
        if (self.tcp_socket is None) or (event.buttons() != QtCore.Qt.LeftButton) or (self.winner is not None) or (self.whoseround != self.player_color) or (not self.is_gaming):
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
            # 发送给对方自己的落子位置
            data = {'type': 'action', 'detail': 'drop', 'data': pos}
            self.tcp_socket.sendall(packSocketData(data))
            # 是否胜利了
            self.winner = checkWin(self.chessboard)
            if self.winner:
                self.showGameEndInfo()
                return
            # 切换回合方(其实就是改颜色)
            self.nextRound()
    '''显示游戏结束结果'''
    def showGameEndInfo(self):
        self.is_gaming = False
        info_img = QPixmap(self.cfg.WIN_IMAGEPATHS.get(self.winner))
        self.winner_info_label = QLabel(self)
        self.winner_info_label.setPixmap(info_img)
        self.winner_info_label.resize(info_img.size())
        self.winner_info_label.move(50, 50)
        self.winner_info_label.show()
    '''响应接收到的数据'''
    def responseForReceiveData(self, data):
        if data['type'] == 'action' and data['detail'] == 'exit':
            QMessageBox.information(self, '提示', '您的对手已退出游戏, 游戏将自动返回主界面')
            self.goHome()
        elif data['type'] == 'action' and data['detail'] == 'startgame':
            self.opponent_player_color, self.player_color = data['data']
            self.whoseround = 'white'
            self.whoseround2nickname_dict = {self.player_color: self.nickname, self.opponent_player_color: self.opponent_nickname}
            res = QMessageBox.information(self, '提示', '对方请求(重新)开始游戏, 您为%s, 您是否同意?' % {'white': '白子', 'black': '黑子'}.get(self.player_color), QMessageBox.Yes | QMessageBox.No)
            if res == QMessageBox.Yes:
                data = {'type': 'reply', 'detail': 'startgame', 'data': True}
                self.tcp_socket.sendall(packSocketData(data))
                self.is_gaming = True
                self.setWindowTitle('五子棋-微信公众号: Charles的皮卡丘 ——> %s走棋' % self.whoseround2nickname_dict.get(self.whoseround))
                for i, j in product(range(19), range(19)):
                    if self.chessboard[i][j]:
                        self.chessboard[i][j].close()
                        self.chessboard[i][j] = None
                self.history_record.clear()
                self.winner = None
                if self.winner_info_label:
                    self.winner_info_label.close()
                self.winner_info_label = None
                self.chessman_sign.hide()
            else:
                data = {'type': 'reply', 'detail': 'startgame', 'data': False}
                self.tcp_socket.sendall(packSocketData(data))
        elif data['type'] == 'action' and data['detail'] == 'drop':
            pos = data['data']
            # 实例化一个棋子并显示
            c = Chessman(self.cfg.CHESSMAN_IMAGEPATHS.get(self.whoseround), self)
            c.move(QPoint(*Chesspos2Pixel(pos)))
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
        elif data['type'] == 'action' and data['detail'] == 'givein':
            self.winner = self.player_color
            self.showGameEndInfo()
        elif data['type'] == 'action' and data['detail'] == 'urge':
            self.urge_sound.play()
        elif data['type'] == 'action' and data['detail'] == 'regret':
            res = QMessageBox.information(self, '提示', '对方请求悔棋, 您是否同意?', QMessageBox.Yes | QMessageBox.No)
            if res == QMessageBox.Yes:
                pre_round = self.history_record.pop(-1)
                self.chessboard[pre_round[0]][pre_round[1]].close()
                self.chessboard[pre_round[0]][pre_round[1]] = None
                self.chessman_sign.hide()
                self.nextRound()
                data = {'type': 'reply', 'detail': 'regret', 'data': True}
                self.tcp_socket.sendall(packSocketData(data))
            else:
                data = {'type': 'reply', 'detail': 'regret', 'data': False}
                self.tcp_socket.sendall(packSocketData(data))
        elif data['type'] == 'reply' and data['detail'] == 'startgame':
            if data['data']:
                self.is_gaming = True
                self.setWindowTitle('五子棋-微信公众号: Charles的皮卡丘 ——> %s走棋' % self.whoseround2nickname_dict.get(self.whoseround))
                for i, j in product(range(19), range(19)):
                    if self.chessboard[i][j]:
                        self.chessboard[i][j].close()
                        self.chessboard[i][j] = None
                self.history_record.clear()
                self.winner = None
                if self.winner_info_label:
                    self.winner_info_label.close()
                self.winner_info_label = None
                self.chessman_sign.hide()
                QMessageBox.information(self, '提示', '对方同意开始游戏请求, 您为%s, 执白者先行.' % {'white': '白子', 'black': '黑子'}.get(self.player_color))
            else:
                QMessageBox.information(self, '提示', '对方拒绝了您开始游戏的请求.')
        elif data['type'] == 'reply' and data['detail'] == 'regret':
            if data['data']:
                pre_round = self.history_record.pop(-1)
                self.chessboard[pre_round[0]][pre_round[1]].close()
                self.chessboard[pre_round[0]][pre_round[1]] = None
                self.nextRound()
                QMessageBox.information(self, '提示', '对方同意了您的悔棋请求.')
            else:
                QMessageBox.information(self, '提示', '对方拒绝了您的悔棋请求.')
        elif data['type'] == 'nickname':
            self.opponent_nickname = data['data']
    '''随机生成双方颜色-白子先走'''
    def randomAssignColor(self):
        self.player_color = random.choice(['white', 'black'])
        self.opponent_player_color = 'white' if self.player_color == 'black' else 'black'
        self.whoseround = 'white'
        self.whoseround2nickname_dict = {self.player_color: self.nickname, self.opponent_player_color: self.opponent_nickname}
    '''改变落子方'''
    def nextRound(self):
        self.whoseround = self.player_color if self.whoseround == self.opponent_player_color else self.opponent_player_color
        self.setWindowTitle('五子棋-微信公众号: Charles的皮卡丘 ——> %s走棋' % self.whoseround2nickname_dict.get(self.whoseround))
    '''开始监听客户端的连接'''
    def startListen(self):
        while True:
            try:
                self.setWindowTitle('五子棋-微信公众号: Charles的皮卡丘 ——> 服务器端启动成功, 等待客户端连接中')
                self.tcp_socket, self.client_ipport = self.tcp_server.accept()
                self.setWindowTitle('五子棋-微信公众号: Charles的皮卡丘 ——> 客户端已连接, 点击开始按钮进行游戏')
                data = {'type': 'nickname', 'data': self.nickname}
                self.tcp_socket.sendall(packSocketData(data))
                self.receiveClientData()
            except:
                break
    '''接收客户端数据'''
    def receiveClientData(self):
        while True:
            data = receiveAndReadSocketData(self.tcp_socket)
            self.receive_signal.emit(data)
    '''关闭窗口事件'''
    def closeEvent(self, event):
        if self.tcp_socket:
            self.tcp_socket.sendall(packSocketData({'type': 'action', 'detail': 'exit'}))
            self.tcp_socket.shutdown(socket.SHUT_RDWR)
            self.tcp_socket.close()
        self.tcp_server.close()
        return super().closeEvent(event)