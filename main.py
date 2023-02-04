# inspired by Prof. moshe sipper, BGU
import random

THREE_SAT_SIZE = 1000 #number of clauses
POP_SIZE = 1000 #number of individuals
N = 500 #number of variables
GENERATIONS = 200 #number of generations
TOURNAMENT_SIZE = 100 #number of individuals to pick from the population
MUTATION_PROB = 1 #the probability for mautation
MUTATION_TRESHOLD = 30 #the minimal gen to start mutating from.
ITERATIONS = 10 #number of iterations.
def randimize_t_f():
    return (random.uniform(0,1) < 0.5)

def randomize_individaul():
    return [randimize_t_f() for i in range(N)]

def randomize_population():
    return [randomize_individaul() for i in range(POP_SIZE)]

def smart_individual(index, default):
    res = []
    for i in range (0,N):
        if (i == index):
            res.append(default)
        else:
            res.append(not default)
    return res

def smart_population():
    res = []
    for i in range (0,N):
        res.append(smart_individual(i,True))
    for i in range (0,N):
        res.append(smart_individual(i,False))
    for i in range (N*2,POP_SIZE):
        res.append(randomize_individaul())
    return res



def randomize_3sat():
    res = []
    for i in range (THREE_SAT_SIZE):
        curr = []
        for i in range (3):
            curr.append([random.randint(0,N-1),randimize_t_f()])
        res.append(curr)
    return res

def check_clause(clause,individual):
    for curr in clause:
        x = curr[0]
        bool = curr[1]
        if (individual[x] == bool):
            return True
    return False

#-------------Evolutionaty Fuctions-----------------


def fitness(individaual,sat):
    counter = 0
    for clause in sat:
        if (check_clause(clause,individaual)):
            counter+=1
    return (counter/THREE_SAT_SIZE)

def selection(population,fitnesses):
    tournament = [random.randint(0, POP_SIZE-1) for i in range(TOURNAMENT_SIZE)] # select tournament contenders
    tournament_fitnesses = [fitnesses[tournament[i]] for i in range(TOURNAMENT_SIZE)]
    return population[tournament[tournament_fitnesses.index(max(tournament_fitnesses))]]

def mutation(individual):
    i = random.randint(0,N-1)
    individual[i] = not (individual[i])
    return individual

def crossover(parent1, parent2):
    son = []
    cut = random.randint(0,N-1)
    for i in range (cut):
        son.append(parent1[i])
    for i in range (cut,N):
        son.append(parent2[i])
    return son

def main():
    sat = randomize_3sat()
    results = []
    for i in range (ITERATIONS):
        population = randomize_population()
        fitnesses = [fitness(population[i], sat) for i in range(POP_SIZE)]
        best_of_run_gen = -1
        best_of_run = population[fitnesses.index(max(fitnesses))]
        best_of_run_fitness = max(fitnesses)
        print("----------Iteration ", i)
        for gen in range(GENERATIONS):
            print("----------Genertaion",gen,"-------")
            nextgen_population = []
            # elitism
            nextgen_population.append(best_of_run)
            for i in range(POP_SIZE-1):
                parent1 = selection(population, fitnesses)
                parent2 = selection(population, fitnesses)
                child = crossover(parent1,parent2)
                if (random.uniform(0,1) < MUTATION_PROB and gen>MUTATION_TRESHOLD):
                    child = mutation(child)
                nextgen_population.append(child)
            population = nextgen_population
            fitnesses = [fitness(population[i],sat) for i in range(POP_SIZE)]
            if max(fitnesses) > best_of_run_fitness:
                best_of_run_gen = gen
                best_of_run = population[fitnesses.index(max(fitnesses))]
                best_of_run_fitness = max(fitnesses)
                print("_________Improvement Achieved!_______________")
                print("gen:", best_of_run_gen, ", best_of_run_f:", best_of_run_fitness)
                if best_of_run_fitness == 1: break
        print("_________End Of Evolution!_______________")
        print("_________best results:_______________")
        print("gen:", best_of_run_gen, ", best_of_run_f:", best_of_run_fitness, "individual: ", best_of_run)
        results.append([best_of_run_gen, best_of_run_fitness])
    for i in range (ITERATIONS):
        print("Iteration ", i, ", Gen: ", results[i][0], ", Fitness: ", results[i][1])

if __name__ == "__main__":
    main()
