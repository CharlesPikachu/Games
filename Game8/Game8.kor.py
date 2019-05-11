# 타워 방어 게임

# 저자: Charles

# 공개 번호 : Charles 's Pikachu

import pygame

from interface import END

from interface import START

from interface import GAMING

from interface import CHOICE

WIDTH = 800

HEIGHT = 600





# 메임 함수

def main():

	pygame.init()

	pygame.mixer.init()

	pygame.mixer.music.load('resource/audios/1.mp3')

	pygame.mixer.music.play(-1, 0.0)

	pygame.mixer.music.set_volume(0.25)

	screen = pygame.display.set_mode((WIDTH, HEIGHT))

	pygame.display.set_caption("塔防游戏-公众号: Charles的皮卡丘")

	clock = pygame.time.Clock()

	# 게임 시작 인터페이스 호출

	start_interface = START.START(WIDTH, HEIGHT)

	is_play = start_interface.update(screen)

	if not is_play:

		return

	# 게임 인터페이스 호출

	while True:

		choice_interface = CHOICE.CHOICE(WIDTH, HEIGHT)

		map_choice, difficulty_choice = choice_interface.update(screen)

		game_interface = GAMING.GAMING(WIDTH, HEIGHT)

		game_interface.start(screen, map_path='./maps/%s.map' % map_choice, difficulty_path='./difficulty/%s.json' % difficulty_choice)

		end_interface = END.END(WIDTH, HEIGHT)

		end_interface.update(screen)





if __name__ == '__main__':

	main()