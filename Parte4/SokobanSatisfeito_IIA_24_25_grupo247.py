# Nossas funcoes
def csp_possivel_solucao(caixas, goals_alcancaveis):
    variables = list(caixas)
    domains = {var: goals_alcancaveis[var] for var in variables}
    neighbors = {var: [var2 for var2 in variables if var != var2 and set(goals_alcancaveis[var]).intersection(goals_alcancaveis[var2]) and goals_alcancaveis[var2]] for var in variables}
    for var in variables:
        if neighbors[var] == []:
            neighbors.pop(var)
    def constraints(var1, a, var2, b):
        return a != b

    return CSP(variables, domains, neighbors, constraints)

def csp_find_alcancaveis_1goal(s, goal):
    caixas = s.initial['caixas']
    variables = list(s.navegaveis)
    domains = {var: [0, 1] for var in variables}
    neighbors = {var1: [var2 for var2 in variables if var1 != var2 and eh_vizinho(var1, var2, s, caixas)] for var1 in variables}


    def constraints(var1, a, var2, b):
        if var2 not in neighbors[var1]:
            return True
        if a == 1 and b == 0:
            return False
        if b == 1 and a == 0:
            return False
        return True

    return CSP(variables, domains, neighbors, constraints)

def eh_vizinho(celula1, celula2, s, caixas):
    diff_linha = celula2[0] - celula1[0]
    diff_coluna = celula2[1] - celula1[1]
    deltas = diff_linha, diff_coluna

    if s.possible(s.initial['sokoban'], caixas, deltas) and (abs(diff_linha) + abs(diff_coluna) == 1):
        return True

    return False
    
def find_alcancaveis_all_goals(s):
    sorted_goals = sorted(list(s.goal))
    result_alcancaveis = {}
    
    for goal in sorted_goals:
        csp_sokoban2 = csp_find_alcancaveis_1goal(s, goal)
        r = backtracking_search(csp_sokoban2, order_domain_values=number_ascending_order, inference=forward_checking)
        if r is not None:
            for cell, reachable in r.items():
                if cell not in result_alcancaveis:
                    result_alcancaveis[cell] = []
                if reachable == 1:
                    result_alcancaveis[cell].append(goal)

    for cell in s.navegaveis:
        if cell not in result_alcancaveis:
            result_alcancaveis[cell] = []

    return result_alcancaveis
