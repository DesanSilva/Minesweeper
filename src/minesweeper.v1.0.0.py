from tkinter import *
import numpy as np
import random
import sys
import os

BASE_PATH = sys._MEIPASS if getattr(sys, "frozen", False) else os.path.abspath("../assets")
ICON_PATH = os.path.join(BASE_PATH, "icon.ico")

class Minesweeper():
    def __init__(self, mines=50):
        self.board_size = 500
        self.number_of_mines = mines
        print(f'left click to uncover a square \nright click to mark a square \nmiddle click to reset')
        
        self.window = Tk()
        self.window.title('Minesweeper')
        self.window.iconbitmap(ICON_PATH)
        
        self.canvas = Canvas(self.window, width=self.board_size, height=self.board_size)
        self.canvas.pack()

        self.window.bind('<Button-1>', self.uncover)           # left click
        self.window.bind('<Button-2>', self.reset_board)       # middle click
        self.window.bind('<Button-3>', self.flag_mines)        # right click

        self.initialize_board()
        self.board_status = np.zeros(shape=(20, 20))
        self.create_mines()
        
    '''
    Board Status
    
    0 - no mine unflagged covered
    1 - mine unflagged covered
    2 - no mine flagged covered
    3 - mine flagged covered
    4 - no mine unflagged uncovered
    5 - no mine flagged uncovered
    6 - clicked on mine
    7,8 - final state uneditable
    '''
    
    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(19):
            x = (i + 1) * self.board_size / 20
            self.canvas.create_line(x, 0, x, self.board_size)  # vertical lines
        for i in range(19):
            y = (i + 1) * self.board_size / 20
            self.canvas.create_line(0, y, self.board_size, y)  # horizontal lines

    def create_mines(self):
        for i in range(self.number_of_mines):
            x, y = random.randint(0, 19), random.randint(0, 19)
            self.board_status[x][y] = 1
            
    def colour(self, num):
        if num == 0:
            return '#C0C0C0'
        elif num == 1:
            return '#0000FF'
        elif num == 2:
            return '#017E00'
        elif num == 3:
            return '#FF0000'
        elif num == 4:
            return '#010180'
        elif num == 5:
            return '#810101'
        elif num == 6:
            return '#008080'
        elif num == 7:
            return '#000000'
        elif num == 8:
            return '#808080'

    def draw(self, x, y, tile_colour, outline = None):
        self.canvas.create_rectangle((x+0.5) * (self.board_size / 20)-12, (y+0.5) * (self.board_size / 20)-12,
                                     (x+0.5) * (self.board_size / 20)+12, (y+0.5) * (self.board_size / 20)+12,
                                     fill = tile_colour, outline = outline)

    def write(self, text_type, x=None, y=None, text=None):
        '''
        text type
        0 - cell numbers
        1 - win/lose message
        2 - reset message
        '''
        if (text_type == 0):
            self.canvas.create_text((x+0.5) * (self.board_size / 20), (y+0.5) * (self.board_size / 20),
                                    font="cmr 15 bold", fill=self.colour(self.check_3x3(x, y)),
                                    text=self.check_3x3(x, y))
        elif (text_type == 1):
            if (text=="You Lose"):
                colour = "#FF0000"
            elif (text=="You Win"):
                colour = "#00FF00"
            self.canvas.create_text(self.board_size / 2, self.board_size / 3,
                                    font='cmr 30 bold', fill=colour, text=text)
        elif (text_type == 2):
            self.canvas.create_text(self.board_size / 2, self.board_size * 3 / 4,
                                    font='cmr 20 bold', fill="#000000", text="Middle click to reset")

    def check_3x3(self, x, y):
        mines = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if 0 <= x+i < 20 and 0 <= y+j < 20:
                    if (self.board_status[x+i][y+j] == 1) or (self.board_status[x+i][y+j] == 3) or (self.board_status[x+i][y+j] == 6):
                        mines += 1
        return mines

    def flood_fill(self, x, y):
        if x < 0 or x >= 20 or y < 0 or y >= 20 or self.board_status[x][y] != 0:  # boundaries
            return 
        self.board_status[x][y] = 4
        self.draw(x, y, '#C0C0C0')
        self.write(0, x, y)
        if self.check_3x3(x, y) == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i != 0 or j != 0:
                        self.flood_fill(x+i, y+j)
                        
    def uncover(self, event):
        x = int(event.x // (self.board_size / 20))
        y = int(event.y // (self.board_size / 20))
        if self.board_status[x][y] == 0:
            self.flood_fill(x, y)
        if self.board_status[x][y] == 7:
            self.canvas.delete('all')
            self.write(1, text="You Lose")
            self.write(2)
        elif self.board_status[x][y] == 8:
            self.canvas.delete('all')
            self.write(1, text="You Win")
            self.write(2)
        elif self.board_status[x][y] == 1:
            self.board_status[x][y] = 6
            self.draw(x, y, '#FF0000')
            for x in range(20):
                for y in range(20):
                    if self.board_status[x][y] == 0:
                        self.draw(x, y, '#C0C0C0')
                    elif self.board_status[x][y] == 1:
                        self.draw(x, y, '#000000')
                    elif self.board_status[x][y] == 2:
                        self.draw(x, y, '#FFFF00')
            self.show_numbers()
            for x in range(20):
                for y in range(20):
                    self.board_status[x][y] = 7
        else:
            count = 0
            for x in range(20):
                for y in range(20):
                    if (self.board_status[x][y] == 0) or (self.board_status[x][y] == 2):
                        count += 1
            if count == 0:
                for x in range(20):
                    for y in range(20):
                        if self.board_status[x][y] == 1:
                            self.draw(x, y, '#00FF00')
                        self.board_status[x][y] = 8

    def flag_mines(self, event):
        x = int(event.x // (self.board_size / 20))
        y = int(event.y // (self.board_size / 20))
        if self.board_status[x][y] == 0:
            self.board_status[x][y] = 2
            self.draw(x, y, '#00FF00')
        elif self.board_status[x][y] == 1:
            self.board_status[x][y] = 3
            self.draw(x, y, '#00FF00')
        elif self.board_status[x][y] == 2:
            self.board_status[x][y] = 0
            self.draw(x, y, '#F0F0F0', '')
        elif self.board_status[x][y] == 3:
            self.board_status[x][y] = 1
            self.draw(x, y, '#F0F0F0', '')
        elif self.board_status[x][y] == 4:
            self.board_status[x][y] = 5
            self.draw(x, y, '#00FF00')
        elif self.board_status[x][y] == 5:
            self.board_status[x][y] = 4
            self.draw(x, y, '#C0C0C0')
            self.write(0, x, y)

    def show_numbers(self):
        for x in range(20):
            for y in range(20):
                if (self.board_status[x][y] == 0) or (self.board_status[x][y] == 2) or (self.board_status[x][y] == 4):
                    self.write(0, x, y)

    def reset_board(self, event):
        self.canvas.delete('all')
        self.initialize_board()
        self.board_status = np.zeros(shape=(20, 20))
        self.create_mines()

game_instance = Minesweeper()
game_instance.mainloop()
