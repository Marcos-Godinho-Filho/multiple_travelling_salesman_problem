from utils import calculate_tour_total_distance
import random
import math
import copy
import time

# esta função gera a vizinhança utilizando um operador de busca local chamado SWAP
def get_neighbors(current_solution, n_cities, number_of_neighbors_to_generate, distances):
    possible_solutions = []
    for k in range(number_of_neighbors_to_generate):
        # estamos criando uma cópia dessa variável com endereços de memória diferentes uma da outra mas com valores iguais
        neighbor_solution = copy.deepcopy(current_solution)

        i, j = random.sample(range(n_cities), 2)

        idx = 0
        for idx1, salesman in enumerate(neighbor_solution):
            for idx2, _ in enumerate(salesman):
                if idx == i:
                    i = [idx1, idx2]
                if idx == j:
                    j = [idx1, idx2]
                idx += 1

        neighbor_solution[i[0]][i[1]], neighbor_solution[j[0]][j[1]] = neighbor_solution[j[0]][j[1]], neighbor_solution[i[0]][i[1]]
        possible_solutions.append(neighbor_solution)

    best_neighbor = min(possible_solutions, key = lambda x: calculate_tour_total_distance(x, distances))

    return best_neighbor

# alpha: constante de decaimento da temperatura no intervalo [0, 1]
# initial_temperature: temperatura inicial > 0
# maximum_iterations: número máximo de iterações do algoritmo
def main(alpha, initial_temperature, min_temperature, initial_solution, n_cities, distances, k_neighbors_to_generate):

    start_time = time.time()

    # criar algo para controlar o decaimento da temperatura
    current_temperature = initial_temperature

    # criar uma solução inicial ou "chute" inicial
    # (a) heurística aleatória
    # (b) heurística gulosa
    # current_solution = random.sample(range(n_cities), n_cities)
    current_solution = initial_solution

    # explorará o espaço de soluções por maximum_iterations
    # while current_temperature >= 0.0:
    while current_temperature > min_temperature:

        neighbor_solution = get_neighbors(current_solution, n_cities, k_neighbors_to_generate, distances)

        # construir a vizinhança de current_solution e escolher uma delas
        # neighbor_solution = get_neighbors(current_solution)

        # calcular diferença entre o valor da função objetivo da solução vizinha escolhida e a solução atual
        current_solution_total_distance = calculate_tour_total_distance(current_solution, distances)
        neighbor_solution_total_distance = calculate_tour_total_distance(neighbor_solution, distances)

        delta = current_solution_total_distance - neighbor_solution_total_distance

        # delta == 0: solução atual é igual a solução vizinha escolhida
        # delta < 0: solução atual é melhor que a solução vizinha escolhida
        # delta > 0: solução vizinha escolhida é melhor que a solução atual
        if delta < 0:
            current_solution = neighbor_solution
        # até a linha de cima, temos o algoritmo do hill climbing
        else:
            try:
                if random.uniform(0,1) < math.exp(delta / current_temperature):
                    current_solution = neighbor_solution
            except OverflowError:
                break

        # current_temperature = current_temperature - alpha
        current_temperature = alpha * current_temperature

    end_time = time.time()

    return current_solution, end_time - start_time
