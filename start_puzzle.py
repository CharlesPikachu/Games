
"""
启动拼图游戏的脚本
"""
import sys
import os

# 添加项目路径到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from cpgames.cpgames import CPGames

if __name__ == '__main__':
    print('正在启动拼图游戏...')
    print('游戏功能：')
    print('  - 按 U 键上传自定义图片')
    print('  - 按 H/M/L 键选择难度')
    print('  - 按 H 键显示提示')
    print('  - 按方向键或 WASD 移动拼图')
    print('  - 限时 5 分钟')
    print('')
    
    # 启动游戏
    game_client = CPGames()
    game_client.execute('puzzlepieces')