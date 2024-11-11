from jogos import *
from tictacchess import *

def func_247(state, player):
    """A player that chooses a legal move at random."""
    clone=copy.deepcopy(state)
    return func_winner(clone, player) + func_lines(clone, player)

def func_lines(state, player):
    pieces = state.player_used_cells(player)[0]
    other_pieces = state.player_used_cells(state.other())[0]
    num_pieces = len(pieces)
    center = [(1,1),(1,2),(2,1),(2,2)]
    if num_pieces == 1:
        return 1 if pieces[0] in center else -1
    elif num_pieces == 2:
        return 2 if (in_row(pieces) and all(not in_row([pieces[0], p]) for p in other_pieces)) else -2
    return 0

def func_winner(state, player):
    winner = state.have_winner()
    if winner != None:
        return infinity if winner==player else -infinity
    # se não reconhece o final do jogo, verifica quem tem três em linha:
    almost_winner = state.n_in_row(3)
    if almost_winner == None or almost_winner == 'BOTH':
        return 5
    return 10 if almost_winner==player else -10