import algorithms as algs
import networkx as nx
import random
import utils
import math
def genetic(G, pop_size=50, reps=1000,elite_size = -1,chance = 10 ):
    if elite_size<0:
        elite_size =math.ceil(pop_size/10)
    population = generate_population(G, algs.nearest_neighbour, pop_size)
    best_weight = float('inf')
    best_sol = None
    i = 0
    while i < reps:
        for member in population:
            if member[1] < best_weight:
                best_weight = member[1]
                best_sol = member[0]
                i = 0
                print(member[1])
        parents,elite = selection(G, population,pop_size,elite_size)
        population = breed(G, parents,chance)
        population+=elite
        population = sorted(population,key = lambda x:x[1])
        population = population[:pop_size]
        i+=1

    return best_sol


def generate_population(G, alg=algs.k_random, pop_size=10):
    population = []

    for n in range(pop_size):
        sol = alg(G)
        weight = utils.objective(sol)
        population.append((sol,weight))

    return population

def mutate(G,route,operation = algs.invert):
    geneA = random.randint(0, len(G.nodes())-1)
    geneB = random.randint(0, len(G.nodes())-1)
    start = min(geneA, geneB)
    end = max(geneA, geneB)
    return operation(G,route,start,end)


def selection(G, population, pop_size, elite_size=2): #tournament
    parents = []
    sortu = sorted(population,key = lambda x:x[1])
    while len(parents)<pop_size:
        potential_parents = []

        for i in range(30):
            p = random.choice(population)
            potential_parents.append(p)

        best = potential_parents[0]
        for element in potential_parents:
            if element[1] < best[1]:
                best = element

        parents.append(best)
    the_best_parents = sortu[0:elite_size]
    return parents, the_best_parents
        
def selection2(G, population, pop_size, elite_size=2): #roulette
    parents = []
    
    prob = []
    sortu = sorted(population,key = lambda x:x[1])
    
    maxi = population[0][1]
    sum = 0

    for i in range(len(population)):
        if maxi < population[i][1]:
            maxi = population[i][1]
        sum+=1/population[i][1]

    for i in range(len(population)):
        prob.append((1/population[i][1])/sum)

    while len(parents)<pop_size:
        for i in range(len(population)):
            if random.uniform(0,1)>prob[i] and population[i] not in parents:
                parents.append(population[i])
                if len(parents)>=pop_size:
                    break
    return parents,sortu[0:elite_size]

def single_breed(G,parent1,parent2,start,end,chance = 40):
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
    if prob<=chance: 
        child = mutate(G,child)
    return (child,utils.objective(child))


def breed(G, parents,chance):
    new_pop = []
    for i in range(0, len(parents)-1, 2):
        parent1 = parents[i][0].nodes()
        parent2 = parents[i+1][0].nodes()
        geneA = random.randint(0, len(parent1)-1)
        geneB = random.randint(0, len(parent2)-1)

        start = min(geneA, geneB)
        end = max(geneA, geneB)
        new_pop.append(single_breed(G,parent1,parent2,start,end,chance))
        new_pop.append(single_breed(G,parent2,parent1,start,end,chance))

    return new_pop
