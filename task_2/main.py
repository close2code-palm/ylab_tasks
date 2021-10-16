"""AI, numpy and game theory versus YOU"""
import sys
from os import system, name
from random import choice

import numpy
import numpy as np

MARKS = {'X', 'O', '+', '-', '@', '$'}


# not important in case of usbility but this fun is pure FP
def choose_mark() -> MARKS:
    """Gets player's input string to choose the game mark to play."""
    print(MARKS)
    mark_input = input(f"Please, choose Your mark(#, for default, or {MARKS}):")
    mark_input = filter(lambda m: m in MARKS, mark_input)
    # somehow validate!!!
    mark = str(mark_input) or '#'
    return mark


GAME_BOARD = np.zeros((10, 10))
BOARD_VIEW = np.zeros((11, 11))

BOARD_VIEW[0] = np.arange(-1, 10)

for i in range(-1, 10):
    BOARD_VIEW[0][i] = i

# masks
POSSIBLE_TURNS = np.ones((10, 10))

# will be integrated after algorythm
h_player_mark = '#'

# used to track 'turn owners'
TURN_FLAG = False

PLAYER_CODE = 0
AI_CODE = 1

def choose_first():
    """Returns boolean value whether the player wins the game."""
    return choice((1, 2))


def show_board():
    """Displays game progress"""
    print(BOARD_VIEW)


def h_turn_inp():
    """Taking coordinates in turn from brave player"""
    print("Now its your turn!!!")
    coord_x = input("Enter your choice(x):")
    coord_y = input("Enter your choice(y):")
    return int(coord_x), int(coord_y)


# THis func is not urgent
def display():
    """Shows board in human readable format"""
    for i in range(10):
        for j in range(10):
            if GAME_BOARD[i][j] == 11111:
                pass


def check_out_space():
    """Waits until all fields are occupied"""
    if set(BOARD_VIEW) == {1, 2}:
        game_finish_output(0)


def game_finish_output(winner_code):
    if not winner_code:
        sys.exit('Draw, game board is empty')
    else:
        sys.exit(f'Player {winner_code} wins!!!')


def game_finish_check():
    """Looking for win strokes on the board.
    Vertical, horizontal lines, or diagonals"""
    for i in range(7):
        for j in range(7):
            win_cond_diag = (GAME_BOARD[i][j] == GAME_BOARD[i + 1][j + 1] == GAME_BOARD[i + 2][j + 2]
                             == GAME_BOARD[i + 3][j + 3] == GAME_BOARD[i + 4][j + 4])
            if win_cond_diag:
                game_finish_output(PLAYER_CODE)
        for j in range(10):
            win_cond_vert = (GAME_BOARD[i][j] == GAME_BOARD[i + 1][j] == GAME_BOARD[i + 2][j]
                             == GAME_BOARD[i + 3][j] == GAME_BOARD[i + 4][j])
            if win_cond_vert:
                game_finish_output(PLAYER_CODE)
    # untesteted, we could nest cycle and shadow outer i counter, more readable
    for i in range(10):
        for j in range(7):
            win_cond_hor = (GAME_BOARD[i][j] == GAME_BOARD[i][j + 1] == GAME_BOARD[i][j + 2]
                            == GAME_BOARD[i][j + 3] == GAME_BOARD[i][j + 4])
            if win_cond_hor:
                game_finish_output(PLAYER_CODE)
    check_out_space()


def game_fin_aftr_mark_plcd(x, y, player_mark):
    """Checks fro completed lines.
    Called after each turn
    """
    # game_finish_check upgraded
    # Was needed to refactor in case of speed and memory optimization
    for dg_cnt in range(5):
        if (x-dg_cnt in range(10)) and (y-dg_cnt in range(10)):
        # here s check for diag existance
            win_cond_diag = GAME_BOARD[x - dg_cnt][y - dg_cnt] == GAME_BOARD[x - dg_cnt + 1][y - dg_cnt + 1] == \
                            GAME_BOARD[x - dg_cnt + 2][y - dg_cnt + 2] == GAME_BOARD[x - dg_cnt + 3][y - dg_cnt + 3] == \
                            GAME_BOARD[x - dg_cnt + 4][y - dg_cnt + 4] == player_mark
            if win_cond_diag:
                game_finish_output(PLAYER_CODE)
    for hz_cnt in range(5):
        if x-hz_cnt in range(10):
            win_cond_horiz = GAME_BOARD[x - hz_cnt][y] == GAME_BOARD[x - hz_cnt + 1][y] == \
                             GAME_BOARD[x - hz_cnt + 2][y] == GAME_BOARD[x - hz_cnt + 3][y] ==\
                             GAME_BOARD[x - hz_cnt + 4][y] == player_mark
            if win_cond_horiz:
                game_finish_output(PLAYER_CODE)
    for vert_cnt in range(5):
        if y-vert_cnt in range(10):
            win_cond_vert = GAME_BOARD[x][y - vert_cnt] == GAME_BOARD[x][y - vert_cnt + 1] ==\
                            GAME_BOARD[x][y - vert_cnt + 2] == GAME_BOARD[x][y - vert_cnt + 3] ==\
                            GAME_BOARD[x][y - vert_cnt + 4] == player_mark
            if win_cond_vert:
                game_finish_output(PLAYER_CODE)


def estimate_cells():
    """Calculates the cells value for current board
    and returns the most with updating
    global GAME_BOARD variable
    """
    cur_mark = PLAYER_CODE
    CALC_BOARD = numpy.empty_like(GAME_BOARD)
    CALC_BOARD[:] = GAME_BOARD
    for m in range(10):
        for n in range(10):
            if CALC_BOARD[m][n] == 0:
                CALC_BOARD[m][n] = cur_mark
                game_finish_check()
                check_out_space()
    pass


def strategy():
    """:returns the most valuable cell
    coordinates to make a turn"""


def turn(x, y, player):
    """making operations threaded with each
    turn"""
    if player:
        GAME_BOARD[x][y] = 11111
        BOARD_VIEW[x][y] = 1
    else:
        GAME_BOARD[x][y] = 10101
        BOARD_VIEW[x][y] = 2
    global TURN_FLAG
    TURN_FLAG = not TURN_FLAG
    # passing the turn order


# so needed...
def logging(result='I WIN', *turn_data):
    """write down the game"""
    # players can cross over and replay

    pos: tuple[int, int]
    player: str
    mark: MARKS
    pos, player, mark = turn_data

    list_of_turns = set()

    def mark_roll(player, mark):
        """Initiate the set via information
        about which player owns first turn and
        his mark"""
        list_of_turns.add((player, mark))

    def record_turn(*coords):
        """coordinates of mark"""
        list_of_turns.add((coords))


def clear():
    """prepares screen for new output,
    for 3 major systems"""
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def update():
    clear()
    show_board()


def main():
    """The game itself"""
    # Greeting
    print("Welcome to 'REVERSE ZEROS - CROSSES', HERO!!!")

    # A draw, its information output
    global PLAYER_CODE
    PLAYER_CODE = choose_first()
    player_readable = "Computer" if PLAYER_CODE == 1 else "Human"
    print(f'Its {player_readable} time to go first!!!')
    show_board()

    while True:
        game_finish_check()
        show_board()


if __name__ == '__main__':
    main()
#    import pdb

#   pdb.set_trace()
