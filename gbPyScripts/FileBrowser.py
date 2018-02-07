import sys
import os
import subprocess
import curses
import curses.ascii
from OptionMenu import OptionMenu
from fuzzywuzzy import fuzz

def FileBrowser(stdscr):
    stdscr.clear()
    curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_WHITE)
    menu = OptionMenu(2,2,10,15)
    stack = [['/Users/Greg/Dropbox',0,0,'']]
    changedDir = True
    result = ''
    done = False
    search = ''
    while not done:
        h, w = stdscr.getmaxyx()
        menu.setSize(1,1,h-2,w-2)
        cwd = stack[-1][0]
        if changedDir:
            search = ''
            options = os.listdir(cwd)
            options = [(x+'/' if os.path.isdir(os.path.join(cwd,x)) else x) for x in options]
            menu.setOptions(options)
            if len(stack[-1][3]) > 0:
                search = stack[-1][3]
                menu.addSort((lambda x: fuzz.partial_ratio(x.lower(),search.lower())))
            menu.setView(stack[-1][1], stack[-1][2])
            changedDir = False
        menu.draw(stdscr)
        stdscr.refresh()
        c = stdscr.getch()
        if c == curses.KEY_UP:
            menu.moveUp()
        elif c == curses.KEY_DOWN:
            menu.moveDown()
        elif c == curses.KEY_ENTER or c == 10 or c == 13:
            selection = menu.getSelection()
            if not os.path.isdir(os.path.join(cwd,selection)):
                result = '{}'.format(os.path.join(cwd,selection))
                done = True
        elif c == curses.KEY_RIGHT:
            selection = menu.getSelection()
            if os.path.isdir(os.path.join(cwd,selection)):
                stack[-1][1], stack[-1][2] = menu.getView()
                stack[-1][3] = search     
                stack.append([os.path.join(cwd,selection),0,0,''])
                changedDir = True
        elif c == curses.KEY_LEFT and len(stack) > 1:
            stack = stack[:-1]
            changedDir = True
        elif c == curses.KEY_BACKSPACE or c == 127: 
            if len(search) > 0:
                search = search[:-1]
                menu.addSort((lambda x: fuzz.partial_ratio(x.lower(),search.lower())))
            else:
                menu.removeSort()
        elif curses.ascii.isascii(c):
            search += chr(c)
            menu.addSort((lambda x: fuzz.partial_ratio(x.lower(),search.lower())))
    return result 

if __name__ == '__main__':
    result = curses.wrapper(FileBrowser)
    subprocess.call(['vim',result])

