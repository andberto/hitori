'''
HITORI GAME
Parma, 11/12/19
Andrea Bertogalli
'''

import tkinter

SCREEN_WIDTH = tkinter.Tk().winfo_screenwidth()
SCREEN_HEIGTH = tkinter.Tk().winfo_screenheight()
SCREEN_MARGIN = 150
CLEAR = "CL"
BLACK = "BL"
CIRCLE = "CI"
CELLS_SPRITE_WIDTH = 60
CELLS_SPRITE_HEIGHT = 60
LONG_PRESS = 0.5
CIRCUMFERENCE_BORDER_WIDTH = 5
DIRECTIONS = [(0,1),(0,-1),(1,0),(-1,0)]
OFFLINE_PUZZLES_DIR = "offline_puzzles"
PUZZLES_DIMENSIONS = [5,6,8]
HITORI_LOGO = "resources/logo.png"
CLEAR_SPRITE = "resources/cell_clear.png"
BLACK_SPRITE = "resources/cell_black.png"
CIRCLE_SPRITE = "resources/cell_circle.png"
BACKGROUND_SPRITE = "resources/menu_background.png"
BACKGROUND_SPRITE_WIDTH = 960
BACKGROUND_BUTTON_SPRITE_SIDE = 30
RELEASED_MENU_BUTTON_SPRITE = "resources/button_up.png"
PRESSED_MENU_BUTTON = "resources/button_down.png"
TOGGLE_MENU_BUTTON = "resources/toggle_button.png"
TOGGLE_MENU_BUTTON_WIDTH = 84
LOGO_WIDTH = 99
LOGO_HEIGHT = 99
SHOW_MENU = 0
HIDE_MENU = 1
HIDE_SPACING = 35
SHOW_SPACING = 170
BUTTONS = range(4)
BUTTONS_TEXT = ["INFO","NEW PUZZLE","RESTART","SOLVE"]
LEFT_SPACING = 20
INFO = 0
RESTART = 2
NEW_PUZZLE = 1
SOLVE = 3
INFO_MESSAGE = ("1) left click to play on a cell\\n" +
               "2) left click (long press) annotation on a cell\\n" +
               "3) middle click click to remove the annotation on a cell\\n" + 
               "4) spacebar to use the helps function\\n" +
               "5) enter to use the advanced helps function\\n" +
               "6) hitori rules at: https://it.wikipedia.org/wiki/Hitori")
HIGH_PRIORITY_FILE = None
ALERT_DELAY = 10