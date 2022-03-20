'''
Function:
    一些工具函数
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import json
from itertools import product


'''check dir'''
def checkDir(dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
        return False
    return True


'''检查是否有人胜利'''
def checkWin(chessboard):
    # 是否是平局
    is_full = True
    for i, j in product(range(19), range(19)):
        if chessboard[i][j] is None:
            is_full = False
    if is_full:
        return 'draw'
    # 是否有人赢了
    for i, j in product(range(19), range(19)):
        # --和右边4个子连成5个
        if i < 15:
            chessmans = [chessboard[i][j], chessboard[i+1][j], chessboard[i+2][j], chessboard[i+3][j], chessboard[i+4][j]]
            if None not in chessmans:
                colors = [c.color for c in chessmans]
                if len(list(set(colors))) == 1:
                    return colors[0]
        # --和下边4个子连成5个
        if j < 15:
            chessmans = [chessboard[i][j], chessboard[i][j+1], chessboard[i][j+2], chessboard[i][j+3], chessboard[i][j+4]]
            if None not in chessmans:
                colors = [c.color for c in chessmans]
                if len(list(set(colors))) == 1:
                    return colors[0]
        # --和右下角4个子连成5个
        if i < 15 and j < 15:
            chessmans = [chessboard[i][j], chessboard[i+1][j+1], chessboard[i+2][j+2], chessboard[i+3][j+3], chessboard[i+4][j+4]]
            if None not in chessmans:
                colors = [c.color for c in chessmans]
                if len(list(set(colors))) == 1:
                    return colors[0]
        # --和左下角4个子连成5个
        if i > 3 and j < 15:
            chessmans = [chessboard[i][j], chessboard[i-1][j+1], chessboard[i-2][j+2], chessboard[i-3][j+3], chessboard[i-4][j+4]]
            if None not in chessmans:
                colors = [c.color for c in chessmans]
                if len(list(set(colors))) == 1:
                    return colors[0]
    return None


'''将像素坐标转为棋盘坐标'''
def Pixel2Chesspos(point):
    x, y = point.x(), point.y()
    x = round((x - 50.) / 30.)
    y = round((y - 50.) / 30.)
    return (x, y)


'''棋盘坐标转像素坐标'''
def Chesspos2Pixel(position):
    x = position[0] * 30 + 50
    y = position[1] * 30 + 50
    return (x, y)


'''接收并读取网络数据'''
def receiveAndReadSocketData(socket):
    data = ''
    while True:
        data_part = socket.recv(1024).decode()
        if 'END' in data_part:
            data += data_part[:data_part.index('END')]
            break
        data += data_part
    return json.loads(data, encoding='utf-8')


'''包装待发送数据'''
def packSocketData(data):
    return (json.dumps(data)+' END').encode()