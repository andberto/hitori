'''
HITORI GAME
Parma, 11/12/19
Andrea Bertogalli
'''

import g2d
from BoardGame import BoardGame
from time import time
import Constants

class BoardGameGui:
    def __init__(self, g: BoardGame):
        self._game = g
        self._cell_side = (min(Constants.SCREEN_WIDTH,Constants.SCREEN_HEIGTH) - Constants.SHOW_SPACING - Constants.SCREEN_MARGIN) // self._game.get_side() 
        self._downtime = 0
        self._clear = g2d.load_image(Constants.CLEAR_SPRITE)
        self._black = g2d.load_image(Constants.BLACK_SPRITE)
        self._circle = g2d.load_image(Constants.CIRCLE_SPRITE)
        self._menu_background = g2d.load_image(Constants.BACKGROUND_SPRITE)
        self._released_menu_button = g2d.load_image(Constants.RELEASED_MENU_BUTTON_SPRITE)
        self._toggle_menu_button = g2d.load_image(Constants.TOGGLE_MENU_BUTTON)
        self._pressed_menu_button = g2d.load_image(Constants.PRESSED_MENU_BUTTON)
        self._buttons_interactive_areas = []
        self._menu = False
        self._show_confirm = False
        self._confirm_delay = 0
        self._spacing = Constants.HIDE_SPACING
        self._menu_button_interactive_area = ((self._game.get_side() * self._cell_side)//2 - Constants.TOGGLE_MENU_BUTTON_WIDTH // 2,self._spacing - Constants.BACKGROUND_BUTTON_SPRITE_SIDE,(self._game.get_side() * self._cell_side)//2 + Constants.TOGGLE_MENU_BUTTON_WIDTH // 2 ,self._spacing)
        self.update_buttons()

    def tick(self):
        if g2d.key_pressed("Spacebar"): self._game.help_user()
        elif g2d.key_pressed("Enter"): self._game.all_helps(self._game.first_clear())
        elif g2d.key_pressed("MiddleButton"):
            mouse = g2d.mouse_position()
            x, y = mouse[0] // self._cell_side, (mouse[1] - self._spacing) // self._cell_side
            self._game.clear_at(y,x)
        elif g2d.key_pressed("LeftButton"): self._downtime = time()
        elif g2d.key_released("LeftButton"):
            mouse = g2d.mouse_position()
            x, y = mouse[0] // self._cell_side, (mouse[1] - self._spacing) // self._cell_side
            if 0 <= y < self._game.get_side() and 0 <= x < self._game.get_side(): 
                if time() - self._downtime > Constants.LONG_PRESS:
                    self._game.flag_at(y, x)
                else:
                    self._game.play_at(y, x)
            else: self.check_buttons_click(mouse[1],mouse[0])
        self.update_buttons()

    def check_buttons_click(self,y,x):
        #verifico pressione bottoni con mouse (controllo aree interattive del canvas)
        if self._menu_button_interactive_area[0] <=  x <= self._menu_button_interactive_area[2] and self._menu_button_interactive_area[1] <=  y <= self._menu_button_interactive_area[3]:
            self._menu = not self._menu
            if self._menu: self._spacing = Constants.SHOW_SPACING
            else: self._spacing = Constants.HIDE_SPACING
            g2d.init_canvas(((self._game.get_side() * self._cell_side), (self._game.get_side() * self._cell_side)+ self._spacing))  
            self._menu_button_interactive_area = ((self._game.get_side() * self._cell_side)//2 - Constants.TOGGLE_MENU_BUTTON_WIDTH // 2,self._spacing - Constants.BACKGROUND_BUTTON_SPRITE_SIDE,(self._game.get_side() * self._cell_side)//2 + Constants.TOGGLE_MENU_BUTTON_WIDTH // 2 ,self._spacing)
            return

        for area in self._buttons_interactive_areas:
            if area[0] <=  x <= area[2] and area[1] <=  y <= area[3]:
                if self._buttons_interactive_areas.index(area) == Constants.INFO: 
                    g2d.alert(Constants.INFO_MESSAGE)
                elif self._buttons_interactive_areas.index(area) == Constants.NEW_PUZZLE: 
                    self._game.new_puzzle()
                    self._game.start_chrono()
                    self._cell_side = (min(Constants.SCREEN_WIDTH,Constants.SCREEN_HEIGTH) - Constants.SHOW_SPACING - Constants.SCREEN_MARGIN) // self._game.get_side() 
                    g2d.init_canvas(((self._game.get_side() * self._cell_side), (self._game.get_side() * self._cell_side)+ self._spacing))
                elif self._buttons_interactive_areas.index(area) == Constants.RESTART: 
                    self._game.remove_annotations()
                    self._game.start_chrono()
                elif self._buttons_interactive_areas.index(area) == Constants.SOLVE:
                    self._game.remove_annotations()
                    self._game.start_chrono()
                    self._game.solve() 
                g2d.draw_image(self._pressed_menu_button,(area[0],area[1]))
                return

    def draw_menu(self, side: int):
        self._buttons_interactive_areas.clear()
        g2d.draw_image(self._menu_background,(-(Constants.BACKGROUND_SPRITE_WIDTH - side * self._cell_side),0))
        g2d.set_color((255, 255, 0))
        g2d.draw_image(self._toggle_menu_button,((side * self._cell_side)//2 - Constants.TOGGLE_MENU_BUTTON_WIDTH // 2,self._spacing - Constants.BACKGROUND_BUTTON_SPRITE_SIDE - 2))
        g2d.draw_text_centered("Andrea Bertogalli",(side * self._cell_side - 95,self._spacing - 10 ),15)
        btn_spacing = (Constants.SHOW_SPACING - (len(Constants.BUTTONS) * Constants.BACKGROUND_BUTTON_SPRITE_SIDE)) // len(Constants.BUTTONS)
        g2d.set_color((0, 0, 0))
        if not self._menu: return
        
        g2d.set_color((255, 255, 0))
        for i in Constants.BUTTONS:
            g2d.draw_image(self._released_menu_button,(Constants.LEFT_SPACING,(i*(Constants.BACKGROUND_BUTTON_SPRITE_SIDE + btn_spacing)+5)))
            g2d.draw_text(Constants.BUTTONS_TEXT[i],(Constants.LEFT_SPACING + Constants.BACKGROUND_BUTTON_SPRITE_SIDE + 5,(i*(Constants.BACKGROUND_BUTTON_SPRITE_SIDE + btn_spacing)+10)),20)
            self._buttons_interactive_areas.append((Constants.LEFT_SPACING,(i*(Constants.BACKGROUND_BUTTON_SPRITE_SIDE + btn_spacing)+5),Constants.LEFT_SPACING + Constants.BACKGROUND_BUTTON_SPRITE_SIDE,(i*(Constants.BACKGROUND_BUTTON_SPRITE_SIDE + btn_spacing)+5) + Constants.BACKGROUND_BUTTON_SPRITE_SIDE))
        g2d.draw_text(self._game.hitori_info()[0] + ", N." + self._game.hitori_info()[1],(side * self._cell_side - 140,2),20)
        g2d.set_color((0, 0, 0))

    def update_buttons(self):
        g2d.clear_canvas()
        g2d.set_color((0, 0, 0))
        side = self._game.get_side()
        self.draw_menu(side)

        for y in range(side):
            for x in range(side):
                if self._game.annotation_at(y,x) == Constants.CLEAR:
                    g2d.draw_image_clip(self._clear,(0,0,Constants.CELLS_SPRITE_WIDTH,Constants.CELLS_SPRITE_HEIGHT),(x*self._cell_side, y*self._cell_side+self._spacing,self._cell_side,self._cell_side))
                    g2d.draw_text_centered(self._game.value_at(y, x), (x * self._cell_side + self._cell_side//2, (y * self._cell_side + self._cell_side//2)+ self._spacing), self._cell_side//2)
                elif self._game.annotation_at(y,x) == Constants.BLACK:
                    g2d.draw_image_clip(self._black,(0,0,Constants.CELLS_SPRITE_WIDTH,Constants.CELLS_SPRITE_HEIGHT),(x*self._cell_side, y*self._cell_side+self._spacing,self._cell_side,self._cell_side))
                elif self._game.annotation_at(y,x) == Constants.CIRCLE:
                    g2d.draw_image_clip(self._circle,(0,0,Constants.CELLS_SPRITE_WIDTH,Constants.CELLS_SPRITE_HEIGHT),(x*self._cell_side, y*self._cell_side+self._spacing,self._cell_side,self._cell_side))
                    g2d.draw_text_centered(self._game.value_at(y, x), (x * self._cell_side + self._cell_side//2, (y * self._cell_side + self._cell_side//2) + self._spacing), self._cell_side//2)

        g2d.update_canvas()

        if self._game.finished():
            if self._show_confirm:
                g2d.alert(self._game.solved_message())
                self._game.remove_annotations()
                self._game.start_chrono()
                self._show_confirm = False
                self._confirm_delay = 0
                return
            self._show_confirm = self._confirm_delay == Constants.ALERT_DELAY
            self._confirm_delay += 1

def gui_play(game: BoardGame):
    cs = (min(Constants.SCREEN_WIDTH,Constants.SCREEN_HEIGTH) - Constants.SHOW_SPACING - Constants.SCREEN_MARGIN) // game.get_side()     
    g2d.init_canvas(((game.get_side() * cs), (game.get_side() * cs) + Constants.HIDE_SPACING))
    ui = BoardGameGui(game)
    g2d.main_loop(ui.tick)
