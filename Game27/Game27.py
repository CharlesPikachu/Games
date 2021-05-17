'''
Function:
    记忆翻牌小游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import cfg
import pygame
import random
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk


'''记忆翻牌小游戏'''
class FlipCardByMemory():
    def __init__(self):
        # 播放背景音乐
        self.playbgm()
        # 载入得分后响起的音乐
        self.score_sound = pygame.mixer.Sound(cfg.AUDIOPATHS['score'])
        self.score_sound.set_volume(1)
        # 卡片图片路径
        self.card_dir = random.choice(cfg.IMAGEPATHS['carddirs'])
        # 主界面句柄
        self.root = Tk()
        self.root.wm_title('Flip Card by Memory —— Charles的皮卡丘')
        # 游戏界面中的卡片字典
        self.game_matrix = {}
        # 背景图像
        self.blank_image = PhotoImage(data=cfg.IMAGEPATHS['blank'])
        # 卡片背面
        self.cards_back_image = PhotoImage(data=cfg.IMAGEPATHS['cards_back'])
        # 所有卡片的索引
        cards_list = list(range(8)) + list(range(8))
        random.shuffle(cards_list)
        # 在界面上显示所有卡片的背面
        for r in range(4):
            for c in range(4):
                position = f'{r}_{c}'
                self.game_matrix[position] = Label(self.root, image=self.cards_back_image)
                self.game_matrix[position].back_image = self.cards_back_image
                self.game_matrix[position].file = str(cards_list[r * 4 + c])
                self.game_matrix[position].show = False
                self.game_matrix[position].bind('<Button-1>', self.clickcallback)
                self.game_matrix[position].grid(row=r, column=c)
        # 已经显示正面的卡片
        self.shown_cards = []
        # 场上存在的卡片数量
        self.num_existing_cards = len(cards_list)
        # 显示游戏剩余时间
        self.num_seconds = 30
        self.time = Label(self.root, text=f'Time Left: {self.num_seconds}')
        self.time.grid(row=6, column=3, columnspan=2)
        # 居中显示
        self.root.withdraw()
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2
        y = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 2
        self.root.geometry('+%d+%d' % (x, y))
        self.root.deiconify()
        # 计时
        self.tick()
        # 显示主界面
        self.root.mainloop()
    '''点击回调函数'''
    def clickcallback(self, event):
        card = event.widget
        if card.show: return
        # 之前没有卡片被翻开
        if len(self.shown_cards) == 0:
            self.shown_cards.append(card)
            image = ImageTk.PhotoImage(Image.open(os.path.join(self.card_dir, card.file+'.png')))
            card.configure(image=image)
            card.show_image = image
            card.show = True
        # 之前只有一张卡片被翻开
        elif len(self.shown_cards) == 1:
            # --之前翻开的卡片和现在的卡片一样
            if self.shown_cards[0].file == card.file:
                def delaycallback():
                    self.shown_cards[0].configure(image=self.blank_image)
                    self.shown_cards[0].blank_image = self.blank_image
                    card.configure(image=self.blank_image)
                    card.blank_image = self.blank_image
                    self.shown_cards.pop(0)
                    self.score_sound.play()
                self.num_existing_cards -= 2
                image = ImageTk.PhotoImage(Image.open(os.path.join(self.card_dir, card.file+'.png')))
                card.configure(image=image)
                card.show_image = image
                card.show = True
                card.after(300, delaycallback)
            # --之前翻开的卡片和现在的卡片不一样
            else:
                self.shown_cards.append(card)
                image = ImageTk.PhotoImage(Image.open(os.path.join(self.card_dir, card.file+'.png')))
                card.configure(image=image)
                card.show_image = image
                card.show = True
        # 之前有两张卡片被翻开
        elif len(self.shown_cards) == 2:
            # --之前翻开的第一张卡片和现在的卡片一样
            if self.shown_cards[0].file == card.file:
                def delaycallback():
                    self.shown_cards[0].configure(image=self.blank_image)
                    self.shown_cards[0].blank_image = self.blank_image
                    card.configure(image=self.blank_image)
                    card.blank_image = self.blank_image
                    self.shown_cards.pop(0)
                    self.score_sound.play()
                self.num_existing_cards -= 2
                image = ImageTk.PhotoImage(Image.open(os.path.join(self.card_dir, card.file+'.png')))
                card.configure(image=image)
                card.show_image = image
                card.show = True
                card.after(300, delaycallback)
            # --之前翻开的第二张卡片和现在的卡片一样
            elif self.shown_cards[1].file == card.file:
                def delaycallback():
                    self.shown_cards[1].configure(image=self.blank_image)
                    self.shown_cards[1].blank_image = self.blank_image
                    card.configure(image=self.blank_image)
                    card.blank_image = self.blank_image
                    self.shown_cards.pop(1)
                    self.score_sound.play()
                self.num_existing_cards -= 2
                image = ImageTk.PhotoImage(Image.open(os.path.join(self.card_dir, card.file+'.png')))
                card.configure(image=image)
                card.show_image = image
                card.show = True
                card.after(300, delaycallback)
            # --之前翻开的卡片和现在的卡片都不一样
            else:
                self.shown_cards.append(card)
                self.shown_cards[0].configure(image=self.cards_back_image)
                self.shown_cards[0].show = False
                self.shown_cards.pop(0)
                image = ImageTk.PhotoImage(Image.open(os.path.join(self.card_dir, card.file+'.png')))
                self.shown_cards[-1].configure(image=image)
                self.shown_cards[-1].show_image = image
                self.shown_cards[-1].show = True
        # 判断游戏是否已经胜利
        if self.num_existing_cards == 0:
            is_restart = messagebox.askyesno('Game Over', 'Congratulations, you win, do you want to play again?')
            if is_restart: self.restart()
            else: self.root.destroy()
    '''播放背景音乐'''
    def playbgm(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(cfg.AUDIOPATHS['bgm'])
        pygame.mixer.music.play(-1, 0.0)
    '''计时'''
    def tick(self):
        if self.num_existing_cards == 0: return
        if self.num_seconds != 0:
            self.num_seconds -= 1
            self.time['text'] = f'Time Left: {self.num_seconds}'
            self.time.after(1000, self.tick)
        else:
            is_restart = messagebox.askyesno('Game Over', 'You fail since time up, do you want to play again?')
            if is_restart: self.restart()
            else: self.root.destroy()
    '''重新开始游戏'''
    def restart(self):
        self.root.destroy()
        client = FlipCardByMemory()


'''run'''
if __name__ == '__main__':
    client = FlipCardByMemory()