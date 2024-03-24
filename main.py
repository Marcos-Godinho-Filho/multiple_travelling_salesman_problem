import random
import math
import matplotlib.pyplot as plt
from city import City


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


def draw_cities (cities: list[City], centroid: City):

    plt.clf()

    for i, city in enumerate(cities):
        plt.scatter(city.x, city.y, color='red')
        plt.text(city.x, city.y, f'{i+1}')
    
    plt.scatter(centroid.x, centroid.y, color='blue')

    plt.show()


def find_centroid_city (n_cities: int, distances: list, cities: list[City]):
    centroid_city, centroid_distances = None, float('inf')
    for city in range(n_cities):
        # for each city, calculate sum of distances to every other city
        distances_sum = 0
        for distance in distances[city]: 
            distances_sum += distance

        if distances_sum < centroid_distances:
            centroid_city, centroid_distances = city, distances_sum
    
    return cities[centroid_city]


centroid = find_centroid_city(n_cities, distances, cities)
draw_cities(cities, centroid)


# TODO:
    # [x] Draw cities
    # [x] Find centroid city (city that has the lowest sum of distances to every other city)
    # [x] Draw centroid
    # [] Create polygon
    # [] Each sallesman will travel to one polygon 