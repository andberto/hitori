def abstract():
    raise NotImplementedError("Abstract method")

class BoardGame:
    def play_at(self, y: int, x: int): abstract()
    def flag_at(self, y: int, x: int): abstract()
    def value_at(self, y: int, x: int) -> str: abstract()
    def annotation_at(self, y: int, x: int) -> str: abstract()
    def get_side(self) -> int: abstract()
    def finished(self) -> bool: abstract()
    def solve(self) -> bool: abstract()
    def new_puzzle(self): abstract()
    def solved_message(self) -> str: abstract() 
    def remove_annotations(self): abstract()


def print_game(game: BoardGame):
    for y in range(game.get_side()):
        for x in range(game.get_side()):
            val = game.value_at(x, y)
            print(f"{val:3}", end='')
        print()

def console_play(game: BoardGame):
    print_game(game)

    while not game.finished():
        x, y = input().split(' ')
        game.play_at(int(x), int(y))
        print_game(game)

    print(game.solved_message())
