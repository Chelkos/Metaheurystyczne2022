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

def open_file(title,sym_type,size,alg_name):
    file_name = title+"_"+sym_type+"_"+str(size)+"_"+alg_name+".txt"
    file = open(file_name,"a")
    return file

def open_file_no_size(title,sym_type,alg_name):
    file_name = title+"_"+sym_type+"_"+alg_name+".txt"
    file = open(file_name,"a")
    return file

def write_to_file(file,x,y):
    file.write("("+str(x)+", "+str(y)+")\n")

def test_all(G):
    algorithms = [
        alg.k_random,
        alg.nearest_neighbour, 
        alg.repetitive_nearest_neighbour,
        alg._2_opt
    ]

    for algorithm in algorithms:
        print(utils.objective(algorithm(G)))

if __name__=='__main__':
    G = gen.generate_symmetric(10, 1000)
    alg.generate_neighbourhood(G)
