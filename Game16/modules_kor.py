'''
Function:
	24점 게임
Author:
	Charles
WeChat 공개번호:
	Charles의 피카츄
'''
import copy
import random
import pygame


'''
Function:
	카드 클래스
Initial Args:
	--x: 왼쪽 상단
	--y: 오른쪽 하단
	--width: 와이드
	--height: 높이
	--text: 텍스트
	--font: [글꼴 경로, 글꼴 크기]
	--font_colors(list): 글꼴 색
	--bg_colors(list): 배경 색상
'''
class Card(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height, text, font, font_colors, bg_colors, attribute, **kwargs):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect(x, y, width, height)
		self.text = text
		self.attribute = attribute
		self.font_info = font
		self.font = pygame.font.Font(font[0], font[1])
		self.font_colors = font_colors
		self.is_selected = False
		self.select_order = None
		self.bg_colors = bg_colors
	'''화면에 그리기'''
	def draw(self, screen, mouse_pos):
		pygame.draw.rect(screen, self.bg_colors[1], self.rect, 0)
		if self.rect.collidepoint(mouse_pos):
			pygame.draw.rect(screen, self.bg_colors[0], self.rect, 0)
		font_color = self.font_colors[self.is_selected]
		text_render = self.font.render(self.text, True, font_color)
		font_size = self.font.size(self.text)
		screen.blit(text_render, (self.rect.x+(self.rect.width-font_size[0])/2,
								  self.rect.y+(self.rect.height-font_size[1])/2))


'''버튼 클래스'''
class Button(Card):
	def __init__(self, x, y, width, height, text, font, font_colors, bg_colors, attribute, **kwargs):
		Card.__init__(self, x, y, width, height, text, font, font_colors, bg_colors, attribute)
	'''버튼 기능에 따라 응답작업 수행'''
	def do(self, game24_gen, func, sprites_group, objs):
		if self.attribute == 'NEXT':
			for obj in objs:
				obj.font = pygame.font.Font(obj.font_info[0], obj.font_info[1])
				obj.text = obj.attribute
			self.font = pygame.font.Font(self.font_info[0], self.font_info[1])
			self.text = self.attribute
			game24_gen.generate()
			sprites_group = func(game24_gen.numbers_now)
		elif self.attribute == 'RESET':
			for obj in objs:
				obj.font = pygame.font.Font(obj.font_info[0], obj.font_info[1])
				obj.text = obj.attribute
			game24_gen.numbers_now = game24_gen.numbers_ori
			game24_gen.answers_idx = 0
			sprites_group = func(game24_gen.numbers_now)
		elif self.attribute == 'ANSWERS':
			self.font = pygame.font.Font(self.font_info[0], 20)
			self.text = '[%d/%d]: ' % (game24_gen.answers_idx+1, len(game24_gen.answers)) + game24_gen.answers[game24_gen.answers_idx]
			game24_gen.answers_idx = (game24_gen.answers_idx+1) % len(game24_gen.answers)
		else:
			raise ValueError('Button.attribute unsupport <%s>, expect <%s>, <%s> or <%s>...' % (self.attribute, 'NEXT', 'RESET', 'ANSWERS'))
		return sprites_group


'''24점 게임 생성기'''
class game24Generator():
	def __init__(self):
		self.info = 'game24Generator'
	'''생성기'''
	def generate(self):
		self.__reset()
		while True:
			self.numbers_ori = [random.randint(1, 10) for i in range(4)]
			self.numbers_now = copy.deepcopy(self.numbers_ori)
			self.answers = self.__verify()
			if self.answers:
				break
	'''하나의 숫자만 남았을 때 24인지 확인'''
	def check(self):
		if len(self.numbers_now) == 1 and float(self.numbers_now[0]) == self.target:
			return True
		return False
	'''재설정'''
	def __reset(self):
		self.answers = []
		self.numbers_ori = []
		self.numbers_now = []
		self.target = 24.
		self.answers_idx = 0
	'''생성된 번호에 답이 있는지 확인'''
	def __verify(self):
		answers = []
		for item in self.__iter(self.numbers_ori, len(self.numbers_ori)):
			item_dict = []
			list(map(lambda i: item_dict.append({str(i): i}), item))
			solution1 = self.__func(self.__func(self.__func(item_dict[0], item_dict[1]), item_dict[2]), item_dict[3])
			solution2 = self.__func(self.__func(item_dict[0], item_dict[1]), self.__func(item_dict[2], item_dict[3]))
			solution = dict()
			solution.update(solution1)
			solution.update(solution2)
			for key, value in solution.items():
				if float(value) == self.target:
					answers.append(key)
		# 반복되는 숫자가있을 때 표현식을 반복하지 마십시오 (T_T 너무 느려서 최적화 할 수 없습니다)
		answers = list(set(answers))
		return answers
	'''재귀열거'''
	def __iter(self, items, n):
		for idx, item in enumerate(items):
			if n == 1:
				yield [item]
			else:
				for each in self.__iter(items[:idx]+items[idx+1:], n-1):
					yield [item] + each
	'''계산기능'''
	def __func(self, a, b):
		res = dict()
		for key1, value1 in a.items():
			for key2, value2 in b.items():
				res.update({'('+key1+'+'+key2+')': value1+value2})
				res.update({'('+key1+'-'+key2+')': value1-value2})
				res.update({'('+key2+'-'+key1+')': value2-value1})
				res.update({'('+key1+'×'+key2+')': value1*value2})
				value2 > 0 and res.update({'('+key1+'÷'+key2+')': value1/value2})
				value1 > 0 and res.update({'('+key2+'÷'+key1+')': value2/value1})
		return res'''
Function:
	24점 게임
Author:
	Charles
WeChat 공개번호:
	Charles의 피카츄
'''
import copy
import random
import pygame


'''
Function:
	카드 클래스
Initial Args:
	--x: 왼쪽 상단
	--y: 오른쪽 하단
	--width: 와이드
	--height: 높이
	--text: 텍스트
	--font: [글꼴 경로, 글꼴 크기]
	--font_colors(list): 글꼴 색
	--bg_colors(list): 배경 색상
'''
class Card(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height, text, font, font_colors, bg_colors, attribute, **kwargs):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect(x, y, width, height)
		self.text = text
		self.attribute = attribute
		self.font_info = font
		self.font = pygame.font.Font(font[0], font[1])
		self.font_colors = font_colors
		self.is_selected = False
		self.select_order = None
		self.bg_colors = bg_colors
	'''화면에 그리기'''
	def draw(self, screen, mouse_pos):
		pygame.draw.rect(screen, self.bg_colors[1], self.rect, 0)
		if self.rect.collidepoint(mouse_pos):
			pygame.draw.rect(screen, self.bg_colors[0], self.rect, 0)
		font_color = self.font_colors[self.is_selected]
		text_render = self.font.render(self.text, True, font_color)
		font_size = self.font.size(self.text)
		screen.blit(text_render, (self.rect.x+(self.rect.width-font_size[0])/2,
								  self.rect.y+(self.rect.height-font_size[1])/2))


'''버튼 클래스'''
class Button(Card):
	def __init__(self, x, y, width, height, text, font, font_colors, bg_colors, attribute, **kwargs):
		Card.__init__(self, x, y, width, height, text, font, font_colors, bg_colors, attribute)
	'''버튼 기능에 따라 응답작업 수행'''
	def do(self, game24_gen, func, sprites_group, objs):
		if self.attribute == 'NEXT':
			for obj in objs:
				obj.font = pygame.font.Font(obj.font_info[0], obj.font_info[1])
				obj.text = obj.attribute
			self.font = pygame.font.Font(self.font_info[0], self.font_info[1])
			self.text = self.attribute
			game24_gen.generate()
			sprites_group = func(game24_gen.numbers_now)
		elif self.attribute == 'RESET':
			for obj in objs:
				obj.font = pygame.font.Font(obj.font_info[0], obj.font_info[1])
				obj.text = obj.attribute
			game24_gen.numbers_now = game24_gen.numbers_ori
			game24_gen.answers_idx = 0
			sprites_group = func(game24_gen.numbers_now)
		elif self.attribute == 'ANSWERS':
			self.font = pygame.font.Font(self.font_info[0], 20)
			self.text = '[%d/%d]: ' % (game24_gen.answers_idx+1, len(game24_gen.answers)) + game24_gen.answers[game24_gen.answers_idx]
			game24_gen.answers_idx = (game24_gen.answers_idx+1) % len(game24_gen.answers)
		else:
			raise ValueError('Button.attribute unsupport <%s>, expect <%s>, <%s> or <%s>...' % (self.attribute, 'NEXT', 'RESET', 'ANSWERS'))
		return sprites_group


'''24점 게임 생성기'''
class game24Generator():
	def __init__(self):
		self.info = 'game24Generator'
	'''생성기'''
	def generate(self):
		self.__reset()
		while True:
			self.numbers_ori = [random.randint(1, 10) for i in range(4)]
			self.numbers_now = copy.deepcopy(self.numbers_ori)
			self.answers = self.__verify()
			if self.answers:
				break
	'''하나의 숫자만 남았을 때 24인지 확인'''
	def check(self):
		if len(self.numbers_now) == 1 and float(self.numbers_now[0]) == self.target:
			return True
		return False
	'''재설정'''
	def __reset(self):
		self.answers = []
		self.numbers_ori = []
		self.numbers_now = []
		self.target = 24.
		self.answers_idx = 0
	'''생성된 번호에 답이 있는지 확인'''
	def __verify(self):
		answers = []
		for item in self.__iter(self.numbers_ori, len(self.numbers_ori)):
			item_dict = []
			list(map(lambda i: item_dict.append({str(i): i}), item))
			solution1 = self.__func(self.__func(self.__func(item_dict[0], item_dict[1]), item_dict[2]), item_dict[3])
			solution2 = self.__func(self.__func(item_dict[0], item_dict[1]), self.__func(item_dict[2], item_dict[3]))
			solution = dict()
			solution.update(solution1)
			solution.update(solution2)
			for key, value in solution.items():
				if float(value) == self.target:
					answers.append(key)
		# 반복되는 숫자가있을 때 표현식을 반복하지 마십시오 (T_T 너무 느려서 최적화 할 수 없습니다)
		answers = list(set(answers))
		return answers
	'''재귀열거'''
	def __iter(self, items, n):
		for idx, item in enumerate(items):
			if n == 1:
				yield [item]
			else:
				for each in self.__iter(items[:idx]+items[idx+1:], n-1):
					yield [item] + each
	'''계산기능'''
	def __func(self, a, b):
		res = dict()
		for key1, value1 in a.items():
			for key2, value2 in b.items():
				res.update({'('+key1+'+'+key2+')': value1+value2})
				res.update({'('+key1+'-'+key2+')': value1-value2})
				res.update({'('+key2+'-'+key1+')': value2-value1})
				res.update({'('+key1+'×'+key2+')': value1*value2})
				value2 > 0 and res.update({'('+key1+'÷'+key2+')': value1/value2})
				value1 > 0 and res.update({'('+key2+'÷'+key1+')': value2/value1})
		return res