import random
import math
import matplotlib.pyplot as plt
from city import City
from connection import Connection


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
#print(cities)
#for l in distances:
#    print(l)


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


def distance_between_cities (first: City, second: City):
    return int(math.sqrt((second.x - first.x) ** 2 + (second.y - first.y) ** 2))


def create_polygon (n_cities: int, distances: list, cities: list[City], centroid: City):
    # sort cities from the farest to the nearest city from centroid
    cities_clone = cities.copy()
    cities_clone.sort(key = lambda city: distance_between_cities(city, centroid), reverse = True)
    # print(cities_clone)
    # TODO: Consider using 'set'

    polygon_edges: list[Connection] = []

    # for each far city from centroid
    while len(cities_clone) > 1:
        far_city = cities_clone.pop(0) # so 2 connections between same cities are created
        # now find the nearest city from that one
        #print(f'Far city: {far_city}')
        #print(cities_clone)
        nearest_city = min(cities_clone, key = lambda city: distance_between_cities(far_city, city))
        #print(f'Near city: {nearest_city}')
        # create connection between cities
        connection = Connection(far_city, nearest_city)
        polygon_edges.append(connection)
    
    return polygon_edges


p = create_polygon(n_cities, distances, cities, centroid)

def draw_polygon (centroid: City, polygon: list[Connection]):
    plt.clf()

    plt.scatter(centroid.x, centroid.y, color='blue')

    for edge in polygon:
        plt.plot([edge.origin.x, edge.destination.x], [edge.origin.y, edge.destination.y], marker = 'o')

    plt.show()

draw_polygon(centroid, p)

# TODO:
    # [x] Draw cities
    # [x] Find centroid city (city that has the lowest sum of distances to every other city)
    # [x] Draw centroid
    # [] Create polygon:
    #   [x] Find farest city
    #   [x] Find nearest city to the previous one
    #   [] Create a connection between both
    # [] Draw polygon
    # [] Each sallesman will travel to one polygon 