import networkx as nx
import math
import random 
import utils
tabu = []
bestest_solution = nx.Graph()
def nearest_neighbour(Graphy, node=False):
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



def generate_neighbourhood(G):
    n = len(list(G.nodes()))
    algs = [invert]
    neighbours = []
    first_solution = nearest_neighbour(G)
    for i in range(n):
        for j in range(i+1,n):
            curr_rep = invert(G,first_solution,i,j)
            curr_weight = utils.objective(curr_rep)
            neighbours.append((curr_rep,curr_weight))
    neighbours.sort(key=lambda i:i[1],reverse=False)
    for pair in neighbours:
        if pair[1] not in tabu:
            tabu.append(pair[1])
            if pair[2] < utils.objective(bestest_solution):
                bestest_solution = pair[1]
    print(neighbours)
