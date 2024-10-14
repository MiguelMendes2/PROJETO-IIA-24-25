from searchPlus import *
from copy import deepcopy

linha1= "  ##### \n"
linha2= "###...# \n"
linha3= "#o@$..# \n"
linha4= "###.$o# \n"
linha5= "#o##..# \n"
linha6= "#.#...##\n"
linha7= "#$.....#\n"
linha8= "#......#\n"
linha9= "########\n"
mundoStandard=linha1+linha2+linha3+linha4+linha5+linha6+linha7+linha8+linha9

class SokobanState(object):

    def __init__(self, sokoban, boxes):
        self.sokoban = tuple(sokoban)
        self.boxes = set(boxes)

    def __eq__(self, value: object) -> bool:
        return (self.sokoban == value.sokoban and
                self.boxes == value.boxes)


class Sokoban(Problem):

    directions = {
            'N': (-1, 0),  # Norte (acima)
            'W': (0, -1),  # Oeste (esquerda)
            'E': (0, 1),   # Leste (direita)
            'S': (1, 0),   # Sul (abaixo)
        }

    def __init__(self, situacaoInicial=mundoStandard):
        """Construtor de Sokoban"""
        sokoban, boxes, goals, corners = None, set(), set(), set()
        self.map = situacaoInicial.split('\n')[:-1]
        for i, line in enumerate(self.map):
            for j, char in enumerate(line):
                if char in "@+":
                    sokoban = (i, j)
                if char in "$*":
                    boxes.add((i, j))
                if char in "+*o":
                    goals.add((i, j))
                if char in ".@" and self.is_corner(i, j):
                    corners.add((i, j))
        self.corners = corners
        self.initial = SokobanState(sokoban, boxes)
        self.goals = set(goals)

    def is_corner(self, i, j):
        """Identifica as cantos"""
        if self.map[i - 1][j] == "#" and self.map[i][j - 1] == "#": # Canto superior esquerdo
            return True
        if self.map[i - 1][j] == "#" and self.map[i][j + 1] == "#": # Canto superior direito
            return True
        if self.map[i + 1][j] == "#" and self.map[i][j - 1] == "#": # Canto inferior esquerdo
            return True
        if self.map[i + 1][j] == "#" and self.map[i][j + 1] == "#": # Canto inferior direito
            return True
        return False

    def movimento_valido(self, state, x, y, dx, dy):
        """Verifica se o movimento na direção dx, dy é válido"""
        mapa = self.map
        comp = len(mapa)
        lag = len(mapa[0])

        # Posição para onde o Sokoban deseja ir
        new_x, new_y = x + dx, y + dy

        # Se a nova posição for navegável, o movimento é válido
        if mapa[new_x][new_y] != "#" and (new_x, new_y) not in state.boxes:
            return True

        # Se a nova posição contiver uma caixa, verifica se ela pode ser empurrada
        if (new_x, new_y) in state.boxes:
            proximo_x, proximo_y = new_x + dx, new_y + dy

            # Verifica se a posição seguinte é válida
            if proximo_x < 0 or proximo_x >= comp or proximo_y < 0 or proximo_y >= lag:
                return False

            # Verifica se a posição seguinte é uma caixa
            if (proximo_x, proximo_y) in state.boxes:
                return False

            proximo_destino = mapa[proximo_x][proximo_y]
            # A caixa pode ser empurrada se a próxima posição for navegável ou um objetivo
            if (proximo_x, proximo_y) in self.goals or (proximo_destino != "#" and (proximo_x, proximo_y) not in self.corners):
                return True

        # Qualquer outra situação torna o movimento inválido
        return False

    def actions(self, state):
        """Retorna uma lista de ações possíveis (N, S, W, E) para o Sokoban"""
        x, y = state.sokoban
        actions = []

        for direcao, (dx, dy) in self.directions.items():
            if self.movimento_valido(state, x, y, dx, dy):
                actions.append(direcao)
        return actions

    def result(self, state, action):
        """Devolve o estado que resulta de executar action em state"""
        nstate = SokobanState(deepcopy(state.sokoban), deepcopy(state.boxes))
        ni, nj = nstate.sokoban
        dx, dy = self.directions[action]
        nstate.sokoban = (ni + dx, nj + dy)

        if nstate.sokoban in nstate.boxes:
            nni, nnj = nstate.sokoban
            nstate.boxes.remove(nstate.sokoban)
            nstate.boxes.add((nni + dx, nnj + dy))
        return nstate

    def goal_test(self, state):
        """Verifica se state é um estado final"""
        return state.boxes == self.goals

    def executa(self, state, actions):
        """Partindo de state, executa a sequência (lista) de acções (em actions) e devolve o último estado"""
        nstate = SokobanState(deepcopy(state.sokoban), deepcopy(state.boxes))
        for a in actions:
            nstate = self.result(nstate, a)
        return nstate

    def display(self, state):
        """Devolve a grelha em modo txt"""
        map = ""
        for i, linha in enumerate(self.map):
            for j, celula in enumerate(linha):
                if (i, j) == state.sokoban:
                    map += "+" if (i, j) in self.goals else "@"
                elif (i, j) in state.boxes:
                    map +=  "*" if (i, j) in self.goals else "$"
                elif (i, j) in self.goals:
                    map += "o"
                elif celula in "# ":
                    map += celula
                else:
                    map += "."
            map += '\n'
        return map

    def __eq__(self, value: object) -> bool:
        return super().__eq__(value)