import tsplib95 as tsp
import algorithms as alg
import generators as gen
import random
import utils
import networkx as nx
import time
import genetic as gene

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
    for size in [10,20,30,40,50,60,70,80,90,100]:
        curr_graph = gen.generate_asymmetric(size,1000)
        for a in algs:
            if a == alg.invert:
                n = "invert"
            elif a==alg.insert:
                n = "insert"
            elif a==alg.swap:
                n = "swap"
            
            f_w = open(str('asym_tabu_'+n+'.txt'),"a")
            sol = alg.tabu_search(curr_graph,type_a=a)
            write_to_file(f_w,size,utils.objective(sol))

def test_start():
    algs = [
        alg.nearest_neighbour,
        alg.repetitive_nearest_neighbour,
        alg.k_random,
        alg._2_opt
    ]
    for size in [10,20,30,40,50,60,70,80,90,100]:
        curr_graph = gen.generate_symmetric(size,1000)
        for a in algs:
            if a == alg.nearest_neighbour:
                n = "nearest"
            elif a==alg.repetitive_nearest_neighbour:
                n = "repetitive"
            elif a==alg.k_random:
                n = "random"
            elif a==alg._2_opt:
                n = "opt"
            f_w = open(str('tabu_'+n+'.txt'),"a")
            sol = alg.tabu_search(curr_graph,start_type=a)
            write_to_file(f_w,size,utils.objective(sol))


def test_tabu_size():
    starter = alg.nearest_neighbour
    operation = alg.invert
    for size in [20,50,100]:
        curr_graph = gen.generate_symmetric(size,1000)
        f_w = open(str('tabu_list_size_'+str(size)+'.txt'),'a')
        for tabu_size in [1,3,6,12,25,50,100]:
            sol = alg.tabu_search(curr_graph,start_type=starter,size=tabu_size)
            write_to_file(f_w,tabu_size,utils.objective(sol))


def test_tabu_graph():
    starter = alg.nearest_neighbour
    operation = alg.invert
    f_s = open(str('astabu_graph_test_solution.txt'),'a')
    f_t = open(str('astabu_graph_test_time.txt'),'a')

    f_s2 = open(str('as2opt_graph_test_solution.txt'),'a')
    f_t2 = open(str('as2opt_graph_test_time.txt'),'a')

    f_s3 = open(str('asrnn_graph_test_solution.txt'),'a')
    f_t3 = open(str('asrnn_graph_test_time.txt'),'a')

    f_s4 = open(str('asr_graph_test_solution.txt'),'a')
    f_t4 = open(str('asr_graph_test_time.txt'),'a')

    f_s5 = open(str('ask_graph_test_solution.txt'),'a')
    f_t5 = open(str('ask_graph_test_time.txt'),'a')
    for size in [10,20,30,40,50,60,70,80,90,100]:
       
        curr_graph = gen.generate_asymmetric(size,1000)
        start = time.time()       
        sol = alg.tabu_search(curr_graph,start_type=starter,size=12,type_a=operation) 
        t = time.time()-start
        write_to_file(f_s,size,utils.objective(sol))
        write_to_file(f_t,size,t)

        start = time.time()       
        sol = alg._2_opt(curr_graph) 
        t = time.time()-start
        write_to_file(f_s2,size,utils.objective(sol))
        write_to_file(f_t2,size,t)

        start = time.time()       
        sol = alg.repetitive_nearest_neighbour(curr_graph)
        t = time.time()-start
        write_to_file(f_s3,size,utils.objective(sol))
        write_to_file(f_t3,size,t)

        start = time.time()       
        sol = alg.nearest_neighbour(curr_graph)
        t = time.time()-start
        write_to_file(f_s4,size,utils.objective(sol))
        write_to_file(f_t4,size,t)

        start = time.time()       
        sol = alg.k_random(curr_graph, 100) 
        t = time.time()-start
        write_to_file(f_s5,size,utils.objective(sol))
        write_to_file(f_t5,size,t)

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


def test_genetic(G):
    return

if __name__=='__main__':
    random.seed(170)
    G = gen.generate_symmetric(20,1000)
    #sol = alg.repetitive_nearest_neighbour(G)
    #print(utils.objective(sol))
    #test_alg_type()
    #test_start()
    #test_tabu_graph()
    #test_tabu_size()
    print(utils.objective(alg.repetitive_nearest_neighbour(G)))
    sol = alg.tabu_search(G, 100, 15, alg.invert, alg.nearest_neighbour)
    print(utils.objective(sol))
 
    sol = gene.genetic(G,120)
    print(utils.objective(sol))