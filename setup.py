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
    'cpgames.core.games.base': ['resources/fonts/*', 'resources/audios/*'],
    'cpgames.core.games.aircraftwar': ['resources/audios/*', 'resources/images/*'],
    'cpgames.core.games.alieninvasion': ['resources/*'],
    'cpgames.core.games.angrybirds': ['resources/audios/*', 'resources/fonts/*', 'resources/images/*'],
    'cpgames.core.games.bomberman': ['resources/audios/*', 'resources/maps/*', 'resources/images/batman/*', 'resources/images/dk/*', 'resources/images/misc/*', 'resources/images/zelda/*'],
    'cpgames.core.games.breakoutclone': ['resources/audios/*', 'resources/levels/*'],
    'cpgames.core.games.bunnybadger': ['resources/audios/*', 'resources/images/*'],
    'cpgames.core.games.catchcoins': ['resources/audios/*', 'resources/images/*'],
    'cpgames.core.games.flappybird': ['resources/audios/*', 'resources/images/*'],
    'cpgames.core.games.flipcardbymemory': ['resources/audios/*', 'resources/images/series1/*', 'resources/images/series2/*', 'resources/images/series3/*'],
    'cpgames.core.games.gemgem': ['resources/audios/*', 'resources/images/*'],
    'cpgames.core.games.gobang': ['resources/audios/*', 'resources/images/bg/*', 'resources/images/buttons/*', 'resources/images/chessman/*', 'resources/images/icon/*', 'resources/images/win/*'],
    'cpgames.core.games.greedysnake': ['resources/audios/*'],
    'cpgames.core.games.maze': ['resources/audios/*', 'resources/images/*'],
    'cpgames.core.games.minesweeper': ['resources/audios/*', 'resources/fonts/*', 'resources/images/*'],
    'cpgames.core.games.pacman': ['resources/audios/*', 'resources/fonts/*', 'resources/images/*'],
    'cpgames.core.games.pingpong': ['resources/audios/*', 'resources/images/*'],
    'cpgames.core.games.puzzlepieces': ['resources/images/*'],
    'cpgames.core.games.ski': ['resources/audios/*', 'resources/images/*'],
    'cpgames.core.games.sokoban': ['resources/audios/*', 'resources/images/*', 'resources/levels/*'],
    'cpgames.core.games.tankwar': ['resources/audios/*', 'resources/images/bullet/*', 'resources/images/enemyTank/*', 'resources/images/food/*', 'resources/images/home/*', 'resources/images/others/*', 'resources/images/playerTank/*', 'resources/images/scene/*'],
    'cpgames.core.games.tankwar.modules': ['levels/*'],
    'cpgames.core.games.tetris': ['resources/*'],
    'cpgames.core.games.towerdefense': ['resources/audios/*', 'resources/fonts/*', 'resources/maps/*', 'resources/difficulties/*', 'resources/images/choice/*', 'resources/images/end/*', 'resources/images/game/*', 'resources/images/pause/*', 'resources/images/start/*'],
    'cpgames.core.games.trexrush': ['resources/audios/*', 'resources/images/*'],
    'cpgames.core.games.twentyfourpoint': ['resources/audios/*'],
    'cpgames.core.games.twozerofoureight': ['resources/audios/*'],
    'cpgames.core.games.voicecontrolpikachu': ['resources/images/*'],
    'cpgames.core.games.whacamole': ['resources/audios/*', 'resources/images/*'],
    'cpgames.core.games.magictower': ['resources/images/*', 'resources/levels/*', 'resources/fonts/*', 'resources/images/map0/*', 'resources/images/map1/*', 'resources/images/player/*'],
    'cpgames.core.games.bloodfootball': ['resources/images/*', 'resources/audios/*'],
}


'''setup'''
setup(
    name=cpgames.__title__,
    version=cpgames.__version__,
    description=cpgames.__description__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
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
    install_requires=[lab.strip('\n') for lab in list(open('requirements.txt', 'r').readlines())],
    zip_safe=True,
    packages=find_packages(),
)