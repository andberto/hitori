'''
HITORI GAME
Parma, 11/12/19
Andrea Bertogalli
'''

from Hitori import Hitori
from g2d import alert
from BoardGameGui import gui_play
from BoardGame import console_play
from Constants import HIGH_PRIORITY_FILE

def main():
    game = Hitori(HIGH_PRIORITY_FILE)
    gui_play(game)
    #console_play(game)

main() 
