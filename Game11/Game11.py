'''
Function:
	俄罗斯方块主程序
Author:
	Charles
公众号:
	Charles的皮卡丘
'''
import sys
import random
from utils import *
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QHBoxLayout, QLabel


'''
Function:
	定义俄罗斯方块游戏类
'''
class TetrisGame(QMainWindow):
	def __init__(self):
		super().__init__()
		# 是否暂停ing
		self.is_paused = False
		# 是否开始ing
		self.is_started = False
		self.initUI()
	'''界面初始化'''
	def initUI(self):
		# 块大小
		self.grid_size = 22
		# 游戏帧率
		self.fps = 200
		self.timer = QBasicTimer()
		# 焦点
		self.setFocusPolicy(Qt.StrongFocus)
		# 水平布局
		layout_horizontal = QHBoxLayout()
		self.inner_board = InnerBoard()
		self.external_board = ExternalBoard(self, self.grid_size, self.inner_board)
		layout_horizontal.addWidget(self.external_board)
		self.side_panel = SidePanel(self, self.grid_size, self.inner_board)
		layout_horizontal.addWidget(self.side_panel)
		self.status_bar = self.statusBar()
		self.external_board.score_signal[str].connect(self.status_bar.showMessage)
		self.start()
		self.center()
		self.setWindowTitle('Tetris-公众号:Charles的皮卡丘')
		self.show()
		self.setFixedSize(self.external_board.width() + self.side_panel.width(),
						  self.side_panel.height() + self.status_bar.height())
	'''游戏界面移动到屏幕中间'''
	def center(self):
		screen = QDesktopWidget().screenGeometry()
		size = self.geometry()
		self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)
	'''更新界面'''
	def updateWindow(self):
		self.external_board.updateData()
		self.side_panel.updateData()
		self.update()
	'''开始'''
	def start(self):
		if self.is_started:
			return
		self.is_started = True
		self.inner_board.createNewTetris()
		self.timer.start(self.fps, self)
	'''暂停/不暂停'''
	def pause(self):
		if not self.is_started:
			return
		self.is_paused = not self.is_paused
		if self.is_paused:
			self.timer.stop()
			self.external_board.score_signal.emit('Paused')
		else:
			self.timer.start(self.fps, self)
		self.updateWindow()
	'''计时器事件'''
	def timerEvent(self, event):
		if event.timerId() == self.timer.timerId():
			removed_lines = self.inner_board.moveDown()
			self.external_board.score += removed_lines
			self.updateWindow()
		else:
			super(TetrisGame, self).timerEvent(event)
	'''按键事件'''
	def keyPressEvent(self, event):
		if not self.is_started or self.inner_board.current_tetris == tetrisShape().shape_empty:
			super(TetrisGame, self).keyPressEvent(event)
			return
		key = event.key()
		# P键暂停
		if key == Qt.Key_P:
			self.pause()
			return
		if self.is_paused:
			return
		# 向左
		elif key == Qt.Key_Left:
			self.inner_board.moveLeft()
		# 向右
		elif key == Qt.Key_Right:
			self.inner_board.moveRight()
		# 旋转
		elif key == Qt.Key_Up:
			self.inner_board.rotateAnticlockwise()
		# 快速坠落
		elif key == Qt.Key_Space:
			self.external_board.score += self.inner_board.dropDown()
		else:
			super(TetrisGame, self).keyPressEvent(event)
		self.updateWindow()


'''run'''
if __name__ == '__main__':
	app = QApplication([])
	tetris = TetrisGame()
	sys.exit(app.exec_())