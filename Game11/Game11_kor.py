'''
Function:
	테트리스
Author:
	Charles
닉네임:
	Charles의 피카츄
'''
import sys
import random
from utils import *
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QHBoxLayout, QLabel
	

	

'''
Function:
	러시아 쿼드러플 게임류 정의
'''
class TetrisGame(QMainWindow):
	def __init__(self):
		super().__init__()
		# 일시정지 여부ing
		self.is_paused = False
		# 시작 여부ing
		self.is_started = False
		self.initUI()
	'''인터페이스 초기화'''
	def initUI(self):
		# 블록크기
		self.grid_size = 22
		# 게임 프레임률
		self.fps = 200
		self.timer = QBasicTimer()
		# 초점
		self.setFocusPolicy(Qt.StrongFocus)
		# 수평배치
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
		self.setWindowTitle('Tetris-공공번호:Charles의 피카츄')
		self.show()
		self.setFixedSize(self.external_board.width() + self.side_panel.width(),
							 self.side_panel.height() + self.status_bar.height())
	'''게임 인터페이스가 화면 가운데로 이동'''
	def center(self):
		screen = QDesktopWidget().screenGeometry()
		size = self.geometry()
		self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)
	'''인터페이스 업데이트'''
	def updateWindow(self):
		self.external_board.updateData()
		self.side_panel.updateData()
		self.update()
	'''시작'''
	def start(self):
		if self.is_started:
			return
		self.is_started = True
		self.inner_board.createNewTetris()
		self.timer.start(self.fps, self)
	'''일시 중지/일시 중지 안함'''
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
	'''타이머 사건'''
	def timerEvent(self, event):
		if event.timerId() == self.timer.timerId():
			removed_lines = self.inner_board.moveDown()
			self.external_board.score += removed_lines
			self.updateWindow()
		else:
			super(TetrisGame, self).timerEvent(event)
	'''버튼 사건'''
	def keyPressEvent(self, event):
		if not self.is_started or self.inner_board.current_tetris == tetrisShape().shape_empty:
			super(TetrisGame, self).keyPressEvent(event)
			return
		key = event.key()
		# P키 타임아웃
		if key == Qt.Key_P:
			self.pause()
			return
		if self.is_paused:
			return
		# 왼쪽으로
		elif key == Qt.Key_Left:
			self.inner_board.moveLeft()
		# 오른쪽으로
		elif key == Qt.Key_Right:
			self.inner_board.moveRight()
		# 회전
		elif key == Qt.Key_Up:
			self.inner_board.rotateAnticlockwise()
		# 빠른 추락
		elif key == Qt.Key_Space:
			self.external_board.score += self.inner_board.dropDown()
		else:
			super(TetrisGame, self).keyPressEvent(event)
		self.updateWindow()
	

	

if __name__ == '__main__':
	app = QApplication([])
	tetris = TetrisGame()
	sys.exit(app.exec_())

