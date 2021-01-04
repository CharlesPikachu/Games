'''
Function:
    仿八分音符的声控小游戏
作者:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import cfg
import cocos
import struct
from modules import *
from cocos.sprite import Sprite
from pyaudio import PyAudio, paInt16


'''定义声控游戏类'''
class VCGame(cocos.layer.ColorLayer):
    def __init__(self):
        super(VCGame, self).__init__(255, 255, 255, 255, 800, 600)
        # frames_per_buffer
        self.num_samples = 1000
        # 声控条
        self.vbar = Sprite(cfg.BLOCK_IMAGE_PATH)
        self.vbar.position = 20, 450
        self.vbar.scale_y = 0.1
        self.vbar.image_anchor = 0, 0
        self.add(self.vbar)
        # 皮卡丘
        self.pikachu = Pikachu(cfg.PIKACHU_IMAGE_PATH)
        self.add(self.pikachu)
        # 地面
        self.floor = cocos.cocosnode.CocosNode()
        self.add(self.floor)
        position = 0, 100
        for i in range(120):
            b = Block(cfg.BLOCK_IMAGE_PATH, position)
            self.floor.add(b)
            position = b.x + b.width, b.height
        # 声音输入
        audio = PyAudio()
        self.stream = audio.open(format=paInt16, channels=1, rate=int(audio.get_device_info_by_index(0)['defaultSampleRate']), input=True, frames_per_buffer=self.num_samples)
        # 屏幕更新
        self.schedule(self.update)
    '''碰撞检测'''
    def collide(self):
        diffx = self.pikachu.x - self.floor.x
        for b in self.floor.get_children():
            if (b.x <= diffx + self.pikachu.width * 0.8) and (diffx + self.pikachu.width * 0.2 <= b.x + b.width):
                if self.pikachu.y < b.height:
                    self.pikachu.land(b.height)
                    break
    '''定义游戏规则'''
    def update(self, dt):
        # 获取每帧的音量
        audio_data = self.stream.read(self.num_samples)
        k = max(struct.unpack('1000h', audio_data))
        self.vbar.scale_x = k / 10000.0
        if k > 3000:
            self.floor.x -= min((k / 20.0), 150) * dt
        # 皮卡丘跳跃
        if k > 8000:
            self.pikachu.jump((k - 8000) / 1000.0)
        # 碰撞检测
        self.collide()
    '''重置'''
    def reset(self):
        self.floor.x = 0


'''run'''
if __name__ == '__main__':
    cocos.director.director.init(caption="Pikachu Go Go Go —— Charles的皮卡丘")
    cocos.director.director.run(cocos.scene.Scene(VCGame()))