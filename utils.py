import networkx as nx
import matplotlib.pyplot as plt

def objective(G):
    return G.size(weight='weight')

def draw(G):
    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()
