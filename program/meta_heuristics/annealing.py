import random
import math
import copy

n_cities = 17

distances = [
    [  0,   548,  776,  696,  582,  274,  502,  194,  308,  194,  536,  502,  388,  354,  468,  776,  662],
    [ 548,    0,  684,  308,  194,  502,  730,  354,  696,  742, 1084,  594,  480,  674, 1016,  868, 1210],
    [ 776,  684,    0,  992,  878,  502,  274,  810,  468,  742,  400, 1278, 1164, 1130,  788,  1552, 754],
    [ 696,  308,  992,    0,  114,  650,  878,  502,  844,  890, 1232,  514,  628,  822,  1164, 560, 1358],
    [ 582,  194,  878,  114,    0,  536,  764,  388,  730,  776, 1118,  400,  514,  708,  1050, 674, 1244],
    [ 274,  502,  502,  650,  536,    0,  228,  308,  194,  240,  582,  776,  662,  628,  514, 1050,  708],
    [ 502,  730,  274,  878,  764,  228,    0,  536,  194,  468,  354, 1004,  890,  856,  514, 1278,  480],
    [ 194,  354,  810,  502,  388,  308,  536,    0,  342,  388,  730,  468,  354,  320,  662,  742,  856],
    [ 308,  696,  468,  844,  730,  194,  194,  342,    0,  274,  388,  810,  696,  662,  320, 1084,  514],
    [ 194,  742,  742,  890,  776,  240,  468,  388,  274,    0,  342,  536,  422,  388,  274,  810,  468],
    [ 536, 1084,  400, 1232, 1118,  582,  354,  730,  388,  342,    0,  878,  764,  730,  388, 1152,  354],
    [ 502,  594, 1278,  514,  400,  776, 1004,  468,  810,  536,  878,    0,  114,  308,  650,  274,  844],
    [ 388,  480, 1164,  628,  514,  662,  890,  354,  696,  422,  764,  114,    0,  194,  536,  388,  730],
    [ 354,  674, 1130,  822,  708,  628,  856,  320,  662,  388,  730,  308,  194,    0,  342,  422,  536],
    [ 468, 1016,  788, 1164, 1050,  514,  514,  662,  320,  274,  388,  650,  536,  342,    0,  764,  194],
    [ 776,  868, 1552,  560,  674, 1050, 1278,  742, 1084,  810, 1152,  274,  388,  422,  764,    0,  798],
    [ 662, 1210,  754, 1358, 1244,  708,  480,  856,  514,  468,  354,  844,  730,  536,  194,  798,    0],
] 

def get_total_distance(tour):
    
    total_distance = 0

    for i in range(n_cities - 1):
        total_distance += distances[tour[i]][tour[i+1]]

    # tour[-1]: pega o último elemento (-2 pega o 2º último e por assim vai)
    total_distance += distances[tour[-1]][tour[0]]

    return total_distance

# esta função gera a vizinhança utilizando um operador de busca local chamado SWAP
def get_neighbors(current_solution):

    # estamos criando uma cópia dessa variável com endereços de memória diferentes uma da outra mas com valores iguais
    neighbor_solution = copy.deepcopy(current_solution)
    i, j = random.sample(range(n_cities), 2)
    neighbor_solution[i], neighbor_solution[j] = neighbor_solution[j], neighbor_solution[i]

    return neighbor_solution

# alpha: constante de decaimento da temperatura no intervalo [0, 1]
# initial_temperature: temperatura inicial > 0
# maximum_iterations: número máximo de iterações do algoritmo
def annealing(alpha, initial_temperature, maximum_iterations):
    # criar algo para controlar o decaimento da temperatura
    current_temperature = initial_temperature
    
    # criar uma solução inicial ou "chute" inicial
    # (a) heurística aleatória
    # (b) heurística gulosa
    current_solution = random.sample(range(n_cities), n_cities)
    
    # explorará o espaço de soluções por maximum_iterations
    # while current_temperature >= 0.0:
    for k in range(maximum_iterations):
        
        # construir a vizinhança de current_solution e escolher uma delas
        neighbor_solution = get_neighbors(current_solution)

        # calcular diferença entre o valor da função objetivo da solução vizinha escolhida e a solução atual
        delta = get_total_distance(current_solution) - get_total_distance(neighbor_solution)

        # delta == 0: solução atual é igual a solução vizinha escolhida
        # delta < 0: solução atual é melhor que a solução vizinha escolhida
        # delta > 0: solução vizinha escolhida é melhor que a solução atual
        if delta > 0:
            current_solution = neighbor_solution
        # até a linha de cima, temos o algoritmo do hill climbing
        else:
            if random.uniform(0,1) < math.exp(-delta / current_temperature):
                current_solution = neighbor_solution

        # current_temperature = current_temperature - alpha
        current_temperature = alpha * current_temperature
