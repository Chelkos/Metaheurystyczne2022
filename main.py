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
    f_s = open(str('tabu_graph_test_solution.txt'),'a')
    f_t = open(str('tabu_graph_test_time.txt'),'a')

    f_s2 = open(str('2opt_graph_test_solution.txt'),'a')
    f_t2 = open(str('2opt_graph_test_time.txt'),'a')

    f_s3 = open(str('rnn_graph_test_solution.txt'),'a')
    f_t3 = open(str('rnn_graph_test_time.txt'),'a')

    f_s4 = open(str('r_graph_test_solution.txt'),'a')
    f_t4 = open(str('r_graph_test_time.txt'),'a')


    f_s5 = open(str('gene_graph_test_solution.txt'),'a')
    f_t5 = open(str('gene_graph_test_time.txt'),'a')
    for size in [10,20,30,40,50,60,70,80,90,100]:
       
        curr_graph = gen.generate_symmetric(size,1000)
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
        sol = gene.genetic(curr_graph)
        t = time.time()-start
        write_to_file(f_s5,size,utils.objective(sol))
        write_to_file(f_t5,size,t)

def test_all(G):
    algorithms = [
        alg.k_random,
        alg.nearest_neighbour, 
        alg.repetitive_nearest_neighbour,
        alg._2_opt,
        alg.tabu_search,
        gene.genetic
    ]

    for algorithm in algorithms:
        print(utils.objective(algorithm(G)))





def test_genetic():
    sizes = [20,30,50]
    graphs = ['bayg29.tsp','bays29.tsp'] 
    pop_size = [10,50,100,200,300,400,500,1000]
    reps = [100,200,400,800,1000]
    elite_size = [0,5,10,20,40,80]
    mutate_chance = [0,5,10,20,40,60,100]
    algs = [alg.nearest_neighbour,alg.repetitive_nearest_neighbour,alg._2_opt,alg.tabu_search]
    for size in sizes:
        G = gen.generate_symmetric(size,1000)
        base_name = ""+str(size)+"_"
        r_f_time = base_name+"_reps_time.txt"
        r_f_weight = base_name+"_reps_weight.txt"
        f_t = open(r_f_time,'a')
        f_w = open(r_f_weight,'a')
        p_f_time = base_name+"_pop_time.txt"
        p_f_weight = base_name+"_pop_weight.txt"
        p_t = open(p_f_time,'a')
        p_w = open(p_f_weight,'a')
        e_f_time = base_name+"_elite_time.txt"
        e_f_weight = base_name+"_elite_weight.txt"
        e_t = open(e_f_time,'a')
        e_w = open(e_f_weight,'a')
        m_f_time = base_name+"_mutate_time.txt"
        m_f_weight = base_name+"_mutate_weight.txt"
        m_t = open(m_f_time,'a')
        m_w = open(m_f_weight,'a')
        for rep in reps:
            now = time.time()
            sol = gene.genetic(G,reps = rep)
            passed = time.time()-now
            result = utils.objective(sol)
            write_to_file(f_t,rep,passed)
            write_to_file(f_w,rep,result)
        for pop in pop_size:
            now = time.time()
            sol = gene.genetic(G,pop_size=pop)
            passed = time.time()-now
            result = utils.objective(sol)
            write_to_file(p_t,pop,passed)
            write_to_file(p_w,pop,result)
        for elite in elite_size:
            now = time.time()
            sol = gene.genetic(G,elite_size=elite)
            passed = time.time()-now
            result = utils.objective(sol)
            write_to_file(e_t,elite,passed)
            write_to_file(e_w,elite,result)
        for m in mutate_chance:
            now = time.time()
            sol = gene.genetic(G,chance=m)
            passed = time.time()-now
            result = utils.objective(sol)
            write_to_file(m_t,elite,passed)
            write_to_file(m_w,elite,result)


        
    return

if __name__=='__main__':
    random.seed(152)
    test_tabu_graph()
    #test_genetic()
