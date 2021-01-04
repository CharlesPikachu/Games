'''配置文件'''
import os


'''屏幕大小'''
SCREENSIZE = (800, 600)
'''图片路径'''
IMAGEPATHS = {
    'choice': {
        'load_game': os.path.join(os.getcwd(), 'resources/images/choice/load_game.png'),
        'map1': os.path.join(os.getcwd(), 'resources/images/choice/map1.png'),
        'map1_black': os.path.join(os.getcwd(), 'resources/images/choice/map1_black.png'),
        'map1_red': os.path.join(os.getcwd(), 'resources/images/choice/map1_red.png'),
        'map2': os.path.join(os.getcwd(), 'resources/images/choice/map2.png'),
        'map2_black': os.path.join(os.getcwd(), 'resources/images/choice/map2_black.png'),
        'map2_red': os.path.join(os.getcwd(), 'resources/images/choice/map2_red.png'),
        'map3': os.path.join(os.getcwd(), 'resources/images/choice/map3.png'),
        'map3_black': os.path.join(os.getcwd(), 'resources/images/choice/map3_black.png'),
        'map3_red': os.path.join(os.getcwd(), 'resources/images/choice/map3_red.png'),
    },
    'end': {
        'gameover': os.path.join(os.getcwd(), 'resources/images/end/gameover.png'),
        'continue_red': os.path.join(os.getcwd(), 'resources/images/end/continue_red.png'),
        'continue_black': os.path.join(os.getcwd(), 'resources/images/end/continue_black.png'),
    },
    'game': {
        'arrow1': os.path.join(os.getcwd(), 'resources/images/game/arrow1.png'), 
        'arrow2': os.path.join(os.getcwd(), 'resources/images/game/arrow2.png'), 
        'arrow3': os.path.join(os.getcwd(), 'resources/images/game/arrow3.png'), 
        'basic_tower': os.path.join(os.getcwd(), 'resources/images/game/basic_tower.png'), 
        'boulder': os.path.join(os.getcwd(), 'resources/images/game/boulder.png'), 
        'bush': os.path.join(os.getcwd(), 'resources/images/game/bush.png'), 
        'cave': os.path.join(os.getcwd(), 'resources/images/game/cave.png'), 
        'dirt': os.path.join(os.getcwd(), 'resources/images/game/dirt.png'), 
        'enemy_blue': os.path.join(os.getcwd(), 'resources/images/game/enemy_blue.png'), 
        'enemy_pink': os.path.join(os.getcwd(), 'resources/images/game/enemy_pink.png'), 
        'enemy_red': os.path.join(os.getcwd(), 'resources/images/game/enemy_red.png'), 
        'enemy_yellow': os.path.join(os.getcwd(), 'resources/images/game/enemy_yellow.png'), 
        'godark': os.path.join(os.getcwd(), 'resources/images/game/godark.png'), 
        'golight': os.path.join(os.getcwd(), 'resources/images/game/golight.png'), 
        'grass': os.path.join(os.getcwd(), 'resources/images/game/grass.png'), 
        'healthfont': os.path.join(os.getcwd(), 'resources/images/game/healthfont.png'), 
        'heavy_tower': os.path.join(os.getcwd(), 'resources/images/game/heavy_tower.png'), 
        'med_tower': os.path.join(os.getcwd(), 'resources/images/game/med_tower.png'), 
        'nexus': os.path.join(os.getcwd(), 'resources/images/game/nexus.png'), 
        'othergrass': os.path.join(os.getcwd(), 'resources/images/game/othergrass.png'), 
        'path': os.path.join(os.getcwd(), 'resources/images/game/path.png'), 
        'rock': os.path.join(os.getcwd(), 'resources/images/game/rock.png'), 
        'tiles': os.path.join(os.getcwd(), 'resources/images/game/tiles.png'), 
        'unitfont': os.path.join(os.getcwd(), 'resources/images/game/unitfont.png'), 
        'water': os.path.join(os.getcwd(), 'resources/images/game/water.png'), 
        'x': os.path.join(os.getcwd(), 'resources/images/game/x.png'), 
    },
    'pause': {
        'gamepaused': os.path.join(os.getcwd(), 'resources/images/pause/gamepaused.png'), 
        'resume_black': os.path.join(os.getcwd(), 'resources/images/pause/resume_black.png'), 
        'resume_red': os.path.join(os.getcwd(), 'resources/images/pause/resume_red.png'), 
    },
    'start': {
        'play_black': os.path.join(os.getcwd(), 'resources/images/start/play_black.png'), 
        'play_red': os.path.join(os.getcwd(), 'resources/images/start/play_red.png'), 
        'quit_black': os.path.join(os.getcwd(), 'resources/images/start/quit_black.png'), 
        'quit_red': os.path.join(os.getcwd(), 'resources/images/start/quit_red.png'), 
        'start_interface': os.path.join(os.getcwd(), 'resources/images/start/start_interface.png'), 
    },
}
'''地图路径'''
MAPPATHS = {
    '1': os.path.join(os.getcwd(), 'resources/maps/1.map'),
    '2': os.path.join(os.getcwd(), 'resources/maps/2.map'),
    '3': os.path.join(os.getcwd(), 'resources/maps/3.map'),
}
'''字体路径'''
FONTPATHS = {
    'Calibri': os.path.join(os.getcwd(), 'resources/fonts/Calibri.ttf'),
    'm04': os.path.join(os.getcwd(), 'resources/fonts/m04.ttf'),
    'Microsoft Sans Serif': os.path.join(os.getcwd(), 'resources/fonts/Microsoft Sans Serif.ttf'),
}
'''不同难度的settings'''
DIFFICULTYPATHS = {
    'easy': os.path.join(os.getcwd(), 'resources/difficulties/easy.json'),
    'hard': os.path.join(os.getcwd(), 'resources/difficulties/hard.json'),
    'medium': os.path.join(os.getcwd(), 'resources/difficulties/medium.json'),
}
'''音频路径'''
AUDIOPATHS = {
    'bgm': os.path.join(os.getcwd(), 'resources/audios/bgm.mp3'),
}