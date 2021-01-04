'''
Function:
    打砖块小游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import cfg
from modules import breakoutClone


'''主函数'''
def main():
    game = breakoutClone(cfg)
    game.run()


'''run'''
if __name__ == '__main__':
    main()