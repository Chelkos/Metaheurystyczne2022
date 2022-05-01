import networkx as nx
import math
import random 
import utils

def nearest_neighbour(Graphy, node=False):
    random.seed(30)
    G = Graphy.copy()
    solution = nx.DiGraph()
    node = node or random.choice(list(G.nodes()))
    first_node = node

    while len(G.nodes()) - 1:
        min = math.inf

        for u,v in G.edges(node):
            if G[u][v]['weight'] < min:
                min = G[u][v]['weight']
                next_node = v

        solution.add_edge(node, next_node, weight=min)
        G.remove_node(node)
        node = next_node
    
    solution.add_edge(node, first_node, weight=Graphy[node][first_node]['weight'])
    return solution
    
def repetitive_nearest_neighbour(G):
    min = math.inf

    for node in G.nodes():
        route = nearest_neighbour(G, node)
        weight = utils.objective(route)
        if weight < min:
            solution = route
            min = weight

    return solution

def k_random(G,k = 30):
    solution = nx.DiGraph()
    solution_weight = None

    for i in range(k):
        possible_solution = nx.DiGraph()
        graph = G.copy()
        random_node = random.choice(list(graph.nodes()))
        first_node = random_node
        for n in range(len(graph.nodes())-1):
            possible_solution.add_node(random_node)
            random_edge = random.choice(list(graph.edges(random_node)))
            (u, v) = random_edge
            edge_weight =  graph[u][v]['weight']
            possible_solution.add_node(v)
            possible_solution.add_edge(u,v,weight = edge_weight)
            graph.remove_node(u)
            random_node = v
        possible_solution.add_edge(random_node, first_node, weight=G[random_node][first_node]['weight'])
        if solution_weight is None or utils.objective(possible_solution) < solution_weight:
            solution = possible_solution
            solution_weight = utils.objective(possible_solution)

    return solution

def invert(G, route, i, j):
    nodes = list(route.nodes())
    inverted = nodes[:i] + nodes[i:j+1][::-1] + nodes[j+1:]

    new_route = nx.DiGraph()

    for n in range(len(inverted) - 1):
        new_route.add_edge(inverted[n], inverted[n+1], weight=G[inverted[n]][inverted[n+1]]['weight'])
    
    new_route.add_edge(inverted[0], inverted[len(G.nodes())-1], weight=G[inverted[0]][inverted[len(G.nodes())-1]]['weight'])

    return new_route

def swap(G, route, i, j):
    nodes = list(route.nodes())
    nodes[i], nodes[j] = nodes[j], nodes[i]

    new_route = nx.DiGraph()

    for n in range(len(nodes) - 1):
        new_route.add_edge(nodes[n], nodes[n+1], weight=G[nodes[n]][nodes[n+1]]['weight'])

    new_route.add_edge(nodes[0], nodes[len(G.nodes())-1], weight=G[nodes[0]][nodes[len(G.nodes())-1]]['weight'])
    return new_route
def insert(G, route, i, j):
    nodes = list(route.nodes())
    node = nodes.pop(i)
    nodes.insert(j, node)
    
    new_route = nx.DiGraph()

    for n in range(len(nodes) - 1):
        new_route.add_edge(nodes[n], nodes[n+1], weight=G[nodes[n]][nodes[n+1]]['weight'])

    new_route.add_edge(nodes[0], nodes[len(G.nodes())-1], weight=G[nodes[0]][nodes[len(G.nodes())-1]]['weight'])
    return new_route

def _2_opt(G):
    n = len(list(G.nodes()))
    solution = repetitive_nearest_neighbour(G)
    min_weight = utils.objective(solution)
    
    progress = True

    while progress == True:
        progress = False

        for i in range(n):
            if progress == True:
                break

            for j in range(i+1, n):
                route = invert(G, solution, i, j)
                weight = utils.objective(route)
            
                if weight < min_weight:
                    solution = route
                    min_weight = weight
                    progress = True
                    break
    return solution

def tabu_search(G, reps=100, size=15,type_a=invert,start_type=repetitive_nearest_neighbour):
    tabu = []
    current_solution = start_type(G)
    best_solution = current_solution
    n = len(G.nodes())
    it = 0

    while it < reps:
        best_neighbour = None
        for i in range(n):
            for j in range(i+1, n):
                if (i,j) not in tabu:
                    neighbour = type_a(G, current_solution, i, j)
                    weight = utils.objective(neighbour)
                    if best_neighbour == None or weight < best_weight:
                        best_neighbour = neighbour
                        best_weight = weight
                        x,y = (i,j)

        tabu.append((x,y))
        current_solution = best_neighbour

        if len(tabu) > size:
            tabu.pop(0)

        if best_weight < utils.objective(best_solution):
            best_solution = current_solution
            it = 0
       
        it += 1

    return best_solution
