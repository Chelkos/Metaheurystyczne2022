import sys
import random
import tsplib95 as tsp
import algorithms as alg
import generators as gen
import utils

def load(file):
    problem = tsp.load(file)
    G = problem.get_graph()
    for n in G.nodes():
        G.has_edge(n,n) and G.remove_edge(n, n)
    return G
      
def test_all(G):
    algorithms = [
        alg.nearest_neighbour, 
        alg.repetitive_nearest_neighbour
    ]

    for algorithm in algorithms:
        H = G.copy()
        print(alg.objective(algorithm(H)))

if __name__=='__main__':
    random.seed(10)
    G = gen.generate_symmetric(5, 1000)
    route = alg.repetitive_nearest_neighbour(G)
    utils.draw(route)
    route = alg.invert(G, route, 1, 3)
    utils.draw(route)
