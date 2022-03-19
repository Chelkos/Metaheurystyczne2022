import math
import random
import networkx as nx

def generate_symmetric(n, k):
    G = nx.complete_graph(n)
    G = nx.relabel_nodes(G, {i: i+1 for i in range(n)})
    nx.set_edge_attributes(G, 0, 'weight')

    for i in range(n):
        for j in range(i+1, n):
            G[i+1][j+1]['weight'] = random.randint(1, k)

    return G

def generate_asymmetric(n, k):
    G = nx.complete_graph(n, nx.DiGraph())
    G = nx.relabel_nodes(G, {i: i+1 for i in range(n)})
    nx.set_edge_attributes(G, 0, 'weight')

    for i in range(n):
        for j in range(n):
            if i != j:
                G[i+1][j+1]['weight'] = random.randint(1, k)

    return G

def generate_euc2d(n, k):
    G = nx.complete_graph(n)
    G = nx.relabel_nodes(G, {i: i+1 for i in range(n)})
    nx.set_edge_attributes(G, 0, 'weight')

    coords = {'x': [], 'y': []}
    for i in range(n):
        coords['x'].append(random.randint(0, k))
        coords['y'].append(random.randint(0, k))

    for i in range(n):
        for j in range(i+1, n):
            xd = coords['x'][i] - coords['x'][j]
            yd = coords['y'][i] - coords['y'][j]
            G[i+1][j+1]['weight'] = int(math.sqrt(xd**2 + yd**2) + 0.5)

    return G
    