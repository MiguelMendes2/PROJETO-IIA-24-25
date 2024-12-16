# Nossas funcoes
from sokoban_aval4 import *
from csp_v3 import *

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
    def handle_neighbors(var1, var2):
        if (var1 not in s.navegaveis or var2 not in s.navegaveis):
            return False
        if abs(var1[0] - var2[0]) + abs(var1[1] - var2[1]) != 1:
            return False
        
        x1,y1 = var1
        x2,y2 = var2
        
        x0 = x1 + (x1-x2)
        y0 = y1 + (y1-y2)
        
        return (x0,y0) in s.navegaveis

    variables = s.navegaveis 
    domains = {var: [1] if var == goal else ([0] if s.its_a_trap(var) else [0, 1]) for var in variables}
    neighbors = {
        var1: [var2 for var2 in variables if var1 != var2 and handle_neighbors(var1, var2)]
        for var1 in variables
    }
    
    def constraints(var1, a, var2, b):
        return not (a == 0 and b == 1)

    return CSP(variables, domains, neighbors, constraints)

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

# Funcoes dadas
def possivel_solucao(caixas,goals_alcancaveis):
    csp_sokoban1 = csp_possivel_solucao(caixas,goals_alcancaveis) # <--- a vossa função csp_possivel_solucao 
    r = backtracking_search(csp_sokoban1, inference = forward_checking)
    return r
    
def find_alcancaveis_1goal(s,goal):
    csp_sokoban2 = csp_find_alcancaveis_1goal(s,goal) # <--- a vossa função csp_find_alcancaveis_1goal 
    r = backtracking_search(csp_sokoban2, order_domain_values = number_ascending_order, inference = forward_checking)    
    return {} if r == None else r
