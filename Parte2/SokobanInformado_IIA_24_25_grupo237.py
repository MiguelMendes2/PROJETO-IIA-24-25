
def h_util(self, node):
    """Para cada objetivo (lugar de armazenamento), calcula a distância de Manhattan à caixa mais próxima
    que ainda não foi alocada, ignorando a existência de paredes e/ou obstáculos, e aloca essa caixa ao objetivo.
    O valor da heurística é a soma todas estas distâncias + a distância entre o sokoban e a caixa mais longínqua
    que ainda não está arrumada. Se estamos num estado final, devolve 0."""
    clone = copy.deepcopy(node.state)

    # Satisfaz objectivo?
    if self.goal_test(node.state):
        return 0

    return self.objective_distance(clone) + self.sokoban_to_box_distance(clone)

def beam_search_plus_count(problem, W, f):
    """Beam Search: search the nodes with the best W scores in each depth.
    Return the solution and how many nodes were expanded."""
    f = memoize(f, 'f')
    node = Node(problem.initial)

    if problem.goal_test(node.state):
        return node, 0

    frontier = PriorityQueue(min, f)
    frontier.append(node)
    explored = set()
    while frontier:
        next_frontier = PriorityQueue(min, f)
        temp = W
        while frontier:
            node = frontier.pop()
            if problem.goal_test(node.state):
                return node, len(explored)

            explored.add(node.state)

            for child in node.expand(problem):
                if child.state not in explored:
                    if child in frontier:
                        other = frontier[child]
                        if f(child) < f(other):
                            del frontier[other]
                            next_frontier.append(child)
                    elif child in next_frontier:
                        other = next_frontier[child]
                        if f(child) < f(other):
                            del next_frontier[other]
                            next_frontier.append(child)
                    else:
                        next_frontier.append(child)

        while next_frontier and temp > 0:
            frontier.append(next_frontier.pop())
            temp -= 1
    return None, len(explored)

def IW_beam_search(problem, h):
    """IW_beam_search (Iterative Widening Beam Search) começa com beam width W=1 e aumenta W iterativamente até
    se obter uma solução. Devolve a solução, o W com que se encontrou a solução, e o número total (acumulado desde W=1)
    de nós expandidos. Assume-se que existe uma solução."""
    W = 1
    total_expanded_nodes = 0

    while True:
        solution, nr_expanded_nodes = beam_search_plus_count(problem, W, lambda n: n.path_cost + h(n))
        total_expanded_nodes += nr_expanded_nodes

        if solution is not None:
            return solution, W, total_expanded_nodes

        W += 1

