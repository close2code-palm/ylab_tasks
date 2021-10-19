import numpy

from task_2.main import game_finish_output, GAME_BOARD, AI_CODE


def game_fin_aftr_mark_plcd(x, y, board=GAME_BOARD, *player_mark):
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
            win_cond_diag = board[x - dg_cnt][y - dg_cnt] == board[x - dg_cnt + 1][y - dg_cnt + 1] == \
                            board[x - dg_cnt + 2][y - dg_cnt + 2] == board[x - dg_cnt + 3][y - dg_cnt + 3] == \
                            board[x - dg_cnt + 4][y - dg_cnt + 4] != 0  # == player_mark
            if win_cond_diag:
                return player_mark
    for hz_cnt in range(5):
        try:
            # if x - hz_cnt in range(10):
            win_cond_horiz = board[x - hz_cnt][y] == board[x - hz_cnt + 1][y] == \
                             board[x - hz_cnt + 2][y] == board[x - hz_cnt + 3][y] == \
                             board[x - hz_cnt + 4][y] != 0  # == player_mark
            if win_cond_horiz:
                return player_mark
        except IndexError:
            pass
    for vert_cnt in range(5):
        try:
            # if y - vert_cnt in range(10):
            win_cond_vert = board[x][y - vert_cnt] == board[x][y - vert_cnt + 1] == \
                            board[x][y - vert_cnt + 2] == board[x][y - vert_cnt + 3] == \
                            board[x][y - vert_cnt + 4] != 0  # == player_mark
            if win_cond_vert:
                return player_mark
        except IndexError:
            pass



ESTIMATED_BOARD = numpy.zeros((10,10))

def estimation_str(x, y):

    # estimation should depend on
    # log or/and on combinations which could be gotten with it

    def inc_if_ex(x,y, board):
        if board[x][y]:
            board[x][y] += 1

    ESTIMATED_BOARD[x,y] += 16

    for i in range(-4,5):
        inc_if_ex(ESTIMATED_BOARD[x + i][y])
        inc_if_ex(ESTIMATED_BOARD[x + i][y + i])
        inc_if_ex(ESTIMATED_BOARD[x][y + i])
