'''
Function:
    定义联机对战
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import random
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from modules.online.server import *
from modules.online.client import *


'''联机对战'''
class playOnlineUI(QWidget):
    def __init__(self, cfg, home_ui, parent=None, **kwargs):
        super(playOnlineUI, self).__init__(parent)
        self.cfg = cfg
        self.home_ui = home_ui
        self.setWindowTitle('联机对战')
        self.setWindowIcon(QIcon(cfg.ICON_FILEPATH))
        self.setFixedSize(300, 200)
        # 昵称
        self.nickname = random.choice(['杰尼龟', '皮卡丘', '小火龙', '小锯鳄', '妙蛙种子', '菊草叶'])
        self.layout0 = QHBoxLayout()
        self.nickname_label = QLabel('游戏昵称:', self)
        self.nickname_edit = QLineEdit(self)
        self.nickname_edit.setText(self.nickname)
        self.layout0.addWidget(self.nickname_label, 1)
        self.layout0.addWidget(self.nickname_edit, 3)
        # IP
        self.target_ip = '127.0.0.1'
        self.layout1 = QHBoxLayout()
        self.ip_label = QLabel('对方IP:', self)
        self.ip_edit = QLineEdit(self)
        self.ip_edit.setText(self.target_ip)
        self.layout1.addWidget(self.ip_label, 1)
        self.layout1.addWidget(self.ip_edit, 3)
        # 按钮
        self.layout2 = QHBoxLayout()
        self.connect_button = QPushButton('作为客户端', self)
        self.connect_button.clicked.connect(self.becomeClient)
        self.ashost_button = QPushButton('作为服务器', self)
        self.ashost_button.clicked.connect(self.becomeHost)
        self.layout2.addWidget(self.connect_button)
        self.layout2.addWidget(self.ashost_button)
        # 布局
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.layout0)
        self.layout.addLayout(self.layout1)
        self.layout.addLayout(self.layout2)
        self.setLayout(self.layout)
    '''作为客户端'''
    def becomeClient(self):
        self.close()
        self.nickname = self.nickname_edit.text()
        self.target_ip = self.ip_edit.text()
        self.client_ui = gobangClient(cfg=self.cfg, nickname=self.nickname, server_ip=self.target_ip)
        self.client_ui.exit_signal.connect(lambda: sys.exit())
        self.client_ui.back_signal.connect(self.home_ui.show)
        self.client_ui.show()
    '''作为服务器'''
    def becomeHost(self):
        self.close()
        self.nickname = self.nickname_edit.text()
        self.server_ui = gobangSever(cfg=self.cfg, nickname=self.nickname)
        self.server_ui.exit_signal.connect(lambda: sys.exit())
        self.server_ui.back_signal.connect(self.home_ui.show)
        self.server_ui.show()