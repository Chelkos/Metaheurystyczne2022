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
