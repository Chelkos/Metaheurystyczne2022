import sys
import random
import math
import tsplib95 as tsp
import networkx as nx
import algorithms as alg

def load(file):
    problem = tsp.load(file)
    G = problem.get_graph()
    for n in G.nodes():
        G.has_edge(n,n) and G.remove_edge(n, n)
    return G

def objective(G):
    return G.size(weight='weight')

def generate(n):
    G = nx.complete_graph(n)
    G = nx.relabel_nodes(G, {i: i+1 for i in range(n)})
    nx.set_edge_attributes(G, 0, 'weight')

    coords = {'x': [], 'y': []}
    for i in range(n):
        coords['x'].append(random.randint(1, 4000))
        coords['y'].append(random.randint(1, 4000))

    for i in range(n):
        for j in range(i, n):
            if i != j:
                xd = coords['x'][i] - coords['x'][j]
                yd = coords['y'][i] - coords['y'][j]
                G[i+1][j+1]['weight'] = int(math.sqrt(xd**2 + yd**2) + 0.5)

    return G
      
if __name__=='__main__':
    G = generate(500)
    solution = alg.closest_neighbour(G)
    print(objective(solution))
