from logging import exception
import networkx as nx
import math
import random 


def objective(G):
    return G.size(weight='weight')

def nearest_neighbour(G, node=False):
    solution = nx.empty_graph()
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
        H = G.copy()
        route = nearest_neighbour(H, node)
        weight = objective(route)
        if weight < min:
            solution = route
            min = weight

    return solution


def k_random(k,G):
    solution = nx.empty_graph()
    solution_weight = None
    for i in range(k):
        possible_solution = nx.empty_graph()
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
            
        if solution_weight is None or objective(possible_solution)<solution_weight:
            
            solution =possible_solution
            solution_weight = objective(possible_solution)
    
    
    return solution