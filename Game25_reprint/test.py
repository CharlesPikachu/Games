#!/usr/bin/python
#coding:utf-8
 
#python Game
 
 
import sys
import random
 
class MineSweeping():
    # Main mine clearance procedure
    def __init__(self,row = 8 ,line= 8,mineNum = 15):
        self.row = row
        self.line = line
        self.score = 0 #Score
        self.mineNum = mineNum
        self.xy_list = [[0 for i in range(self.line)] for i in range(self.row)]
    # InitData
    def initData(self):
        self.xy_list = [[0 for i in range(self.line)] for i in range(self.row)]
        maxMine = self.mineNum
        while maxMine > 0 :
            num_x = random.randint(0,self.row-1)
            num_y = random.randint(0,self.line-1)
            if self.xy_list[num_x][num_y] == 0:
                self.xy_list[num_x][num_y] = 1
                maxMine -= 1
 
    #get x
    def get_pos(self,str_pos):
        while 1:
            try:
                num_x = raw_input(str_pos)
                if int(num_x) in range(self.line) and num_x :
                    break
                else:
                    print u'Input invalid value'
            except:
                pass
        return int(num_x)
 
    #For mine
    def  mine_clear(self,x,y):
        # Get number
        pos = self.xy_list[x][y]
        if pos == 0 :
            self.xy_list[x][y] = 2
            return 0
        elif pos == 2 :
            return 2
        else:
            return 1
 
    # Display of the interface
    def mineFace(self,state):
        if state == 1:
            print '+=================+'
            print '     Game start    '
            print '+=================+'
            tt = ' #'
            print '**************************'
            for i in range(self.line):
                str_t = ''
                for t in xrange(self.row):
                    str_t += tt
                print "|%s|"%(str_t,)
            print '**************************'
            print 'Please input values of x,y(0-7):'
        # Refresh interfacec
        if state == 2:
            tt = ' #'
            print '**************************'
            for i in range(self.line):
                str_t = ''
                for t in xrange(self.row):
                    if self.xy_list[i][t] == 2:
                        str_t += str(self.xy_list[i][t]).rjust(2)
                    else:
                        str_t += tt
                print "|%s|"%(str_t,)
            print '**************************'
        if state == 3:
            print '**************************'
            for i in range(self.line):
                str_t = ''
                for t in xrange(self.row):
                    if int(self.xy_list[i][t]) != 1:
                        str_t += ' 2'
                    else:
                        str_t += ' *'
                print "|%s|"%(str_t,)
            print '**************************'
 
        if  state == 4:
            tt = ' #'
            print '**************************'
            for i in range(self.line):
                str_t = ''
                for t in xrange(self.row):
                    if self.xy_list[i][t] == 2:
                        str_t += str(self.xy_list[i][t]).rjust(2)
                    else:
                        str_t += ' @'
                print "|%s|"%(str_t,)
            print '**************************'
 
 
    def MainLoop(self):
        self.mineFace(1)
        self.score = 0
        self.initData()
        #print self.xy_list
 
 
        # Main loop
        while 1:
            #get x,y
            x = self.get_pos(' X = ')
            y = self.get_pos(' Y = ')
            num = self.mine_clear(x,y)

            win = True
            for i in self.xy_list:
                if 0 in i:
                    win = False
                    break
            if win:
                num = 4
 

            if num == 0:
                self.mineFace(2)
                self.score += 10
            elif num == 2:
                print u'This position has already been cleared.'
            elif num == 1:
                print '+=================+'
                print '     Game over    '
                print '+=================+'
                print u'SCORE : ', self.score
                self.mineFace(3)

                next = raw_input(u'Whether to play the next game :Y or N ')
                if next.upper().startswith('Y'):
                    print u'The Next Inning Begins'
                    self.nextGame()
                else:
                    print '>>> Game exit'
                    break
            else:
                self.score += 10
                print u'Congratulations'
                print u'SCORE : ', self.score
                self.mineFace(4)
                next = raw_input(u'Whether to play the next game :Y or N ')
                if next.upper().startswith('Y'):
                    print u'Next Time'
                    self.nextGame()
                else:
                    print '>>> Game exit'
                    break
 
    # Initial Information
    def nextGame(self):
        self.mineFace(1)
        self.score = 0
        self.initData()
 
 
if __name__ == '__main__':
    mi = MineSweeping(10,10,20)
    mi.MainLoop()
    sys.exit()