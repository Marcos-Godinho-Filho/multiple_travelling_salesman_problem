'''
Theorical Reference:
    * https://medium.com/@Data_Aficionado_1083/genetic-algorithms-optimizing-success-through-evolutionary-computing-f4e7d452084f
    * https://towardsdatascience.com/introduction-to-optimization-with-genetic-algorithm-2f5001d9964b

Code Reference:
    * https://github.com/Rayan-Ali1083/Genetic-Algorithm
    * https://medium.com/aimonks/traveling-salesman-problem-tsp-using-genetic-algorithm-fea640713758
'''
from utils import calculate_tour_total_distance
from typing import List
import random
import copy
from tqdm import tqdm
from time import sleep


def partition(population, initial_city, m):

    partitioned_population = []

    for individual in population:
        partitioned = []
        i = -1

        for index, city in enumerate(individual):
            if index % m == 0:
                partitioned.append([])
                i += 1
                
                partitioned[i-1].append(initial_city)
                partitioned[i].append(initial_city)
            partitioned[i].append(city)

        partitioned_population.append(partitioned)

    return partitioned_population


def initialize_population(heuristic_solution, population_size):
    population = []
    solution = []
    initial_city = heuristic_solution[0][0]

    for salesman in heuristic_solution:
        for city in salesman:
            if city != initial_city:
                solution.append(city)

    for i in range(population_size):

        tours = copy.deepcopy(solution)
        random.shuffle(tours)

        population.append(tours)

    return population


def calculate_fitness(population, distances, m):
    '''
    Generates a [0, 1] score for each chromossome (tour) within a population.
    This score is calculated using the maximum tour distance. That is:
        tours_total_distances = [1000, 2500, 6000, 7000]
    Will produce a:
        score = [6000, 4500, 1000, 0]
    And consequently:
        fitness_score = [0,36; 0,27; 0,06; 0]
    '''
    tours_total_distances = []

    partitioned = partition(population, m)

    for i in range(len(partitioned)):
        tours_total_distances.append(calculate_tour_total_distance(partitioned[i], distances))

    # the tour that has the maximum total distance
    max_tour_distance = max(tours_total_distances)

    scores = list()
    for tour_distance in tours_total_distances:
        # the lower the tour total distance, the higher the tour score
        scores.append(max_tour_distance - tour_distance)

    total_score = sum(scores)
    fitness_score = [score / total_score for score in scores]

    return fitness_score


def select_from_population(population, population_score):
    # Combine population + population_score in order to order it
    combined = list(zip(population, population_score))

    # Sorts based on the score of each tour
    combined_sorted = sorted(combined, key = lambda x: x[1])
    # Return top 50% of population => Most adapted and have greater scores
    elite = combined_sorted[:int(0.5 * len(population))]

    return [tour for tour, score in elite]


def crossover(selected_population, population, genes):
    offspring = list()

    for i in range(len(population)):
        # One parent from the top 50%
        parent1 = random.choice(selected_population)
        # The other one is random, can be from bottom 50% for example
        parent2 = random.choice(population)

        # Crossover point will also be random
        crossover_point_1, crossover_point_2 = random.sample(genes, 2)

        idx = 0
        child = list()

        left: List = copy.deepcopy(genes)
        last = []

        for idx1, salesman in enumerate(parent1):
            child.append([])
            for idx2, city in enumerate(salesman):
                if idx >= crossover_point_1 and idx < crossover_point_2:
                    city2 = parent2[idx1][idx2]

                    if city2 not in child[idx1]:
                        child[idx1].append(city2)
                        left.remove(city2)
                else:
                    if idx >= crossover_point_2:
                        last.append(city)
                        if city in left:
                            left.remove(city)
                    else:
                        child[idx1].append(city)

                idx += 1

            for i in left:
                child[idx1].append(i)
            for i in last:
                child[idx1].append(i)

        print(child)
        sleep(100)
        offspring.append(child)

    return offspring


def mutate(offspring, mutation_rate, genes):
    mutated_offspring = list()

    for individual in offspring:
        # we perform mutations while the random() returns True
        while random.random() < mutation_rate:
            i, j = random.sample(genes, 2)

            # we choose two random indexes
            idx = 0
            for idx1, salesman in enumerate(individual):
                for idx2, _ in enumerate(salesman):
                    if idx == i:
                        i = [idx1, idx2]
                    if idx == j:
                        j = [idx1, idx2]
                    idx += 1

            # SWAP approach
            individual[i[0]][i[1]], individual[j[0]][j[1]] = individual[j[0]][j[1]], individual[i[0]][i[1]]

        mutated_offspring.append(individual)

    return mutated_offspring


def replace(population, population_score, new_generation, new_generation_score):
    new_population = copy.deepcopy(population)
    for p, n in zip(enumerate(population), enumerate(new_generation)):
        # If new generation fitness score is greater than current population's one, we replace it
        if population_score[p[0]] < new_generation_score[n[0]]:
            new_population[p[0]] = new_generation[n[0]]

    return new_population


def main(population_size, mutation_rate, genes, initial_solution, n_generations, distances):

    initial_population = initialize_population(genes, initial_solution, population_size)

    current_population = copy.deepcopy(initial_population)
    population_score = calculate_fitness(current_population, distances)

    for i in tqdm(range(n_generations)):

        # select 50% best individuals from population
        selected = select_from_population(current_population, population_score)

        # perform crossover between selected population and the rest of it
        crossovered = crossover(selected, current_population, genes)

        # perform mutation
        new_generation = mutate(crossovered, mutation_rate, genes)

        new_generation_score = calculate_fitness(new_generation, distances)

        # natural selection itself
        current_population = replace(current_population, population_score, new_generation, new_generation_score)

    # Select the best individual from the final population
    population_score = calculate_fitness(current_population, distances)
    final_elite = select_from_population(current_population, population_score)
    best_tour = final_elite[0]

    return best_tour
