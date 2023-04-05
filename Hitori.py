'''
HITORI GAME
Parma, 11/12/19
Andrea Bertogalli
'''

from BoardGame import BoardGame
import Constants
from operator import add
from time import time,gmtime,strftime
from itertools import combinations,chain
from HitoriDownloader import is_reachable, download_puzzle, get_offline_puzzle, puzzle_info
from random import choice

class Hitori(BoardGame):

    def __init__(self,path):
        if path != None: self._board = self.read_board(path) #se ho un parametro uso il file di parametro
        elif is_reachable(): self._board = download_puzzle(choice(Constants.PUZZLES_DIMENSIONS)) #se non ho un paramentro e (si connessione e host raggiungibile)
        else: self._board = self.read_board(Constants.OFFLINE_PUZZLES_DIR + "/" +get_offline_puzzle(Constants.OFFLINE_PUZZLES_DIR)) #se offline random file da directory (puzzle_offline)
        self._side = len(self._board)
        self._annotations = [[Constants.CLEAR for x in range(self._side)] for y in range(self._side)]    
        self._time_start = time()

    def get_side(self) -> int:
        '''
        returns the game board side 
        '''
        return self._side

    def hitori_info(self) -> str:
        '''
        returns the string with info of the current puzzle
        ex: see http://www.menneske.no/eng/ 
        '''
        return (str(self._side) + "x" + str(self._side),puzzle_info())

    def read_board(self, f: str) -> list:
        '''
        read an hitori bord from a csv file
        '''
        matrix = []
        with open(f, "r") as f:
            for line in f:
                matrix.append(line.strip().split(','))
        return matrix

    def solved_message(self) -> str:
        '''
        returns the message that appears on game finished
        '''
        return "Puzzle solved in: " + strftime("%H:%M:%S", gmtime((time() - self._time_start)))

    def value_at(self, y: int, x: int) -> str:
        '''
        returns the value in a specific cell
        (y,x) of the hitori board
        '''
        return self._board[y][x]
        
    def play_at(self, y: int, x: int):
        '''
        puts a black annotation at (y,x)
        if at (y,x) is already black or circled
        removes the annotation
        '''
        if self.annotation_at(y,x) == Constants.BLACK or self.annotation_at(y,x) == Constants.CIRCLE:
            self._annotations[y][x] = Constants.CLEAR
            return
        self._annotations[y][x] = Constants.BLACK
        
    def annotation_at(self, y: int, x: int) -> str:
        '''
        returns the annotation at (y,x)
        ex: BL, CL, CI
        '''
        return self._annotations[y][x]
    
    def start_chrono(self):
        '''
        begins to time
        '''
        self._time_start = time()

    def remove_annotations(self):
        '''
        removes all hitori board annotations
        '''
        self._annotations = [[Constants.CLEAR for x in range(self._side)] for y in range(self._side)]    
        
    def clear_at(self,y,x):
        '''
        remove the annotation at (y,x)
        '''
        self._annotations[y][x] = Constants.CLEAR
    
    def flag_at(self, y: int, x: int):
        '''
        puts a circle at (y,x)
        '''
        self._annotations[y][x] = Constants.CIRCLE

    def get_cells_by_type(self, typ: str) -> list:
        '''
        returns a list that contains all cells
        by type: black or (clear,circle)
        '''
        cells = []
        for i in range(0, self._side):
            for j in range(0, self._side):
                if self.annotation_at(i,j) == typ:
                    cells.append((i, j))
                elif self.annotation_at(i,j) == Constants.CIRCLE and typ == Constants.CLEAR:
                    cells.append((i, j))
        return cells

    def is_valid_cell(self, y: int ,x: int) -> bool:
        '''
        check if the cell at (y,x)
        has not black neighborns
        true -> wrong situation
        false -> corect situation
        '''
        black_cells = self.get_cells_by_type(Constants.BLACK)
        clicked_cell = (y,x)

        for k in range(len(Constants.DIRECTIONS)):
            if tuple(map(add,clicked_cell , Constants.DIRECTIONS[k])) in black_cells:
                return False
        return True   
             
    def check_black_adjacency(self):
        '''
        check if there are any black 
        adjacency
        true -> wrong situation
        false -> corect situation
        '''
        black_cells = self.get_cells_by_type(Constants.BLACK)
        for i in black_cells:
            if not self.is_valid_cell(i[0],i[1]):
                return False
        return True

    def check_rows_cols(self):
        '''
        check if there are duplicates in the board
        (on rows,cols)
        '''
        for i in range(self._side):
            if self.has_cross_duplicates(i): return False
        return True

    def has_cross_duplicates(self,level) -> bool:
        '''
        check if there are duplicates on x row and x col
        '''
        row = [col for idx,col in enumerate(self._board[level]) if self.annotation_at(level,idx) == Constants.CLEAR or self.annotation_at(level,idx) == Constants.CIRCLE]
        col = [row[level] for idx, row in enumerate(self._board) if self.annotation_at(idx,level) == Constants.CLEAR or self.annotation_at(idx,level) == Constants.CIRCLE]
        return len(row) != len(set(row)) or len(col) != len(set(col))

    def duplicates(self,lst: list, item) -> list:
        '''
        returns duplicates in a list
        '''
        return [i for i, x in enumerate(lst) if x == item]

    def new_puzzle(self):
        '''
        takes a new puzzle:
        see the file, "game_info.md"
        '''
        if is_reachable(): self._board = download_puzzle(choice(Constants.PUZZLES_DIMENSIONS))
        else: self._board = self.read_board(Constants.OFFLINE_PUZZLES_DIR + "/" +get_offline_puzzle(Constants.OFFLINE_PUZZLES_DIR))
        self._side = len(self._board)
        self.remove_annotations()    

    def help_user_with_circles(self):
        '''
        puts circles around black cells
        '''
        black_cells = self.get_cells_by_type(Constants.BLACK)
        for i in black_cells:
            for k in range(len(Constants.DIRECTIONS)):
                cell = tuple(map(add, i, Constants.DIRECTIONS[k]))
                if 0 <= cell[0] < self._side and 0 <= cell[1] < self._side and self.annotation_at(cell[0],cell[1]) == Constants.CLEAR:
                    self._annotations[cell[0]][cell[1]] = Constants.CIRCLE

    def help_user_with_duplicates(self):
        '''
        for each circle put blacks all duplicates
        on row,col
        '''
        white_cells = self.get_cells_by_type(Constants.CLEAR)
        for cell in white_cells:
            if self.annotation_at(cell[0],cell[1]) == Constants.CIRCLE:
                value = self.value_at(cell[0],cell[1])
                row = self._board[cell[0]]
                col = [row[cell[1]] for row in self._board]
                for j in range(self._side):
                    if row[j] == value and j != cell[1]:
                        self._annotations[cell[0]][j] = Constants.BLACK
                    if col[j] == value and j != cell[0]:
                        self._annotations[j][cell[1]] = Constants.BLACK

    def first_clear(self):
        '''
        returns the first clear cell
        '''
        white_cells = self.get_cells_by_type(Constants.CLEAR)
        for i in white_cells:
            if self._annotations[i[0]][i[1]] == Constants.CLEAR: return i

    def mark_auto(self):
        '''
        mark all the obvious cell
        '''
        white_cells = self.get_cells_by_type(Constants.CLEAR)
        for i in white_cells: 
            if self.annotation_at(i[0],i[1]) == Constants.CLEAR: 
                self.all_helps(i)

    def all_helps(self,cell):
        '''
        tries to mark (circle or blacks) a cell
        '''
        backup = [row[:] for row in self._annotations]

        self._annotations[cell[0]][cell[1]] = Constants.BLACK #provo ad annerire
        self.help_user() #applico automatismi
    
        if self.wrong(): 
            self._annotations = [row[:] for row in backup]
            self._annotations[cell[0]][cell[1]] = Constants.CIRCLE
        m1 = [row[:] for row in self._annotations]
        self._annotations = [row[:] for row in backup]

        self._annotations[cell[0]][cell[1]] = Constants.CIRCLE #provo a cerchiare
        self.help_user() #applico automatismi
        
        if self.wrong(): 
            self._annotations = [row[:] for row in backup]
            self._annotations[cell[0]][cell[1]] = Constants.BLACK
        m2 = [row[:] for row in self._annotations]
        self._annotations = [row[:] for row in backup]

        for i in range(self._side):
            for j in range(self._side):
                if m1[i][j] == m2[i][j] and m1[i][j] != Constants.CLEAR and m2[i][j] != Constants.CLEAR:
                    self._annotations[i][j] = m1[i][j]
    
    def help_user(self):
        '''
        calls all helps methods
        '''
        self.help_user_with_duplicates()
        self.help_user_with_circles()

    def solve(self) -> bool:
        '''
        solves the hitori matrix (recursively)
        '''
        self.mark_auto()  # annota tutte le celle ovvie
        if self.wrong(): return False 

        cell = self.first_clear()
                
        if cell != None:
            backup = [row[:] for row in self._annotations]
            for annot in [Constants.BLACK,Constants.CIRCLE]:
                self._annotations[cell[0]][cell[1]] = annot
                if self.solve():
                    return True
                self._annotations = [row[:] for row in backup] #backup
        return self.finished()

    def check_circles_sequence(self) -> bool:
        '''
        check if 2 equal value on the same (row,col)
        are circled
        '''
        for level in range(self._side):
            row = self._board[level]
            col = [row[level] for row in self._board]

            duplicates_row = list(set(tuple(self.duplicates(row, i)) for i in row if len(self.duplicates(row, i)) > 1 ))
            duplicates_col = list(set(tuple(self.duplicates(col, i)) for i in col if len(self.duplicates(col, i)) > 1 ))
            for i in duplicates_row:
                if self.annotation_at(level,i[0]) == Constants.CIRCLE and self.annotation_at(level,i[1]) == Constants.CIRCLE: 
                    return False

            for i in duplicates_col:
                if self.annotation_at(i[0],level) == Constants.CIRCLE and self.annotation_at(i[1],level) == Constants.CIRCLE: 
                    return False
        return True
    
    def finished(self) -> bool:
        '''
        check if the game is finished
        '''
        return self.check_rows_cols() and self.check_black_adjacency() and self.check_white_connections()
        
    def wrong(self) -> bool:
        '''
        check if the game is at a dead end 
        '''
        return not(self.check_circles_sequence() and self.check_black_adjacency() and self.check_white_connections())

    def check_white_connections(self) -> bool:
        '''
        check if all white cells (circle,clear)
        are connected
        '''
        white_cells = self.get_cells_by_type(Constants.CLEAR)
        if len(white_cells) == 0: return True
        cell = white_cells[0]
        graph = [[False for x in range(self._side)] for y in range(self._side)]
        self.fill_graph(graph,cell)

        reachable_vertices,total_white = sum([row.count(True) for row in graph]),len(self.get_cells_by_type(Constants.CLEAR))
        return reachable_vertices == total_white #confronto nodi raggiunti con celle bianche

    def fill_graph(self,graph,cell):
        '''
        mark with true the reachable white cells
        '''
        graph[cell[0]][cell[1]] = True

        for k in range(len(Constants.DIRECTIONS)): #per ogni direzione (celle vicine)
                nearby_cell = tuple(map(add, cell, Constants.DIRECTIONS[k]))
                if 0 <= nearby_cell[0] < self._side and 0 <= nearby_cell[1] < self._side: #se la cella è valida metto a true
                    if (not graph[nearby_cell[0]][nearby_cell[1]]) and (self.annotation_at(nearby_cell[0],nearby_cell[1]) == Constants.CLEAR or self.annotation_at(nearby_cell[0],nearby_cell[1]) == Constants.CIRCLE):
                        graph[nearby_cell[0]][nearby_cell[1]] = True
                        self.fill_graph(graph,nearby_cell)
