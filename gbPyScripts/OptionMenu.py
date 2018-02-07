import sys
import os
import subprocess
import curses
import curses.ascii
from fuzzywuzzy import fuzz

class OptionMenu():
    def __init__(self,y,x,h,w):
        self.setSize(y,x,h,w)
        self.offset = 0
        self.options = []
        self.sorted = None
        self.selection = 0
        self.reader = (lambda x: x)
        self.sorting = (lambda x: x)

    def setOptions(self,options):
        self.options = options 
        self.offset = 0
        self.selection = 0
        self.removeSort()

    def setReader(f):
        self.reader = f

    def setSize(self, y, x, h, w):
        self.x = x
        self.y = y 
        self.h = h
        self.w = w

    def setView(self, selection, offset):
        self.selection = selection
        self.offset = offset

    def getView(self):
        return self.selection, self.offset

    def moveUp(self):
        self.selection = max(self.selection-1,0)
        if self.selection < self.offset:
            self.offset = self.selection

    def moveDown(self):
        self.selection = min(self.selection+1, len(self.options)-1)
        if self.selection >= self.offset + self.h: 
            self.offset = self.selection - self.h +1 

    def getSelection(self):
        return self.getOptions()[self.selection]

    def addSort(self, f):
        self.selection = 0
        self.sorting = f
        self.sorted = sorted(self.options, key=self.sorting, reverse=True)
    
    def removeSort(self):
        self.sorting = (lambda x: x)
        self.selection = 0
        self.sorted = None

    def getOptions(self):
        if self.sorted == None:
            return self.options
        else:
            return self.sorted

    def draw(self,stdscr):
        for i in range(self.h):
            stdscr.addstr(self.y+i, self.x, ' '*(self.w-1))
            if i < len(self.getOptions()):
                index = i + self.offset
                v = self.reader(self.getOptions()[index])
                v = v if len(v) < (self.w-1) else v[:self.w-1]
                if index == self.selection:
                    stdscr.addstr(self.y+i,self.x,v,curses.color_pair(1))
                else:
                    stdscr.addstr(self.y+i,self.x,v)
        
