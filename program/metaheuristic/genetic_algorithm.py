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


def partition(population, initial_city):

    partitioned_population = []

    for individual in population:
        partitioned = []
        solution, cities_per_salesman = individual

        i1, i2 = 0, 0
        i = 0

        for n_city in cities_per_salesman:
            i1 = i2
            i2 += n_city

            partitioned.append([])
            partitioned[i].append(initial_city)
            partitioned[i].extend(solution[i1:i2])
            partitioned[i].append(initial_city)

        partitioned_population.append(partitioned)

    return partitioned_population


def initialize_solution_gene(heuristic_solution):
    solution = []
    initial_city = heuristic_solution[0][0]

    for salesman in heuristic_solution:
        for city in salesman:
            if city != initial_city:
                solution.append(city)

    tours = copy.deepcopy(solution)
    random.shuffle(tours)

    return tours


def initialize_cities_per_salesman_gene(n, m):
    while True:
        pick = random.sample(range(2, n - 2 * (m - 1)), m)
        if sum(pick) == n - 1:
            return pick


def initialize_population(heuristic_solution, n, population_size):
    population = []

    for i in range(population_size):
        population.append([])
        population[i].append(initialize_solution_gene(heuristic_solution))
        population[i].append(initialize_cities_per_salesman_gene(n, len(heuristic_solution)))

    return population


def calculate_fitness(population, distances, initial_city):
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

    partitioned = partition(population, initial_city)

    for i in range(len(partitioned)):
        tours_total_distances.append(calculate_tour_total_distance(partitioned[i], distances))

    # the tour that has the maximum total distance
    max_tour_distance = max(tours_total_distances)

    scores = list()
    for tour_distance in tours_total_distances:
        # the lower the tour total distance, the higher the tour score
        scores.append(max_tour_distance - tour_distance)

    total_score = sum(scores)
    if total_score != 0:
        fitness_score = [score / total_score for score in scores]
    else:
        fitness_score = [1/len(partitioned) for score in scores]

    return fitness_score


def select_from_population(population, population_score):
    # Combine population + population_score in order to order it
    combined = list(zip(population, population_score))

    # Sorts based on the score of each tour
    combined_sorted = sorted(combined, key = lambda x: x[1], reverse=True)
    # Return top 50% of population => Most adapted and have greater scores
    elite = combined_sorted[:int(0.5 * len(population))]

    return [tour for tour, score in elite]


def crossover(selected_population, population):
    offspring = list()

    for i in range(len(population)):
        # One parent from the top 50%
        parent_1 = copy.deepcopy(random.choice(selected_population))
        # The other one is random, can be from bottom 50% for example
        parent_2 = copy.deepcopy(random.choice(population))

        parent_1_cities, parent_2_cities = parent_1[0], parent_2[0]

        proto_child = [-1 for j in range(len(parent_1_cities))]

        # Get a random set of cities from parent 1 and copy the cities
        # on those positions into the corresponding positions of the proto_child
        number_of_cities_from_parent_1 = random.randint(1, len(parent_1_cities))
        cities_from_parent_1 = random.sample(parent_1_cities, number_of_cities_from_parent_1)
        for index, city in enumerate(parent_1_cities):
            if city in cities_from_parent_1:
                proto_child[index] = city

        # Ignore the cities which are already in the proto_child from the second parent.
        # The resulting sequence of cities contains the cities the proto-child needs.
        # Place the cities into the unfixed position of the proto-child from left to
        # right according to the order of the sequence to produce one offspring
        already_in_proto_child = []
        for j in range(len(proto_child)):
            if proto_child[j] == -1:
                for city in parent_2_cities:
                    if city not in cities_from_parent_1 and city not in already_in_proto_child:
                        proto_child[j] = city
                        already_in_proto_child.append(city)
                        break

        # Final child containing the proto_child (cities) and the nubmer of cities per
        # salesman, which is the second gene, selected from the bes parent
        child = [proto_child, parent_1[1]]

        offspring.append(child)

    return offspring


def mutate(offspring, mutation_rate, cities, m):
    mutated_offspring = list()

    copy_cities = copy.deepcopy(cities)
    copy_cities.pop()

    for individual in offspring:

        # we perform mutations while the random() returns True
        while random.random() < mutation_rate:

            i, j = random.sample(copy_cities, 2)
            # SWAP approach - solution gene
            individual[0][i.id], individual[0][j.id] = individual[0][j.id], individual[0][i.id]

            # SWAP approach - n_cities gene
            individual[1].clear()
            individual[1].extend(initialize_cities_per_salesman_gene(len(cities), m))

        mutated_offspring.append(individual)

    return mutated_offspring


def replace(population, population_score, new_generation, new_generation_score):
    new_population = copy.deepcopy(population)
    for p, n in zip(enumerate(population), enumerate(new_generation)):
        # If new generation fitness score is greater than current population's one, we replace it
        if population_score[p[0]] < new_generation_score[n[0]]:
            new_population[p[0]] = new_generation[n[0]]

    return new_population


def main(population_size, mutation_rate, cities, initial_solution, n_generations, distances):

    initial_city = initial_solution[0][0]

    current_population = initialize_population(initial_solution, len(distances), population_size)

    for i in tqdm(range(n_generations)):

        current_population_score = calculate_fitness(current_population, distances, initial_city)

        selected = select_from_population(current_population, current_population_score)

        # perform crossover between selected population and the rest of it
        crossovered = crossover(selected, current_population)

        # perform mutation
        new_generation = mutate(crossovered, mutation_rate, cities, len(initial_solution))

        new_generation_score = calculate_fitness(new_generation, distances, initial_city)

        # natural selection itself
        current_population = replace(current_population, current_population_score, new_generation, new_generation_score)

    # Select the best individual from the final population
    current_population_score = calculate_fitness(current_population, distances, initial_city)
    final_elite = select_from_population(current_population, current_population_score)
    best_tour = final_elite[0]
    best_tour = partition([best_tour], initial_city)
    best_tour = best_tour[0]

    return best_tour
