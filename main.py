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
        elif a==alg.insert:
            n = "insert"
        elif a==alg.swap:
            n = "swap"
        f_w = open(str('tabu_'+n+'.txt'),"w")
        for size in [10,20,30,40]:
            curr_graph = gen.generate_symmetric(size,1000)
            sol = alg.tabu_search(curr_graph,type_a=a)
            write_to_file(f_w,size,utils.objective(sol))

def test_start():
    algs = [
        alg.nearest_neighbour,
        alg.repetitive_nearest_neighbour,
        alg.k_random,
        alg._2_opt
    ]
    for a in algs:
        if a == alg.nearest_neighbour:
            n = "nearest"
        elif a==alg.repetitive_nearest_neighbour:
            n = "repetitive"
        elif a==alg.k_random:
            n = "random"
        elif a==alg._2_opt:
            n = "opt"
        f_w = open(str('tabu_'+n+'.txt'),"w")
        for size in [10,20,30,40]:
            curr_graph = gen.generate_symmetric(size,1000)
            sol = alg.tabu_search(curr_graph,start_type=a)
            write_to_file(f_w,size,utils.objective(sol))


def test_tabu_size():
    starter = alg.nearest_neighbour
    operation = alg.invert
    for size in [10,20,50,75]:
        f_w = open(str('tabu_list_size_'+size+'.txt'),'w')
        for tabu_size in [2,5,7,11,23,41,100,200]:
            curr_graph = gen.generate_symmetric(size,1000)
            sol = alg.tabu_search(curr_graph,start_type=starter,size=tabu_size)
            write_to_file(f_w,tabu_size,utils.objective(sol))


def test_tabu_graph():
    starter = alg.nearest_neighbour
    operation = alg.invert
    f_s = open(str('tabu_graph_test_solution.txt'),'w')
    f_t = open(str('tabu_graph_test_time.txt'),'w')
    for size in [10,20,50,75,100]:
       
        curr_graph = gen.generate_symmetric(size,1000)
        start = time.time()       
        sol = alg.tabu_search(curr_graph,start_type=starter,size=7,type_a=operation) #dalem rozmiar tabu listy 7, ale jak w testach wyjdzie jakis inny optymalny to mozna zmienic
        t = time.time()-start
        write_to_file(f_s,size,utils.objective(sol))
        write_to_file(f_t,size,t)

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
    test_start()
