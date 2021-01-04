'''配置文件'''
import os


# 一些常量
RED = (255, 0, 0)
BLACK = (0, 0, 0)
AZURE = (240, 255, 255)
WHITE = (255, 255, 255)
MISTYROSE = (255, 228, 225)
PALETURQUOISE = (175, 238, 238)
PAPAYAWHIP = (255, 239, 213)
CURRENTPATH = os.getcwd()
FONTPATH = os.path.join(CURRENTPATH, 'resources/fonts/font.TTF')
AUDIOWINPATH = os.path.join(CURRENTPATH, 'resources/audios/win.wav')
AUDIOLOSEPATH = os.path.join(CURRENTPATH, 'resources/audios/lose.wav')
AUDIOWARNPATH = os.path.join(CURRENTPATH, 'resources/audios/warn.wav')
BGMPATH = os.path.join(CURRENTPATH, 'resources/audios/bgm.mp3')
# 数字卡片
# --数字卡片字体颜色
NUMBERFONT_COLORS = [BLACK, RED]
# --数字卡片背景颜色
NUMBERCARD_COLORS = [MISTYROSE, PALETURQUOISE]
# --数字卡片字体路径与大小
NUMBERFONT = [FONTPATH, 50]
# --数字卡片位置
NUMBERCARD_POSITIONS = [(25, 50, 150, 200), (225, 50, 150, 200), (425, 50, 150, 200), (625, 50, 150, 200)]
# 运算符卡片
# --运算符种类
OPREATORS = ['+', '-', '×', '÷']
# --运算符卡片字体颜色
OPREATORFONT_COLORS = [BLACK, RED]
# --运算符卡片背景颜色
OPERATORCARD_COLORS = [MISTYROSE, PALETURQUOISE]
# --运算符卡片字体路径与大小
OPERATORFONT = [FONTPATH, 30]
# --运算符卡片位置
OPERATORCARD_POSITIONS = [(230, 300, 50, 50), (330, 300, 50, 50), (430, 300, 50, 50), (530, 300, 50, 50)]
# 按钮卡片
# --按钮类型
BUTTONS = ['RESET', 'ANSWERS', 'NEXT']
# --按钮卡片字体颜色
BUTTONFONT_COLORS = [BLACK, BLACK]
# --按钮卡片背景颜色
BUTTONCARD_COLORS = [MISTYROSE, PALETURQUOISE]
# --按钮卡片字体路径与大小
BUTTONFONT = [FONTPATH, 30]
# --按钮卡片位置
BUTTONCARD_POSITIONS = [(25, 400, 700/3, 150), (50+700/3, 400, 700/3, 150), (75+1400/3, 400, 700/3, 150)]
# 屏幕大小
SCREENSIZE = (800, 600)
# 卡片类型
GROUPTYPES = ['NUMBER', 'OPREATOR', 'BUTTON']