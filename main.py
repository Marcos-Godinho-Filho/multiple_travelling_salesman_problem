import random
import math
from city import City


n_cities = 17 # número de cidades

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


def get_total_distance(tour: list):
    '''
    - O tour é uma lista de indices, que são as cidades, representando a ordem em que devem ser visitadas. Ou seja,
    [1, 4, 8, 2, 9, 10, ...] significa cidade 1 -> 4 -> 8 -> 2 -> 9 -> 10 -> ...

    - Obs: O tour NÃO É uma lista da matriz. Uma lista da matriz são as conexões de uma cidade N para todas as demais
    '''

    # computar a distância total percorrida pelo salesman NAQUELE TOUR
    total_distance = 0
    for i in range(n_cities - 1): # -1 pois vamos desconsiderar a ultima cidade do tour, ja que eh um caso especial pois precisamos voltar para a primeira cidade
        # vai somando as distancias: 1ª -> 2ª + 2ª -> 7ª + 7ª -> 3ª + ... + 10ª -> 17ª do tour
        total_distance += distances[tour[i]][tour[i+1]] # ou seja, distancia de uma cidade do tour para a proxima cidade do tours
        '''
        obs: não poderia ser:
        for dist in tour:
            total_distance += dist
        pois, sabendo que todas as cidades têm ligações entre si, isso seria 1ª -> 2ª + 1ª -> 3ª + 1ª -> 4ª + ... + 1 -> 17ª.
        Dessa forma, nao seria o caminho total de um tour, e sim a soma das distancias de uma unica cidade para todas as demais
        '''
    
    # voltar para a primeira cidade, pois estamos atualmente na ultima cidade do tour, ou seja: + 17ª -> 1ª
    total_distance += distances[tour[-1]][tour[0]]

    return total_distance


def nearest_neighbor_heuristic_from_0(distances: list):
    # vai gerar um tour, ou seja, uma sequencia de cidades (indices), sendo que vai ser o menor tour possivel
    tour = [0] # nesse caso em especifico, estamos partindo da primeira cidade
    unvisited = list(range(1, len(distances))) # [1, 2, 3, 4, ...]
    while unvisited:
        '''
        O min vai passar pelos elementos de unvisited e para cada elemento, vai associá-lo ao parâmetro candidate
        da função lambda. Então se calcula a distancia dessa cidade atual para a ultima cidade no tour. Então, se associa
        essa distancia para esse elemento (que é a chave desse valor). Como:
        1 -> 314
        2 -> 817
        3 -> 909
        4 -> 124
        5 -> 599
        ...
        Por fim, escolhe-se o elemento com base na menor distancia. A chave da escolhe é essa distancia
        '''
        next_city = min(unvisited, key = lambda candidate: distances[tour[-1]][candidate])
        tour.append(next_city)
        unvisited.remove(next_city)

    return tour


def nearest_neighbor_heuristic_from_random(distances: list):
    unvisited = list(range(0, len(distances)))
    tour = [random.choice(unvisited)]
    unvisited.remove(tour[-1])

    while unvisited:
        next_city = min(unvisited, key = lambda candidate: distances[tour[-1]][candidate])
        tour.append(next_city)
        unvisited.remove(next_city)

    return tour


def random_nearest_neighbor_heuristic(distances: list):
    unvisited = list(range(0, len(distances)))
    tour = random.sample(unvisited, len(distances) / 2) # samples não devolve os elementos escolhidos para o tour

    for i in range(len(tour)):
        unvisited.remove(tour[i])

    while unvisited:
        next_city = min(unvisited, key = lambda candidate: distances[tour[-1]][candidate])
        tour.append(next_city)
        unvisited.remove(next_city)

    return tour



def distances_from_coordinates(coordinates: list):
    size = len(coordinates)
    
    distances = [[0 for _ in range(size)] for __ in range(size)]
    for first in range(size):
        for second in range(size):
            '''
            distances[first][second] == 0 evita que se façam novos cálculos em uma posição já preenchida,
            já que, ao preencher [0][7] por exemplo, ja iria preencher [7][0]. Caso nao tivesse essa verificacao,
            quando chegasse no [7][0] um novo calculo seria feito.
            '''
            if first != second and distances[first][second] == 0:
                f_coords = coordinates[first]
                s_coords = coordinates[second]
                distance = int(math.sqrt((s_coords[0] - f_coords[0]) ** 2 + (s_coords[1] - f_coords[1]) ** 2))
                distances[first][second] = distances[second][first] = distance

    return distances


def create_random_problem (n_cities: int):
    # create n cities and their coordinates
    cities: list[City] = []
    for _ in range(n_cities):
        x, y = int(random.uniform(0, 1000)), int(random.uniform(0, 1000))
        city = City(x, y)
        cities.append(city)

    # create distances array based on those coordinates
    distances = [[0 for _ in range(n_cities)] for __ in range(n_cities)]
    for i in range(n_cities):
        for j in range(i+1, n_cities):
            distances[i][j] = distances[j][i] = int(math.sqrt((cities[j].x - cities[i].x) ** 2 + (cities[j].y - cities[i].y) ** 2))

    return cities, distances


n_cities = 16
cities, distances = create_random_problem(n_cities)
print(cities)
for l in distances:
    print(l)
