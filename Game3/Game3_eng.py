# coding: utf-8
# 作者: Charles
# 公众号: Charles的皮卡丘
# 拼图小游戏
import os
import sys
import random
import pygame
from pygame.locals import *


# 定义常量
Window_Width = 500
Window_Height = 500
Background_Color = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
BLACK = (0, 0, 0)
FPS = 40
Num_Random = 100


# 退出
def Stop():
	pygame.quit()
	sys.exit()


# 判断游戏是否结束
def isOver(board, blankCell, size):
	try:
		Num_Cell = size * size
	except:
		Num_Cell = size[0] * size[1]
	for i in range(Num_Cell-1):
		if board[i] != i:
			return False
	return True


# 将空白Cell左边的Cell右移到空白Cell位置
def moveR(board, blankCell, columns):
	if blankCell % columns == 0:
		return blankCell
	board[blankCell-1], board[blankCell] = board[blankCell], board[blankCell-1]
	return blankCell-1


# 将空白Cell右边的Cell左移到空白Cell位置
def moveL(board, blankCell, columns):
	if (blankCell+1) % columns == 0:
		return blankCell
	board[blankCell+1], board[blankCell] = board[blankCell], board[blankCell+1]
	return blankCell+1


# 将空白Cell上边的Cell下移到空白Cell位置
def MoveD(board, blankCell, columns):
	if blankCell < columns:
		return blankCell
	board[blankCell-columns], board[blankCell] = board[blankCell], board[blankCell-columns]
	return blankCell-columns


# 将空白Cell下边的Cell上移到空白Cell位置
def MoveU(board, blankCell, row, columns):
	if blankCell >= (row-1) * columns:
		return blankCell
	board[blankCell+columns], board[blankCell] = board[blankCell], board[blankCell+columns]
	return blankCell+columns


# 获得打乱的拼图
def CreateBoard(row, columns, Num_Cell):
	board = []
	for i in range(Num_Cell):
		board.append(i)
	# 去掉右下角那块
	blankCell = Num_Cell - 1
	board[blankCell] = -1
	for i in range(Num_Random):
		# 0: left
		# 1: right
		# 2: up
		# 3: down
		direction = random.randint(0, 3)
		if direction == 0:
			blankCell = moveL(board, blankCell, columns)
		elif direction == 1:
			blankCell = moveR(board, blankCell, columns)
		elif direction == 2:
			blankCell = MoveU(board, blankCell, row, columns)
		elif direction == 3:
			blankCell = MoveD(board, blankCell, columns)
	return board, blankCell


# 随机选取一张图片
def GetImagePath(filepath):
	imgs = os.listdir(filepath)
	if len(imgs) == 0:
		print('[Error]: No pictures in filepath...')
	return os.path.join(filepath, random.choice(imgs))


# 显示游戏结束界面
def Show_End_Interface(Demo, width, height):
	Demo.fill(Background_Color)
	font = pygame.font.Font('./font/simkai.ttf', width//8)
	title = font.render('Finished!', True, (233, 150, 122))
	rect = title.get_rect()
	rect.midtop = (width/2, height/2.5)
	Demo.blit(title, rect)
	pygame.display.update()
	pygame.time.wait(500)
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				Stop()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					Stop()


# 显示游戏开始界面
def Show_Start_Interface(Demo, width, height):
	Demo.fill(Background_Color)
	tfont = pygame.font.Font('./font/simkai.ttf', width//4)
	cfont = pygame.font.Font('./font/simkai.ttf', width//20)
	title = tfont.render('拼图游戏', True, Red)
	content1 = cfont.render('按H或M或L键开始游戏', True, Blue)
	content2 = cfont.render('H为5*5模式，M为4*4模式，L为3*3模式', True, Blue)
	trect = title.get_rect()
	trect.midtop = (width/2, height/10)
	crect1 = content1.get_rect()
	crect1.midtop = (width/2, height/2.2)
	crect2 = content2.get_rect()
	crect2.midtop = (width/2, height/1.8)
	Demo.blit(title, trect)
	Demo.blit(content1, crect1)
	Demo.blit(content2, crect2)
	pygame.display.update()
	while True:
		size = None
		for event in pygame.event.get():
			if event.type == QUIT:
				Stop()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					Stop()
				if event.key == ord('l'):
					size = 3
				elif event.key == ord('m'):
					size = 4
				elif event.key == ord('h'):
					size = 5
		if size:
			break
	return size


# 主函数
def main(filepath):
	# 初始化
	pygame.init()
	mainClock = pygame.time.Clock()
	# 加载图片
	gameImg = pygame.image.load(GetImagePath(filepath))
	ImgRect = gameImg.get_rect()
	# 设置窗口
	Demo = pygame.display.set_mode((ImgRect.width, ImgRect.height))
	pygame.display.set_caption('拼图游戏')
	# 开始界面
	size = Show_Start_Interface(Demo, ImgRect.width, ImgRect.height)
	if isinstance(size, int):
		row, columns = size, size
		Num_Cell = size * size
	elif len(size) == 2:
		row, columns = size[0], size[1]
		Num_Cell = size[0] * size[1]
	else:
		print('[Error]: Parameter Size error...')
		Stop()
	# 计算Cell大小
	cellWidth = ImgRect.width // columns
	cellHeight = ImgRect.height // row
	# 游戏是否结束
	over = False
	# 避免初始化为原图
	while True:
		gameBoard, blankCell = CreateBoard(row, columns, Num_Cell)
		if not isOver(gameBoard, blankCell, size):
			break
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				Stop()
			if over:
				Show_End_Interface(Demo, ImgRect.width, ImgRect.height)
			# 键盘操作
			if event.type == KEYDOWN:
				if event.key == K_LEFT or event.key == ord('a'):
					blankCell = moveL(gameBoard, blankCell, columns)
				elif event.key == K_RIGHT or event.key == ord('d'):
					blankCell = moveR(gameBoard, blankCell, columns)
				elif event.key == K_UP or event.key == ord('w'):
					blankCell = MoveU(gameBoard, blankCell, row, columns)
				elif event.key == K_DOWN or event.key == ord('s'):
					blankCell = MoveD(gameBoard, blankCell, columns)
			# 鼠标操作
			if event.type == MOUSEBUTTONDOWN and event.button == 1:
				x, y = pygame.mouse.get_pos()
				x_pos = x // cellWidth
				y_pos = y // cellHeight
				idx = x_pos + y_pos * columns
				if idx==blankCell-1 or idx==blankCell+1 or idx==blankCell+columns or idx==blankCell-columns:
					gameBoard[blankCell], gameBoard[idx] = gameBoard[idx], gameBoard[blankCell]
					blankCell = idx
		if isOver(gameBoard, blankCell, size):
			gameBoard[blankCell] = Num_Cell-1
			over = True
		Demo.fill(Background_Color)
		for i in range(Num_Cell):
			if gameBoard[i] == -1:
				continue
			x_pos = i // columns
			y_pos = i % columns
			rect = pygame.Rect(y_pos*cellWidth, x_pos*cellHeight, cellWidth, cellHeight)
			ImgArea = pygame.Rect((gameBoard[i]%columns)*cellWidth, (gameBoard[i]//columns)*cellHeight, cellWidth, cellHeight)
			Demo.blit(gameImg, rect, ImgArea)
		for i in range(columns+1):
			pygame.draw.line(Demo, BLACK, (i*cellWidth, 0), (i*cellWidth, ImgRect.height))
		for i in range(row+1):
			pygame.draw.line(Demo, BLACK, (0, i*cellHeight), (ImgRect.width, i*cellHeight))
		pygame.display.update()
		mainClock.tick(FPS)


if __name__ == '__main__':
	filepath = './pictures'
	main(filepath)