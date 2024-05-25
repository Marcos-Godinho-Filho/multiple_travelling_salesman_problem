'''
Theorical Reference:
    * https://medium.com/@Data_Aficionado_1083/genetic-algorithms-optimizing-success-through-evolutionary-computing-f4e7d452084f
    * https://towardsdatascience.com/introduction-to-optimization-with-genetic-algorithm-2f5001d9964b

Code Reference:
    * https://github.com/Rayan-Ali1083/Genetic-Algorithm
    * https://medium.com/aimonks/traveling-salesman-problem-tsp-using-genetic-algorithm-fea640713758
'''
from utils import calculate_tour_total_distance
import random
import copy


def initialize_population(genes: list, heuristic_solution, population_size):
    population = list()

    for i in range(population_size):
        # is a copy if the heuristic solution so it does not have to calculate remaining
        # cities. Furthermore, it's easier to create new population because it just have
        # to change the genes in each salesman
        tour_model = copy.deepcopy(heuristic_solution)

        tours = list()

        for salesman in tour_model:
            new_genes = copy.deepcopy(genes)
            # must remove the city from where the salesman leaves/finishes the tour, since that city
            # cannot be in the middle of the tour when creating a new individual, e.g [3,...3,...3]
            new_genes.remove(salesman[0])
            random.shuffle(new_genes)
            for j in range(len(new_genes)):
                salesman[j + 1] = new_genes[j]

            tours.append(salesman)

        population.append(tours)

    return population


def calculate_fitness(population, distances):
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
    for i in range(len(population)):
        tours_total_distances.append(calculate_tour_total_distance(population[i], distances))

    # the tour that has the maximum total distance
    max_tour_distance = max(tours_total_distances)

    scores = list()
    for tour_distance in tours_total_distances:
        # the lower the tour total distance, the higher score that tour has
        scores.append(max_tour_distance - tour_distance)

    total_score = sum(scores)
    fitness_score = [score / total_score for score in scores]

    return fitness_score


def select_from_population(population, population_score):
    # Sort population according to fitness
    sorted_population = sorted(enumerate(population), key = lambda idx, _: population_score[idx])

    # Return top 50% of population => Most adapted
    return sorted_population[:int(0.5 * len(population))]


def crossover(selected_population, population, genes):
    offspring = list()

    for i in range(len(population)):
        # One parent from the top 50%
        parent1 = random.choice(selected_population)
        # The other one is random, can be from bottom 50% for example
        parent2 = random.choice(population)

        # Crossover point will also be random
        crossover_point = random.randint(1, len(genes) - 1)

        idx = 0
        child = list()
        for idx1, salesman in parent1:
            child.append([])
            for idx2, city in salesman:
                if crossover_point < idx:
                    child[idx1].append(city)
                else:
                    child[idx1].append(parent2[idx1][idx2])

        offspring.append(child)

    return offspring


def mutate(offspring, mutation_rate, genes):
    mutated_offspring = list()

    for individual in offspring:
        # we perform mutations while the random() returns True
        while random.random() < mutation_rate:
            i, j = random.sample(range(genes), 2)

            # we choose two random indexes
            idx = 0
            for idx1, salesman in individual:
                for idx2, _ in salesman:
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

    for p, n in zip(enumerate(population), enumerate(new_generation)):
        # If new generation fitness score is greater than current population's one, we replace it
        if population_score[p[0]] < new_generation_score[[n[0]]]:
            population[p[0]] = new_generation[n[0]]

    return population


def main(population_size, mutation_rate, genes, initial_solution, n_generations, distances):

    initial_population = initialize_population(genes, initial_solution, population_size)
    print(initial_population)

    current_population = copy.deepcopy(initial_population)
    population_score = calculate_fitness(current_population, distances)

    for i in n_generations:
        # select 50% best individuals from population
        selected = select_from_population(current_population, population_score)

        # perform crossover between selected population and the rest of it
        crossovered = crossover(selected, current_population, genes)

        # perform mutation
        new_generation = mutate(crossovered, mutation_rate, genes)

        new_generation_score = calculate_fitness(new_generation)

        # natural selection itself
        population = replace(current_population, population_score, new_generation, new_generation_score)

    return population
