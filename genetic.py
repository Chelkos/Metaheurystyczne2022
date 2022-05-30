import algorithms as algs
import networkx as nx
import random
import utils as utils

def generate_population(G, alg=algs.k_random, pop_size =10):
    population = []

    for n in range(pop_size):
        sol = alg(G)
        weight = utils.objective(sol)
        population.append((sol,weight))
        print(sol.nodes()," ",weight)
    selection(G, population,pop_size)
    

#def generate_tuples(population):

def mutate(G,route,operation = algs.invert):
    geneA = random.randint(0, len(G.nodes())-1)
    geneB = random.randint(0, len(G.nodes())-1)
    start = min(geneA, geneB)
    end = max(geneA, geneB)
    return operation(G,route,start,end)


def selection(G, population, pop_size, elite_size=2):
    parents = []
    prob = []
    maxi = population[0][1]
    sum = 0

    for i in range(len(population)):
        if maxi < population[i][1]:
            maxi = population[i][1]
        sum+=1/population[i][1]

    for i in range(len(population)):
        prob.append((1/population[i][1])/sum)

    while len(parents)<pop_size/2:
        for i in range(len(population)):
            if random.randrange(0,1)<prob[i] and population[i] not in parents:
                parents.append(population[i])
                print(population[i][0].nodes())
                if len(parents)>=pop_size/2:
                    break
    breed(G, parents)
    return parents


def single_breed(G,parent1,parent2,start,end):


    print(start, end)
    child = nx.DiGraph()
    
    for j in range(start, end):
        child.add_node(list(parent1)[j])
    
    for j in range(end, len(parent2)):
        if list(parent2)[j] not in list(child.nodes()):
            child.add_node(list(parent2)[j])

    for j in range(0, end):
        if list(parent2)[j] not in list(child.nodes()):
            child.add_node(list(parent2)[j])

    nodes = list(child.nodes())
    for n in range(len(nodes) - 1):
        child.add_edge(nodes[n], nodes[n+1], weight=G[nodes[n]][nodes[n+1]]['weight'])
    
    child.add_edge(nodes[0], nodes[len(G.nodes())-1], weight=G[nodes[0]][nodes[len(G.nodes())-1]]['weight'])
    prob = random.randint(0,100) #mutacja i prawdopodobieństwo zajścia mutacji
    if prob<=1: 
        child = mutate(G,child)
    return (child,utils.objective(child))


def breed(G, parents):
    new_pop = []
    for i in range(0, len(parents)-1, 2):
        parent1 = parents[i][0].nodes()
        parent2 = parents[i+1][0].nodes()
        
        geneA = random.randint(0, len(parent1)-1)
        geneB = random.randint(0, len(parent2)-1)

        start = min(geneA, geneB)
        end = max(geneA, geneB)
        new_pop.append(single_breed(G,parent1,parent2,start,end))
        new_pop.append(single_breed(G,parent2,parent1,start,end))
        new_pop.append(parents[i])
        new_pop.append(parents[i+1])
        print(i)
    #print(new_pop)
