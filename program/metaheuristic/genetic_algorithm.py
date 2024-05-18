# https://www.tandfonline.com/doi/full/10.1080/21642583.2019.1674220
# https://medium.com/aimonks/traveling-salesman-problem-tsp-using-genetic-algorithm-fea640713758
# https://towardsdatascience.com/introduction-to-optimization-with-genetic-algorithm-2f5001d9964b
# https://towardsdatascience.com/genetic-algorithm-implementation-in-python-5ab67bb124a6
'''
Theorical Reference:
    * https://medium.com/@Data_Aficionado_1083/genetic-algorithms-optimizing-success-through-evolutionary-computing-f4e7d452084f

Code Reference:
    * https://github.com/Rayan-Ali1083/Genetic-Algorithm
'''
from heuristic import walk_through_tours
import random
import copy

POPULATION_SIZE = 500
MUTATION_RATE = 0.1


# Initilize population
def initialize_population(genes, heuristic_solution):
    population = list()

    for i in range(POPULATION_SIZE):
        model = copy.deepcopy(heuristic_solution)

        chromossome = list()
        for salesman in model:
            for gene in range(1, len(salesman) - 1):
                salesman[gene] = random.choice(genes)
            chromossome.append(salesman)

        population.append(chromossome)

    return population


def calculate_fitness(target, chromossome_from_population, distances):
    total_distance = walk_through_tours(chromossome_from_population, distances)
    difference = total_distance - target
    return [chromossome_from_population, difference]


def select_from_population(population):
    # Sort population according to fitness
    sorted_population = sorted(population, key = lambda chromossome: chromossome[1])

    # Return top 50% of population => Most adapted
    return sorted_population[:int(0.5 * POPULATION_SIZE)]


def crossover(selected_population, chromossome_len, population):
    offspring = list()

    for i in range(POPULATION_SIZE):
        # One parent from the top 50%
        parent1 = random.choice(selected_population)[0] # [0] gets chromossome it self, without fitness
        # The other one is random, can be from bottom 50% for example
        parent2 = random.choice(population[:int(POPULATION_SIZE * 50)])[0]

        # Crossover point will also be random
        crossover_point = random.randint(1, chromossome_len - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        offspring.append(child)

    return offspring


def mutate(offspring, mutation_rate, genes):
    mutated_offspring = list()

    for chromossome in offspring:
        for salesman in chromossome:
            for gene in range(len(salesman)):
                if random.random() < mutation_rate:
                    salesman[gene] = random.choice(genes)

        mutated_offspring.append(chromossome)

    return mutated_offspring


def replace(new_generation, population):
    for i in range(len(population)):
        # If current fitness is greater than new fitness, it is bad and we must replace it
        if population[i][1] > new_generation[i][1]:
            population[i][0] = new_generation[i][0]
            population[i][1] = new_generation[i][1]
    return population


def main(population_size, mutation_rate, target, genes, initial_solution, distances):
    # 1) Initialize population
    initial_population = initialize_population(genes, initial_solution)
    population = list()
    target_found = False
    generation = 1

    # 2) Order population according to fitness
    for chromossome in initial_population:
        population.append(calculate_fitness(target, chromossome, distances))

    # 3) Natural selection
    while not target_found:
        # 3.1) Select 50% best chromossomes from population
        selected = select_from_population(population)

        # 3.2) Perform crossover between selected population and the rest of it
        population = sorted(population, key = lambda chromossome: chromossome[1])
        crossovered = crossover(selected, target, population)

        # 3.3) Perform mutation
        mutated = mutate(crossovered, mutation_rate, genes)

        new_generation = [calculate_fitness(target, chromossome, distances) for chromossome in mutated]

        # 3.4) Natural selection itself
        population = replace(new_generation, population)

        # If the best chromossome in population has a fitness of 0, it has found the target
        if (population[0][1] == 0):
            print('Target found')
            print('String: ' + str(population[0][0]) + ' Generation: ' + str(generation) + ' Fitness: ' + str(population[0][1]))
            target_found = True

        print('String: ' + str(population[0][0]) + ' Generation: ' + str(generation) + ' Fitness: ' + str(population[0][1]))
        generation += 1
