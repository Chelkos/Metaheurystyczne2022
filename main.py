import sys
import tsplib95 as tsp
import algorithms as alg
import generators as gen

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
    G = gen.generate_asymmetric(5, 4000)
    alg.opt_2(G)
    #test_all(G)
