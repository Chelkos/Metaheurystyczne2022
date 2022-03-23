import networkx as nx
import math
import random 
import utils

def nearest_neighbour(Graphy, node=False):
    G = Graphy.copy()
    solution = nx.DiGraph()
    node = node or random.choice(list(G.nodes()))

    while len(G.nodes()) - 1:
        min = math.inf

        for u,v in G.edges(node):
            if G[u][v]['weight'] < min:
                min = G[u][v]['weight']
                next_node = v

        solution.add_edge(node, next_node, weight=min)
        G.remove_node(node)
        node = next_node
    
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

def k_random(k,G):
    solution = nx.DiGraph()
    solution_weight = None

    for i in range(k):
        possible_solution = nx.DiGraph()
        graph = G.copy()
        random_node = random.choice(list(graph.nodes()))
        
        for n in range(len(graph.nodes())-1):
            possible_solution.add_node(random_node)
            random_edge = random.choice(list(graph.edges(random_node)))
            (u, v) = random_edge
            edge_weight =  graph[u][v]['weight']
            possible_solution.add_node(v)
            possible_solution.add_edge(u,v,weight = edge_weight)
            graph.remove_node(u)
            random_node = v
            
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
