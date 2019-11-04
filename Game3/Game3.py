'''
Function:
	拼图小游戏
作者:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import os
import sys
import random
import pygame
from pygame.locals import *


'''定义一些常量'''
BACKGROUNDCOLOR = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
FPS = 40
NUMRANDOM = 100


'''退出'''
def Stop():
	pygame.quit()
	sys.exit()


'''判断游戏是否结束'''
def isOver(board, size):
	try:
		num_cells = size * size
	except:
		num_cells = size[0] * size[1]
	for i in range(num_cells-1):
		if board[i] != i:
			return False
	return True


'''将空白Cell左边的Cell右移到空白Cell位置'''
def moveR(board, blank_cell_idx, num_cols):
	if blank_cell_idx % num_cols == 0:
		return blank_cell_idx
	board[blank_cell_idx-1], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx-1]
	return blank_cell_idx-1


'''将空白Cell右边的Cell左移到空白Cell位置'''
def moveL(board, blank_cell_idx, num_cols):
	if (blank_cell_idx+1) % num_cols == 0:
		return blank_cell_idx
	board[blank_cell_idx+1], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx+1]
	return blank_cell_idx+1


'''将空白Cell上边的Cell下移到空白Cell位置'''
def moveD(board, blank_cell_idx, num_cols):
	if blank_cell_idx < num_cols:
		return blank_cell_idx
	board[blank_cell_idx-num_cols], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx-num_cols]
	return blank_cell_idx-num_cols


'''将空白Cell下边的Cell上移到空白Cell位置'''
def moveU(board, blank_cell_idx, num_rows, num_cols):
	if blank_cell_idx >= (num_rows-1) * num_cols:
		return blank_cell_idx
	board[blank_cell_idx+num_cols], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx+num_cols]
	return blank_cell_idx+num_cols


'''获得打乱的拼图'''
def CreateBoard(num_rows, num_cols, num_cells):
	board = []
	for i in range(num_cells):
		board.append(i)
	# 去掉右下角那块
	blank_cell_idx = num_cells - 1
	board[blank_cell_idx] = -1
	for i in range(NUMRANDOM):
		# 0: left, 1: right, 2: up, 3: down
		direction = random.randint(0, 3)
		if direction == 0:
			blank_cell_idx = moveL(board, blank_cell_idx, num_cols)
		elif direction == 1:
			blank_cell_idx = moveR(board, blank_cell_idx, num_cols)
		elif direction == 2:
			blank_cell_idx = moveU(board, blank_cell_idx, num_rows, num_cols)
		elif direction == 3:
			blank_cell_idx = moveD(board, blank_cell_idx, num_cols)
	return board, blank_cell_idx


'''随机选取一张图片'''
def GetImagePath(filepath):
	imgs = os.listdir(filepath)
	if len(imgs) == 0:
		raise ValueError('No pictures in <%s>...' % filepath)
	return os.path.join(filepath, random.choice(imgs))


'''显示游戏结束界面'''
def ShowEndInterface(screen, width, height):
	screen.fill(BACKGROUNDCOLOR)
	font = pygame.font.Font('./font/simkai.ttf', width//8)
	title = font.render('Finished!', True, (233, 150, 122))
	rect = title.get_rect()
	rect.midtop = (width/2, height/2.5)
	screen.blit(title, rect)
	pygame.display.update()
	pygame.time.wait(500)
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				Stop()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					Stop()


'''显示游戏开始界面'''
def ShowStartInterface(screen, width, height):
	screen.fill(BACKGROUNDCOLOR)
	tfont = pygame.font.Font('./font/simkai.ttf', width//4)
	cfont = pygame.font.Font('./font/simkai.ttf', width//20)
	title = tfont.render('拼图游戏', True, RED)
	content1 = cfont.render('按H或M或L键开始游戏', True, BLUE)
	content2 = cfont.render('H为5*5模式，M为4*4模式，L为3*3模式', True, BLUE)
	trect = title.get_rect()
	trect.midtop = (width/2, height/10)
	crect1 = content1.get_rect()
	crect1.midtop = (width/2, height/2.2)
	crect2 = content2.get_rect()
	crect2.midtop = (width/2, height/1.8)
	screen.blit(title, trect)
	screen.blit(content1, crect1)
	screen.blit(content2, crect2)
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


'''主函数'''
def main():
	# 初始化
	pygame.init()
	clock = pygame.time.Clock()
	# 加载图片
	game_img_used = pygame.image.load(GetImagePath('./pictures'))
	game_img_used_rect = game_img_used.get_rect()
	# 设置窗口
	screen = pygame.display.set_mode((game_img_used_rect.width, game_img_used_rect.height))
	pygame.display.set_caption('拼图游戏')
	# 开始界面
	size = ShowStartInterface(screen, game_img_used_rect.width, game_img_used_rect.height)
	if isinstance(size, int):
		num_rows, num_cols = size, size
		num_cells = size * size
	elif len(size) == 2:
		num_rows, num_cols = size[0], size[1]
		num_cells = size[0] * size[1]
	else:
		raise ValueError('cell size error')
	# 计算Cell大小
	cell_width = game_img_used_rect.width // num_cols
	cell_height = game_img_used_rect.height // num_rows
	# 游戏是否结束
	over = False
	# 避免初始化为原图
	while True:
		game_board, blank_cell_idx = CreateBoard(num_rows, num_cols, num_cells)
		if not isOver(game_board, size):
			break
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				Stop()
			if over:
				ShowEndInterface(screen, game_img_used_rect.width, game_img_used_rect.height)
			# 键盘操作
			if event.type == KEYDOWN:
				if event.key == K_LEFT or event.key == ord('a'):
					blank_cell_idx = moveL(game_board, blank_cell_idx, num_cols)
				elif event.key == K_RIGHT or event.key == ord('d'):
					blank_cell_idx = moveR(game_board, blank_cell_idx, num_cols)
				elif event.key == K_UP or event.key == ord('w'):
					blank_cell_idx = moveU(game_board, blank_cell_idx, num_rows, num_cols)
				elif event.key == K_DOWN or event.key == ord('s'):
					blank_cell_idx = moveD(game_board, blank_cell_idx, num_cols)
			# 鼠标操作
			if event.type == MOUSEBUTTONDOWN and event.button == 1:
				x, y = pygame.mouse.get_pos()
				x_pos = x // cell_width
				y_pos = y // cell_height
				idx = x_pos + y_pos * num_cols
				if idx == blank_cell_idx-1:
					blank_cell_idx = moveR(game_board, blank_cell_idx, num_cols)
				elif idx == blank_cell_idx+1:
					blank_cell_idx = moveL(game_board, blank_cell_idx, num_cols)
				elif idx == blank_cell_idx+num_cols:
					blank_cell_idx = moveU(game_board, blank_cell_idx, num_rows, num_cols)
				elif idx == blank_cell_idx-num_cols:
					blank_cell_idx = moveD(game_board, blank_cell_idx, num_cols)
		if isOver(game_board, size):
			game_board[blank_cell_idx] = num_cells - 1
			over = True
		screen.fill(BACKGROUNDCOLOR)
		for i in range(num_cells):
			if game_board[i] == -1:
				continue
			x_pos = i // num_cols
			y_pos = i % num_cols
			rect = pygame.Rect(y_pos*cell_width, x_pos*cell_height, cell_width, cell_height)
			img_area = pygame.Rect((game_board[i]%num_cols)*cell_width, (game_board[i]//num_cols)*cell_height, cell_width, cell_height)
			screen.blit(game_img_used, rect, img_area)
		for i in range(num_cols+1):
			pygame.draw.line(screen, BLACK, (i*cell_width, 0), (i*cell_width, game_img_used_rect.height))
		for i in range(num_rows+1):
			pygame.draw.line(screen, BLACK, (0, i*cell_height), (game_img_used_rect.width, i*cell_height))
		pygame.display.update()
		clock.tick(FPS)


'''run'''
if __name__ == '__main__':
	main()