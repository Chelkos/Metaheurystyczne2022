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
        alg.repetitive_nearest_neighbour,
        alg._2_opt
    ]

    for algorithm in algorithms:
        print(utils.objective(algorithm(G)))

if __name__=='__main__':
    G = gen.generate_asymmetric(100, 1000)
    test_all(G)
