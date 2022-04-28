from tracemalloc import start
import tsplib95 as tsp
import algorithms as alg
import generators as gen
import random
import utils
import networkx as nx
import time
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

def test_alg_type():
    algs = [
        alg.invert,
        alg.swap,
        alg.insert,
    ]
    
    
    for a in algs:
        if a == alg.invert:
            n = "invert"
        f_w = open(str('tabu_'+n+'.txt'),"a")
        for size in [10,20,50]:
            curr_graph = gen.generate_symmetric(size,1000)
            sol = alg.tabu_search(curr_graph,50)
            write_to_file(f_w,size,utils.objective(sol))



def test_all(G):
    algorithms = [
        alg.k_random,
        alg.nearest_neighbour, 
        alg.repetitive_nearest_neighbour,
        alg._2_opt,
        alg.tabu_search
    ]

    for algorithm in algorithms:
        print(utils.objective(algorithm(G)))

if __name__=='__main__':
    random.seed(150)
    #G = gen.generate_asymmetric(30, 1000)
    #test_all(G)
    test_alg_type()
