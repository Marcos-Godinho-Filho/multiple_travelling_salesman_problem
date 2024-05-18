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
import random

POPULATION_SIZE = 500
MUTATION_RATE = 0.1
TARGET = '123456790123456'
GENES = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,!0123456789'

# Initilize population
def initialize_population(target):
    population = list()
    target_len = len(target) # chromossome size => number of genes
    for i in range(POPULATION_SIZE):
        chromossome = list()
        for j in range(target_len):
            chromossome.append(random.choice(GENES))
        population.append(chromossome)
    return population
    # population = [[random.choice(GENES) for j in range(target_len)] for i range(POPULATION_SIZE)]


def calculate_fitness(target, chromossome_from_population):
    difference = 0
    for target_position, gene in zip(target, chromossome_from_population):
        if target_position != gene:
            difference += 1
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


def mutate(offspring, mutation_rate):
    mutated_offspring = list()

    for chromossome in offspring:
        for gene in range(len(chromossome)):
            if random.random() < mutation_rate:
                chromossome[gene] = random.choice(GENES)
        mutated_offspring.append(chromossome)

    return mutated_offspring


def replace(new_generation, population):
    for i in range(len(population)):
        # If current fitness is greater than new fitness, it is bad and we must replace it
        if population[i][1] > new_generation[i][1]:
            population[i][0] = new_generation[i][0]
            population[i][1] = new_generation[i][1]
    return population


def main(population_size, mutation_rate, target, genes):
    # 1) Initialize population
    initial_population = initialize_population(target)
    population = list()
    target_found = False
    generation = 1

    # 2) Order population according to fitness
    for chromossome in initial_population:
        population.append(calculate_fitness(target, chromossome))

    # 3) Natural selection
    while not target_found:
        # 3.1) Select 50% best chromossomes from population
        selected = select_from_population(population)

        # 3.2) Perform crossover between selected population and the rest of it
        population = sorted(population, key = lambda chromossome: chromossome[1])
        crossovered = crossover(selected, len(target), population)

        # 3.3) Perform mutation
        mutated = mutate(crossovered, mutation_rate)

        new_generation = [calculate_fitness(target, chromossome) for chromossome in mutated]

        # 3.4) Natural selection itself
        population = replace(new_generation, population)

        # If the best chromossome in population has a fitness of 0, it has found the target
        if (population[0][1] == 0):
            print('Target found')
            print('String: ' + str(population[0][0]) + ' Generation: ' + str(generation) + ' Fitness: ' + str(population[0][1]))
            target_found = True

        print('String: ' + str(population[0][0]) + ' Generation: ' + str(generation) + ' Fitness: ' + str(population[0][1]))
        generation += 1


if __name__ == '__main__':
    main(POPULATION_SIZE, MUTATION_RATE, TARGET, GENES)
