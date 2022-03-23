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
    inversed = route.copy()

    if i != 0:
        inversed.remove_edge(nodes[i-1], nodes[i])
        inversed.add_edge(nodes[i-1], nodes[j], weight=G[nodes[i-1]][nodes[j]]['weight'])

    if j != len(nodes)-1:
        inversed.remove_edge(nodes[j], nodes[j+1])
        inversed.add_edge(nodes[i], nodes[j+1], weight=G[nodes[i]][nodes[j+1]]['weight'])

    for n in range(i, j):
        inversed.remove_edge(nodes[n], nodes[n+1])
        inversed.add_edge(nodes[n+1], nodes[n], weight=G[nodes[n+1]][nodes[n]]['weight'])

    return inversed

def inverse(original,G,i,j):
    helper = G.copy()
    c_graph = G.copy()
    c_size = len(c_graph.nodes())
    node_j = list(helper.nodes())[j]
    node_i = list(helper.nodes())[i]
    if i == 0:
        node_ip = None
    else:
        node_ip = list(helper.nodes())[i-1]
    if j==c_size-1:
        node_jn = None
    else:
        node_jn = list(helper.nodes())[j+1]
    if node_ip is not None:
        c_graph.remove_edge(node_ip,node_i)
    if node_jn is not None:    
        c_graph.remove_edge(node_jn,node_j)
    for k in range(i,j):
        if k>c_size:
            k=0
        new_weight = original[list(helper.nodes())[k+1]][list(helper.nodes())[k]]['weight']
        c_graph.remove_edge(list(helper.nodes())[k],list(helper.nodes())[k+1])
        c_graph.add_edge(list(helper.nodes())[k+1],list(helper.nodes())[k],weight=new_weight)
    if node_ip is not None:
        new_weight_p = original[node_ip][node_j]['weight']
        c_graph.add_edge(node_ip,node_j,weight=new_weight_p)
    if node_jn is not None:
        new_weight_k = original[node_i][node_jn]['weight']
        c_graph.add_edge(node_i,node_jn,weight=new_weight_k)
    return c_graph


def opt_2(G):
    help_graph = G.copy()
    graph_size = len(list(help_graph.nodes()))
    first_solution = nearest_neighbour(help_graph)
    optimal_solution = first_solution
    current_lowest = utils.objective(first_solution)
    print(current_lowest)
    for i in range(0,graph_size):
        for k in range(i+1,graph_size):
            
            current_solution = inverse(G,first_solution,i,k)
            print(utils.objective(current_solution)," ",current_lowest)
            if utils.objective(current_solution)< current_lowest:
                current_lowest = utils.objective(current_solution)
                optimal_solution = current_solution

    return optimal_solution
