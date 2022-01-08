'''
Function:
    setup the cpgames
Author:
    Charles
微信公众号:
    Charles的皮卡丘
GitHub:
    https://github.com/CharlesPikachu
'''
import cpgames
from setuptools import setup, find_packages


'''readme'''
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()


'''package data'''
package_data = {
    'cpgames.modules.core.base': ['resources/fonts/*', 'resources/audios/*'],
    'cpgames.modules.core.aircraftwar': ['resources/audios/*', 'resources/images/*'],
    'cpgames.modules.core.alieninvasion': ['resources/*'],
    'cpgames.modules.core.angrybirds': ['resources/audios/*', 'resources/fonts/*', 'resources/images/*'],
    'cpgames.modules.core.bomberman': ['resources/audios/*', 'resources/maps/*', 'resources/images/batman/*', 'resources/images/dk/*', 'resources/images/misc/*', 'resources/images/zelda/*'],
    'cpgames.modules.core.breakoutclone': ['resources/audios/*', 'resources/levels/*'],
    'cpgames.modules.core.bunnybadger': ['resources/audios/*', 'resources/images/*'],
    'cpgames.modules.core.catchcoins': ['resources/audios/*', 'resources/images/*'],
    'cpgames.modules.core.flappybird': ['resources/audios/*', 'resources/images/*'],
    'cpgames.modules.core.flipcardbymemory': ['resources/audios/*', 'resources/images/series1/*', 'resources/images/series2/*', 'resources/images/series3/*'],
    'cpgames.modules.core.gemgem': ['resources/audios/*', 'resources/images/*'],
    'cpgames.modules.core.gobang': ['resources/audios/*', 'resources/images/bg/*', 'resources/images/buttons/*', 'resources/images/chessman/*', 'resources/images/icon/*', 'resources/images/win/*'],
    'cpgames.modules.core.greedysnake': ['resources/audios/*'],
    'cpgames.modules.core.maze': ['resources/audios/*', 'resources/images/*'],
    'cpgames.modules.core.minesweeper': ['resources/audios/*', 'resources/fonts/*', 'resources/images/*'],
    'cpgames.modules.core.pacman': ['resources/audios/*', 'resources/fonts/*', 'resources/images/*'],
    'cpgames.modules.core.pingpong': ['resources/audios/*', 'resources/images/*'],
    'cpgames.modules.core.puzzlepieces': ['resources/images/*'],
    'cpgames.modules.core.ski': ['resources/audios/*', 'resources/images/*'],
    'cpgames.modules.core.sokoban': ['resources/audios/*', 'resources/images/*', 'resources/levels/*'],
    'cpgames.modules.core.tankwar': ['resources/audios/*', 'resources/images/bullet/*', 'resources/images/enemyTank/*', 'resources/images/food/*', 'resources/images/home/*', 'resources/images/others/*', 'resources/images/playerTank/*', 'resources/images/scene/*'],
    'cpgames.modules.core.tankwar.modules': ['levels/*'],
    'cpgames.modules.core.tetris': ['resources/*'],
    'cpgames.modules.core.towerdefense': ['resources/audios/*', 'resources/fonts/*', 'resources/maps/*', 'resources/difficulties/*', 'resources/images/choice/*', 'resources/images/end/*', 'resources/images/game/*', 'resources/images/pause/*', 'resources/images/start/*'],
    'cpgames.modules.core.trexrush': ['resources/audios/*', 'resources/images/*'],
    'cpgames.modules.core.twentyfourpoint': ['resources/audios/*'],
    'cpgames.modules.core.twozerofoureight': ['resources/audios/*'],
    'cpgames.modules.core.voicecontrolpikachu': ['resources/images/*'],
    'cpgames.modules.core.whacamole': ['resources/audios/*', 'resources/images/*'],
}


'''setup'''
setup(
    name=cpgames.__title__,
    version=cpgames.__version__,
    description=cpgames.__description__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent'
    ],
    author=cpgames.__author__,
    url=cpgames.__url__,
    author_email=cpgames.__email__,
    license=cpgames.__license__,
    include_package_data=True,
    package_data=package_data,
    install_requires=list(open('requirements.txt', 'r').readlines()),
    zip_safe=True,
    packages=find_packages(),
)