import sys
import random
import tsplib95 as tsp
import algorithms as alg
import generators as gen
import utils
import time
import os

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




def test_k():
    graph_sizes = [50,100,300]
    loaded_asym = []
    loaded_sym = []
    k = 1
    dk = 5
    for file in os.listdir(os.getcwd()+"/Graphs/asym"):
        loaded_asym.append(load(os.getcwd()+"/Graphs/asym/"+file))
    for file in os.listdir(os.getcwd()+"/Graphs/sym"):
        loaded_sym.append(load(os.getcwd()+"/Graphs/sym/"+file))
    for size in graph_sizes:
        graph_sym = gen.generate_symmetric(size,1000)
        graph_asym = gen.generate_asymmetric(size,1000)
        time_file_sym = open_file("time","sym",size,"k-random")
        weight_file_sym = open_file("weight","sym",size,"k-random")
        time_file_asym = open_file("time","asym",size,"k-random")
        weight_file_asym = open_file("weight","asym",size,"k-random")
        while k<50:  
            now = time.time()
            asym_solution = alg.k_random(k,graph_asym)
            asym_time = time.time()-now
            write_to_file(time_file_asym,k,asym_time)
            write_to_file(weight_file_asym,k,utils.objective(asym_solution))
            now = time.time()
            sym_solution = alg.k_random(k,graph_sym)
            sym_time = time.time()-now
            write_to_file(time_file_sym,k,sym_time)
            write_to_file(weight_file_sym,k,utils.objective(sym_solution))
            k+=dk
        time_file_sym.close()
        weight_file_sym.close()
        time_file_asym.close()
        weight_file_asym.close()
        k=1
    time_file_loaded_sym = open_file("time","loaded_sym",size,"k-random")
    weight_file_loaded_sym = open_file("weight","loaded_sym",size,"k-random")
    for graph in loaded_sym:
        while k<50:  
            now = time.time()
            sym_solution = alg.k_random(k,graph)
            sym_time = time.time()-now
            write_to_file(time_file_loaded_sym,k,sym_time)
            write_to_file(weight_file_loaded_sym,k,sym_solution)
            k+=dk
        k=1
    time_file_loaded_sym.close()  
    weight_file_loaded_sym.close()
    time_file_loaded_asym = open_file("time","loaded_asym",size,"k-random")
    weight_file_loaded_asym = open_file("weight","loaded_asym",size,"k-random")
    for graph in loaded_asym:
        while k<50:  
            now = time.time()
            asym_solution = alg.k_random(k,graph)
            asym_time = time.time()-now
            write_to_file(time_file_loaded_asym,k,asym_time)
            write_to_file(weight_file_loaded_asym,k,asym_solution)
            k+=dk
        k=1
    time_file_loaded_asym.close()  
    weight_file_loaded_asym.close()

def make_tests():
    loaded_graphs_asym = []
    loaded_graphs_sym = []
    graph_sizes = []
    start_size = 15
    step_size = 10
    curr_size = start_size
    counter = 0

    for file in os.listdir(os.getcwd()+"/Graphs/asym"):
        loaded_graphs_asym.append(load(os.getcwd()+"/Graphs/asym/"+file))

    for file in os.listdir(os.getcwd()+"/Graphs/sym"):
        loaded_graphs_sym.append(load(os.getcwd()+"/Graphs/sym/"+file))

    while curr_size<45:
        graph_sizes.append(curr_size)
        curr_size += step_size
        counter+=1
        if counter >=10:
            step_size +=5
            counter =0

    for size in graph_sizes:
        graph_sym = gen.generate_symmetric(size,1000)
        graph_asym = gen.generate_asymmetric(size,1000)


        time_file = open_file_no_size("time","sym","k_random")
        weight_file = open_file_no_size("weight","sym","k_random")
        test_one_alg(alg.k_random,graph_sym,size,time_file ,weight_file)
        time_file.close()
        weight_file.close()

        time_file = open_file_no_size("time","sym","nearest_neighbour")
        weight_file = open_file_no_size("weight","sym","nearest_neighbour")
        test_one_alg(alg.nearest_neighbour,graph_sym,size,time_file ,weight_file)
        time_file.close()
        weight_file.close()

        time_file = open_file_no_size("time","asym","nearest_neighbour")
        weight_file = open_file_no_size("weight","asym","nearest_neighbour")
        test_one_alg(alg.nearest_neighbour,graph_asym,size,time_file,weight_file)
        time_file.close()
        weight_file.close()

        time_file = open_file_no_size("time","sym","repetitive_neighbour")
        weight_file= open_file_no_size("weight","sym","repetitive_neighbour")
        test_one_alg(alg.repetitive_nearest_neighbour,graph_sym,size,time_file,weight_file)
        time_file.close()
        weight_file.close()


        time_file = open_file_no_size("time","asym","k_random")
        weight_file = open_file_no_size("weight","asym","k_random")
        test_one_alg(alg.k_random,graph_asym,size,time_file ,weight_file)
        time_file.close()
        weight_file.close()


        time_file = open_file_no_size("time","asym","repetitive_neighbour")
        weight_file = open_file_no_size("weight","asym","repetitive_neighbour")
        test_one_alg(alg.repetitive_nearest_neighbour,graph_asym,size,time_file,weight_file)
        time_file.close()
        weight_file.close()

        time_file = open_file_no_size("time","sym","2-opt")
        weight_file = open_file_no_size("weight","sym","2-opt")
        test_one_alg(alg._2_opt,graph_sym,size,time_file,weight_file)
        time_file.close()
        weight_file.close()

        time_file = open_file_no_size("time","asym","2-opt")
        weight_file = open_file_no_size("weight","asym","2-opt")
        test_one_alg(alg._2_opt,graph_asym,size,time_file,weight_file)
        time_file.close()
        weight_file.close()


    for graph_sym in loaded_graphs_sym:

        time_file = open_file_no_size("time","loaded_sym","k_random")
        weight_file = open_file_no_size("weight","loaded_sym","k_random")
        test_one_alg(alg.k_random,graph_sym,len(list(graph_sym.nodes())),time_file ,weight_file)
        time_file.close()
        weight_file.close()


        time_file = open_file_no_size("time","loaded_sym","nearest_neighbour")
        weight_file = open_file_no_size("weight","loaded_sym","nearest_neighbour")
        test_one_alg(alg.nearest_neighbour,graph_sym,len(list(graph_sym.nodes())),time_file ,weight_file)
        time_file.close()
        weight_file.close()


        time_file = open_file_no_size("time","loaded_sym","repetitive_neighbour")
        weight_file= open_file_no_size("weight","loaded_sym","repetitive_neighbour")
        test_one_alg(alg.repetitive_nearest_neighbour,graph_sym,len(list(graph_sym.nodes())),time_file,weight_file)
        time_file.close()
        weight_file.close()


        time_file = open_file_no_size("time","loaded_sym","2-opt")
        weight_file = open_file_no_size("weight","loaded_sym","2-opt")
        test_one_alg(alg._2_opt,graph_sym,len(list(graph_sym.nodes())),time_file,weight_file)
        time_file.close()
        weight_file.close()

    for graph_asym in loaded_graphs_asym:


        time_file = open_file_no_size("time","loaded_asym","k_random")
        weight_file = open_file_no_size("weight","loaded_asym","k_random")
        test_one_alg(alg.k_random,graph_asym,len(list(graph_sym.nodes())),time_file ,weight_file)
        time_file.close()
        weight_file.close()


        time_file = open_file_no_size("time","loaded_asym","nearest_neighbour")
        weight_file = open_file_no_size("weight","loaded_asym","nearest_neighbour")
        test_one_alg(alg.nearest_neighbour,graph_asym,len(list(graph_asym.nodes())),time_file ,weight_file)
        time_file.close()
        weight_file.close()


        time_file = open_file_no_size("time","loaded_asym","repetitive_neighbour")
        weight_file= open_file_no_size("weight","loaded_asym","repetitive_neighbour")
        test_one_alg(alg.repetitive_nearest_neighbour,graph_asym,len(list(graph_asym.nodes())),time_file,weight_file)
        time_file.close()
        weight_file.close()


        time_file = open_file_no_size("time","loaded_asym","2-opt")
        weight_file = open_file_no_size("weight","loaded_asym","2-opt")
        test_one_alg(alg._2_opt,graph_asym,len(list(graph_asym.nodes())),time_file,weight_file)
        time_file.close()
        weight_file.close()


def test_one_alg(chosen_alg,graph,size,time_file,weight_file):
    solution_times = []
    solution_costs = []
    iterations = 3
    for i in range(iterations):
        now = time.time()
        solution = chosen_alg(graph)
        timing = time.time()-now
        solution_times.append(timing)
        solution_costs.append(utils.objective(solution))
        if timing != 0.00:
            break
    avg_time = sum(solution_times)/len(solution_times)
    avg_cost = sum(solution_costs)/len(solution_costs)
    write_to_file(time_file,size,avg_time)
    write_to_file(weight_file,size,avg_cost)

    

def test_all(G):
    algorithms = [
        alg.nearest_neighbour, 
        alg.repetitive_nearest_neighbour,
        alg._2_opt
    ]

    for algorithm in algorithms:
        print(utils.objective(algorithm(G)))


if __name__=='__main__':
    G = gen.generate_asymmetric(100, 4000)
    #test_all(G)
    #test_k()
    make_tests()
