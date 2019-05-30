# coding: utf-8
# 作者: Charles
# 公众号: Charles的皮卡丘
# 仿八分音符的声控小游戏
import os
import cocos
import struct
from cocos.sprite import Sprite
from pyaudio import PyAudio, paInt16
from classes.pikachu import Pikachu
from classes.block import Block


# 定义声控游戏类
# Voice Control Class
class VCGame(cocos.layer.ColorLayer):
	is_event_handler = True
	def __init__(self):
		super(VCGame, self).__init__(255, 255, 255, 255, 800, 600)
		# 初始化参数
		# frames_per_buffer
		self.numSamples = 1000
		# 声控条
		self.vbar = Sprite('black.png')
		self.vbar.position = 20, 450
		self.vbar.scale_y = 0.1
		self.vbar.image_anchor = 0, 0
		self.add(self.vbar)
		# 皮卡丘类
		self.pikachu = Pikachu()
		self.add(self.pikachu)
		# cocosnode精灵类
		self.floor = cocos.cocosnode.CocosNode()
		self.add(self.floor)
		position = 0, 100
		for i in range(120):
			b = Block(position)
			self.floor.add(b)
			position = b.x + b.width, b.height
		# 声音输入
		audio = PyAudio()
		SampleRate = int(audio.get_device_info_by_index(0)['defaultSampleRate'])
		self.stream = audio.open(format=paInt16, 
								 channels=1, 
								 rate=SampleRate, 
								 input=True, 
								 frames_per_buffer=self.numSamples)
		self.schedule(self.update)
	# 碰撞检测
	def collide(self):
		diffx = self.pikachu.x - self.floor.x
		for b in self.floor.get_children():
			if b.x <= diffx + self.pikachu.width * 0.8 and diffx + self.pikachu.width * 0.2 <= b.x + b.width:
				if self.pikachu.y < b.height:
					self.pikachu.land(b.height)
					break
	# 定义游戏规则
	def update(self, dt):
		# 获取每帧的音量
		audio_data = self.stream.read(self.numSamples)
		k = max(struct.unpack('1000h', audio_data))
		self.vbar.scale_x = k / 10000.0
		if k > 3000:
			self.floor.x -= min((k / 20.0), 150) * dt
		if k > 8000:
			self.pikachu.jump((k - 8000) / 1000.0)
		self.collide()
	# 重置
	def reset(self):
		self.floor.x = 0


if __name__ == '__main__':
	cocos.director.director.init(caption="Pikachu~~~")
	cocos.director.director.run(cocos.scene.Scene(VCGame()))