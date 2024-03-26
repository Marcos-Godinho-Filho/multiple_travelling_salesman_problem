import random
import math
import matplotlib.pyplot as plt
from city import City


def distance_between_cities (first: City, second: City):
    return int(math.sqrt((second.x - first.x) ** 2 + (second.y - first.y) ** 2))


def count_connections_to_city (city_id: int, n_cities: int, polygon_connections: list[list[int]]):
    # iterate through connections to city
    connections_to_city = polygon_connections[city_id]
    n_connections = 0
    for i in range(n_cities):
        # if there is any connection
        if connections_to_city[i] == 1:
            n_connections += 1

    return n_connections


def create_random_problem (n_cities: int):
    # create n cities and their coordinates
    cities: list[City] = []
    for i in range(n_cities):
        x, y = int(random.uniform(0, 1000)), int(random.uniform(0, 1000))
        city = City(i, x, y)
        cities.append(city)

    # create distances array based on those coordinates
    distances = [[0 for _ in range(n_cities)] for __ in range(n_cities)]
    for i in range(n_cities):
        for j in range(i+1, n_cities):
            distances[i][j] = distances[j][i] = distance_between_cities(cities[j], cities[i])

    return cities, distances


n_cities = 16
cities, distances = create_random_problem(n_cities)
#print(cities)
#for l in distances:
#    print(l)


def draw_cities (cities: list, centroid: City):
    plt.clf()

    for i, city in enumerate(cities):
        plt.scatter(city.x, city.y, color='red')
        plt.text(city.x, city.y, f'{i+1}')
    
    plt.scatter(centroid.x, centroid.y, color='blue')

    plt.show()


def find_centroid_city (n_cities: int, distances: list, cities: list):
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


def draw_polygon (centroid: City, n_cities: int, cities: list[City], polygon: list[list[int]]):
    plt.clf()

    plt.scatter(centroid.x, centroid.y, color='blue')

    # for edge in polygon:
    #   print(str(edge.origin.id) + "," + str(edge.destination.id))
    #    plt.plot([edge.origin.x, edge.destination.x], [edge.origin.y, edge.destination.y], marker = 'o')

    for i in range(n_cities):
        for j in range(n_cities):
            if polygon[i][j] == 1:
                origin = cities[i]
                destination = cities[j]

                plt.plot([origin.x, destination.x], [origin.y, destination.y], marker = 'o')

    plt.show()


def create_polygon (n_cities: int, distances: list, cities: list, centroid: City) -> list[list[int]]:
    # sort cities from the farest to the nearest city from centroid
    cities_clone = cities.copy()
    # TODO: Use distances matrix
    cities_clone.sort(key = lambda city: distance_between_cities(city, centroid), reverse = True)

    # represents the connection between cities
    polygon_connections = [[0 for _ in range(0, n_cities)] for _ in range(0, n_cities)]
    
    # TODO:
    # [] Create connections from centroid to all cities
    # [] Starting from the nearest to centroid (city C):
    #   [] Get n nearest cities to C (c)
    #   [] Check whether there is a intersection between: C - c and any city - centroid
    #   [] If there is, move to next one
    #   [] Otherwise, create connections (each city must have 3 connections)
    # [] From starting point (centroid in the first case), go to nearest city, and move N / M cities, then go back to starting point (centroid in the first case): this will be the salesmen travel
    
    
    draw_polygon(centroid, n_cities, cities, polygon_connections)

    return polygon_connections


p = create_polygon(n_cities, distances, cities, centroid)
p.sort()


draw_polygon(centroid, n_cities, cities, p)
