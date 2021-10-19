"""AI, numpy and game theory versus YOU"""
import sys
import time
from functools import singledispatch
from os import system, name
from random import choice

import numpy
import numpy as np

MARKS = {'X', 'O', '+', '-', '@', '$'}


# not important in case of usbility but this func is the essence of FP
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
BOARD_VIEW[1:, 0] = np.arange(10)

# for i in range(-1, 10):
#     BOARD_VIEW[0][i] = i

# masks
POSSIBLE_TURNS = np.ones((10, 10))

# will be integrated after algorythm
h_player_mark = '#'

# used to track 'turn owners'
TURN_FLAG: bool = False

PLAYER_CODE = 2
AI_CODE = 1


def choose_first():
    """Returns boolean value whether the player wins the game."""
    return choice((True, False))


def show_board():
    """Displays game progress"""
    print(BOARD_VIEW)


def check_out_space():
    """Waits until all fields are occupied"""
    # if set(GAME_BOARD) == {1, 2}:
    if not np.any(GAME_BOARD):
        game_finish_output('Draw')


def game_finish_output(win_code):
    if win_code == 'Draw':
        sys.exit('Draw, game board is empty')
    else:
        sys.exit('Player ' + win_code + ' wins!!!')


# unused in case of extra calculations
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


def game_fin_aftr_mark_plcd(x, y, player_mark, BOARD):
    """Checks fro completed lines.
    Called after each turn,
    on next turn calculation
    """
    # game_finish_check upgraded
    # Was needed to refactor in case of speed and memory optimization
    for dg_cnt in range(5, 10):
        if (x - dg_cnt in range(10)) and (y - dg_cnt in range(10)):
            # here s check for diag existance
            # and other are equalent
            # IMP!!!
            win_cond_diag = GAME_BOARD[x - dg_cnt][y - dg_cnt] == GAME_BOARD[x - dg_cnt + 1][y - dg_cnt + 1] == \
                            GAME_BOARD[x - dg_cnt + 2][y - dg_cnt + 2] == GAME_BOARD[x - dg_cnt + 3][y - dg_cnt + 3] == \
                            GAME_BOARD[x - dg_cnt + 4][y - dg_cnt + 4] != 0  # == player_mark
            if win_cond_diag:
                game_finish_output(player_mark)
    for hz_cnt in range(5):
        try:
            # if x - hz_cnt in range(10):
            win_cond_horiz = GAME_BOARD[x - hz_cnt][y] == GAME_BOARD[x - hz_cnt + 1][y] == \
                             GAME_BOARD[x - hz_cnt + 2][y] == GAME_BOARD[x - hz_cnt + 3][y] == \
                             GAME_BOARD[x - hz_cnt + 4][y] != 0  # == player_mark
            if win_cond_horiz:
                game_finish_output(player_mark)
        except IndexError:
            pass
    for vert_cnt in range(5):
        try:
            # if y - vert_cnt in range(10):
            win_cond_vert = GAME_BOARD[x][y - vert_cnt] == GAME_BOARD[x][y - vert_cnt + 1] == \
                            GAME_BOARD[x][y - vert_cnt + 2] == GAME_BOARD[x][y - vert_cnt + 3] == \
                            GAME_BOARD[x][y - vert_cnt + 4] != 0  # == player_mark
            if win_cond_vert:
                game_finish_output(player_mark)
        except IndexError:
            pass


def victory_produce(p_c):
    return game_finish_output(p_c)


def check_turn_outcome(x, y):
    CALC_BOARD = numpy.empty_like(GAME_BOARD)
    CALC_BOARD[:] = GAME_BOARD


# too big to make a tree
# def estimate_cells():
#     """Calculates the cells value for current board
#     and returns the most with updating
#     global GAME_BOARD variable
#     """
#     cur_mark = PLAYER_CODE
#     CALC_BOARD = numpy.empty_like(GAME_BOARD)
#     CALC_BOARD[:] = GAME_BOARD
#     for m in range(10):
#         for n in range(10):
#             if CALC_BOARD[m][n] == 0:
#                 CALC_BOARD[m][n] = cur_mark
#                 game_finish_check()
#                 check_out_space()
#     pass


# also need chunks composition strategy
# to make victory composition from separate areas

def strategy_turn_predict() -> tuple[int, int]:
    # lru cache for 2 of 4
    # index can be raised by optimization
    # so called 'pruning'
    """:returns the most valuable cell
    coordinates to make a turn
    based on next placements outcome
    used on board allmost filled"""
    pass


def strategy_line_completion() -> tuple[int, int]:
    """Coordinates based on which fields need to be
    marked to complete or block potential lines
    """

    pass


def turn(player):
    """making operations threaded with each
    turn"""

    def h_turn_inp():
        """Taking coordinates in turn from brave player"""
        print("Now its your turn!!!")
        coord_x = input("Enter your choice(row):")
        coord_y = input("Enter your choice(column):")
        ret_x = int(coord_x)
        ret_y = int(coord_y)
        return ret_x, ret_y if ret_y in range(10) and ret_x in range(10) and \
                               POSSIBLE_TURNS[ret_x][ret_y] else sys.exit('Learn the rules before to play.')

    def ai_move() -> tuple[int, int]:
        """Just a mock function without
        any algorithm except random numbers generating
        """
        pool = numpy.where(POSSIBLE_TURNS[:] == 1)
        pool_coord = list(zip(pool[0], pool[1]))
        while (pool_coord):
            rand_coord = choice(pool_coord)
            r, c = rand_coord
            print()

            def check_turn_outcome(x, y):
                calc_board = numpy.empty_like(GAME_BOARD)
                calc_board[:] = GAME_BOARD
                # try anothr solution on loose
                c_loose = game_fin_aftr_mark_plcd(x, y, calc_board, AI_CODE)
                return None if c_loose else x, y

            outcome = check_turn_outcome(r, c)
            if not check_turn_outcome(r, c):
                pool_coord -= rand_coord
            else:
                print('My turn was {} to {}'.format(r, c))
                return outcome

    if player == AI_CODE:
        x, y = ai_move()
    else:
        x, y = h_turn_inp()
    BOARD_VIEW[x + 1][y + 1] = player
    GAME_BOARD[x][y] = player
    time.sleep(2)
    v_c = game_fin_aftr_mark_plcd(x, y, player, GAME_BOARD)
    if v_c:
        game_finish_output(v_c)
    check_out_space()
    POSSIBLE_TURNS[x][y] = 0
    # passing the turn order
    global TURN_FLAG
    TURN_FLAG = not TURN_FLAG


# so needed... to improve my algorythm by
@singledispatch
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


# different handlers for typed input
# @logging.register(None)
# def logging():
#     pass


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
    # clear()  # not emtying...
    # print('\n' * 20)
    print(('   |' * 11 + '  \n') * 19, end='')
    print('   V' * 11)
    show_board()


def main():
    """The game itself"""
    # Greeting
    print("Welcome to 'REVERSE ZEROS - CROSSES', HERO!!!")

    # A draw, its information output
    global PLAYER_CODE
    global TURN_FLAG
    TURN_FLAG = choose_first()
    player_readable = "Computer" if TURN_FLAG else "Human"
    print(f'Its {player_readable}\'s time to go first!!!')
    show_board()

    while True:
        # mark = PLAYER_CODE if TURN_FLAG else AI_CODE
        # print(f'Its {player_readable}\'s turn.......')
        turn(AI_CODE) if TURN_FLAG else turn(PLAYER_CODE)
        update()

        # if TURN_FLAG:
        #     point = ai_move()
        #     turn(*point, AI_CODE)
        # else:
        #     point = h_turn_inp()
        #     turn(*point, PLAYER_CODE)
        # update()
        # game_fin_aftr_mark_plcd(*point, player_readable)


if __name__ == '__main__':
    main()
#    import pdb

#   pdb.set_trace()
