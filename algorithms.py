import networkx as nx
import random

def nearest_neighbour(G):
    node = random.choice(list(G.nodes()))
    solution = nx.empty_graph()
    solution.add_node(node)

    while len(G.nodes()) - 1:
        min = float('inf')
        nextNode = 0

        for u,v in G.edges(node):
            if G[u][v]['weight'] < min:
                min = G[u][v]['weight']
                nextNode = v

        solution.add_node(nextNode)
        solution.add_edge(node, nextNode, weight=min)
        G.remove_node(node)
        node = nextNode
    
    return solution
    