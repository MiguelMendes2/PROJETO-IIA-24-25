from csp_v3 import *

def csp_possivel_solucao(s):
    for i in range(0, len(s.boxes)):
        if s.boxes[i] not in s.goal:
            return False
    return True

def csp_find_alcancaveis_1goal(s, goal):
    alcancaveis = set()
    alcancaveis.add(goal)
    for i in range(0, len(s.boxes)):
        if s.boxes[i] == goal:
            for j in range(0, len(s.boxes)):
                if i != j:
                    if (s.boxes[j][0] == s.boxes[i][0] and abs(s.boxes[j][1] - s.boxes[i][1]) == 1) or (s.boxes[j][1] == s.boxes[i][1] and abs(s.boxes[j][0] - s.boxes[i][0]) == 1):
                        alcancaveis.add(s.boxes[j])
    return alcancaveis


def find_alcancaveis_all_goals(s):
    sorted_goals = sorted(list(s.goal))
    result_alcancaveis = {}
    for goal in sorted_goals:
        result_alcancaveis[goal] = csp_find_alcancaveis_1goal(s, goal)
    return result_alcancaveis
