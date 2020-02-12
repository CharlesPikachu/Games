'''
Function:
	五子棋小游戏-支持人机和局域网对战
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import sys
import cfg
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from modules.misc.Buttons import *
from modules.ai.playWithAI import *
from modules.online.playOnline import *


'''游戏开始界面'''
class gameStartUI(QWidget):
	def __init__(self, parent=None, **kwargs):
		super(gameStartUI, self).__init__(parent)
		self.setFixedSize(760, 650)
		self.setWindowTitle('五子棋-微信公众号: Charles的皮卡丘')
		self.setWindowIcon(QIcon(cfg.ICON_FILEPATH))
		# 背景图片
		palette = QPalette()
		palette.setBrush(self.backgroundRole(), QBrush(QPixmap(cfg.BACKGROUND_IMAGEPATHS.get('bg_start'))))
		self.setPalette(palette)
		# 按钮
		# --人机对战
		self.ai_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('ai'), self)
		self.ai_button.move(250, 200)
		self.ai_button.show()
		self.ai_button.click_signal.connect(self.playWithAI)
		# --联机对战
		self.online_button = PushButton(cfg.BUTTON_IMAGEPATHS.get('online'), self)
		self.online_button.move(250, 350)
		self.online_button.show()
		self.online_button.click_signal.connect(self.playOnline)
	'''人机对战'''
	def playWithAI(self):
		self.close()
		self.gaming_ui = playWithAIUI(cfg)
		self.gaming_ui.exit_signal.connect(lambda: sys.exit())
		self.gaming_ui.back_signal.connect(self.show)
		self.gaming_ui.show()
	'''联机对战'''
	def playOnline(self):
		self.close()
		self.gaming_ui = playOnlineUI(cfg, self)
		self.gaming_ui.show()


'''run'''
if __name__ == '__main__':
	app = QApplication(sys.argv)
	handle = gameStartUI()
	font = QFont()
	font.setPointSize(12)
	handle.setFont(font)
	handle.show()
	sys.exit(app.exec_())