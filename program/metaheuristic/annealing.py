from heuristic import walk_through_tours
import random
import math
import copy

# esta função gera a vizinhança utilizando um operador de busca local chamado SWAP
def get_neighbors(current_solution, n_cities):

    # estamos criando uma cópia dessa variável com endereços de memória diferentes uma da outra mas com valores iguais
    neighbor_solution = copy.deepcopy(current_solution)
    try:
        i, j = random.sample(range(n_cities), 2)
        if (i != 0 and j != n_cities - 1) and (j != 0 and i != n_cities - 1):
            # Must not change first and last city from solution, since it's centroid
            neighbor_solution[i], neighbor_solution[j] = neighbor_solution[j], neighbor_solution[i]
    except IndexError:
        print(i, j)

    return neighbor_solution

# alpha: constante de decaimento da temperatura no intervalo [0, 1]
# initial_temperature: temperatura inicial > 0
# maximum_iterations: número máximo de iterações do algoritmo
def annealing(alpha, initial_temperature, maximum_iterations, initial_solution, n_cities, distances):
    # criar algo para controlar o decaimento da temperatura
    current_temperature = initial_temperature

    # criar uma solução inicial ou "chute" inicial
    # (a) heurística aleatória
    # (b) heurística gulosa
    # current_solution = random.sample(range(n_cities), n_cities)
    current_solution = initial_solution

    # explorará o espaço de soluções por maximum_iterations
    # while current_temperature >= 0.0:
    for k in range(maximum_iterations):
        neighbor_solution = list()

        # generate neighbors for every salesman trajectory
        for salesman_solution in current_solution:
            salesman_neighbor_solution = get_neighbors(salesman_solution, n_cities)
            neighbor_solution.append(salesman_neighbor_solution)

        # construir a vizinhança de current_solution e escolher uma delas
        # neighbor_solution = get_neighbors(current_solution)

        # calcular diferença entre o valor da função objetivo da solução vizinha escolhida e a solução atual
        current_solution_total_distance = walk_through_tours(current_solution, distances)
        neighbor_solution_total_distance = walk_through_tours(neighbor_solution, distances)

        delta = current_solution_total_distance - neighbor_solution_total_distance

        # delta == 0: solução atual é igual a solução vizinha escolhida
        # delta < 0: solução atual é melhor que a solução vizinha escolhida
        # delta > 0: solução vizinha escolhida é melhor que a solução atual
        if delta > 0:
            current_solution = neighbor_solution
        # até a linha de cima, temos o algoritmo do hill climbing
        else:
            try:
                if random.uniform(0,1) < math.exp(-delta / current_temperature):
                    current_solution = neighbor_solution
            except OverflowError:
                break

        # current_temperature = current_temperature - alpha
        current_temperature = alpha * current_temperature

    return current_solution
