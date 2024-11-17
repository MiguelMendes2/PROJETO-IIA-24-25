from tictacchess import *
from utils import *
from jogos import *

def func_247(state, player):
    def other_player(player):
        return 'WHITE' if player == 'BLACK' else 'BLACK'

    def func_pawn_early_game_247(state, player):
        player_pieces = state.player_pieces(player)
        if state.n_jogadas < 8 and player_pieces in ['p', 'P']:
            return -250
        return 0

    def func_mobility_247(state, player):
        player_moves = 0
        opponent_moves = 0

        player_cells, player_pieces = state.player_used_cells(player)
        for piece, _ in zip(player_pieces, player_cells):
            moves = state.possible_moves(piece)
            player_moves += len(moves) * 2

        player_cells, player_pieces = state.player_used_cells(other_player(player))
        for piece, _ in zip(player_pieces, player_cells):
            moves = state.possible_moves(piece)
            opponent_moves += len(moves) * 2

        return (player_moves - opponent_moves) * 3

    def flexible_alignment_bonus_247(state, player):
        player_cells, _ = state.player_used_cells(player)
        alignments = 0

        # Contar possíveis alinhamentos a partir de diferentes combinações
        for group in combinations(player_cells, 3):
            if in_row(sorted(group)):
                alignments += 1

        return 200 * alignments  # Recompensa maior para mais ameaças simultâneas

    def is_threatening_247(state, player, move):
        # Pieces currently in play for the given player
        pieces = state.player_used_pieces(state.to_move)
        empty_cells = state.empty_cells(state)

        # Early game: if the player can place a new piece at the move location
        if len(pieces) < 4 and move in empty_cells:
            return 100 if state.to_move == player else -100

        # Check if the move aligns with the possible moves of existing pieces
        for piece in pieces:
            if move in state.possible_moves(piece):
                return 100 if state.to_move == player else -100

        # No threat found
        return 0

    def func_center_247(state, player):
        """Player places his pieces in the center"""
        player_cells, _ = state.player_used_cells(player)
        opponent_cells, _ = state.player_used_cells(other_player(player))
        center = [(1,1),(1,2),(2,1),(2,2)]

        player_control = sum(1 for cell in player_cells if cell in center)
        opponent_control = sum(1 for cell in opponent_cells if cell in center)
        return (player_control - opponent_control)

    def func_winner_247(state, player):
        winner = state.have_winner()
        if winner != None:
            return infinity if winner == player else -infinity
        score = 0
        # se não reconhece o final do jogo, verifica quem tem três em linha:
        almost_winner = state.n_in_row(3)
        if almost_winner == player:
            # Check if current state is blocking the row of the player
            missing_cell = row_blocked_247(state, 3, other_player(player), player)
            threat_score  = is_threatening_247(state, player, missing_cell)
            score = threat_score if threat_score != 0 else 1000
        elif almost_winner == other_player(player):
            # Check if current state is blocking the row of the other player
            missing_cell = row_blocked_247(state, 3, player, other_player(player))
            threat_score = is_threatening_247(state, player, missing_cell)
            score = threat_score if threat_score != 0 else -1000

        elif almost_winner == "BOTH":
            # Check if current state is blocking the row of the player
            opponent_missing  = row_blocked_247(state, 3, other_player(player), player)
            score += is_threatening_247(state, player, opponent_missing)
            if score == 0:
                # Check if current state is blocking the row of the other player
                missing_cell = row_blocked_247(state, 3, player, other_player(player))
                threat_score = is_threatening_247(state, player, missing_cell)
                score += threat_score if threat_score != 0 else -500

        return score - state.n_jogadas

    def row_blocked_247(state, n, player, other):
        "Return the player or players who have n-in-row (maybe Both), or None."
        #(play,board,jogadas,capturas,pawn_direction,piece)=self
        cells1,_ = state.player_used_cells(player)
        cells2,_ = state.player_used_cells(other)
        empty_cells = state.empty_cells(state)

        if len(cells2) >= n: # we check if a group of them is in_row, assume
            for group_cells2 in combinations(cells2, n):
                group_cells2 = list(group_cells2)
                for cell1 in cells1 + empty_cells:
                    group_cells2.append(cell1)
                    group_cells2 = sorted(group_cells2)
                    if in_row(group_cells2):
                        return cell1
                    group_cells2.remove(cell1)
        return None

    clone=copy.deepcopy(state)
    return func_winner_247(clone, player) + func_center_247(clone, player) + func_mobility_247(clone,player) + func_pawn_early_game_247(clone, player) + flexible_alignment_bonus_247(clone, player)