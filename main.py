from typing import List
from entities.city import City
from external import *
from math import sqrt
import random
import matplotlib.pyplot as plt


def distance_between_cities (first: City, second: City):
    return int(sqrt((second.x - first.x) ** 2 + (second.y - first.y) ** 2))


def count_connections_to_city (city_id: int, n_cities: int, polygon_connections: List[List[int]]):
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


def draw_polygon (centroid: City, n_cities: int, cities: List[City], polygon: List[List[int]]):
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


def create_polygon (n_cities: int, distances: List[List[int]], cities: List[City], centroid: City) -> List[List[int]]:

    # represents the connection between cities
    polygon_connections = [[0 for _ in range(0, n_cities)] for _ in range(0, n_cities)]
    
    # TODO:
    # [x] Create connections from centroid to all cities
    centroid_index = cities.index(centroid)
    for i in range(n_cities):
        city = cities[i]
        if city != centroid:
            polygon_connections[i][centroid_index] = 1
            polygon_connections[centroid_index][i] = 1
    
    
    # sort cities from the nearest to the farthest city from centroid
    cities_clone = cities.copy()
    cities_clone.sort(key = lambda city: distances[centroid_index][city.id])
    cities_clone.remove(centroid)
    print(cities_clone)
    
    # [] Starting from the nearest to centroid (city C):
    #   [x] Get n nearest cities to C (c)
    fully_connected_cities = []
    for city in cities_clone:
        # This for loop will iterate through the cities near to centroid. From nearest to farthest
        nearest_cities = cities_clone.copy()
        nearest_cities.sort(key = lambda other_city: distances[other_city.id][city.id])
        nearest_cities.remove(city)

        number_of_connections = count_connections_to_city(city.id, n_cities, polygon_connections)

        # 3 connections = 2 between cities and 1 to centroid
        if number_of_connections < 3:
            for nearest_city in nearest_cities:
                if count_connections_to_city(nearest_city.id, n_cities, polygon_connections) < 3 and not nearest_city in fully_connected_cities: 
                    # This for loop will iterate through the cities near to city. It's important because being the
                    # nearest city does not mean the connection will be created, since that may be a intersection.
                    # Here we have 2 of the 4 points needed to check an intersection:
                    # 1 - The nearest city (C) to centroid
                    # 2 - The nearest city (c) to C
                    # Obs: nearest city must not be fully connnected yet, otherwise cycles would be created
                    remaining_cities = nearest_cities.copy()
                    remaining_cities.remove(nearest_city)


                    # [x] Check whether there is a intersection between: C - c and any city - centroid
                    for remaining_city in remaining_cities:
                        # This for loop will iterate through the remaining cities (that not the centroid, city C and city c)
                        # Here we have the remaing 2 points needed to check an intersection:
                        # 3 - Any other city
                        # 4 - The centroid
                        has_intersection = intersect(city, nearest_city, remaining_city, centroid)
                        # [x] if there is any intersection, stop and check the next nearest city
                        if has_intersection:
                            break
                    else:
                        # [] Verify cycles
                        
                        # if no cycle was found between far_city and nearest_city, that means they can 
                        # be connected without creating a cycle

                        is_cycle = False
                        con = polygon_connections[city.id]
                        previous_ix = 0
                        for i in range(n_cities):
                            if con[i] == 1:
                                previous_ix = i
                        con = polygon_connections[previous_ix]
                        previous_previous_ix = 0
                        for i in range(n_cities):
                            if con[i] == 1 and i != previous_ix:
                                previous_previous_ix = i
                        if previous_previous_ix == nearest_city:
                            is_cycle = True
                
                        if not is_cycle:
                            # [x] Otherwise, create connections (each city must have 3 connections)
                            polygon_connections[city.id][nearest_city.id] = 1
                            polygon_connections[nearest_city.id][city.id] = 1
                            number_of_connections += 1
                    
                    if number_of_connections == 3: # between cities
                        fully_connected_cities.append(city)
                        break
    
    draw_polygon(centroid, n_cities, cities, polygon_connections)

    return polygon_connections


p = create_polygon(n_cities, distances, cities, centroid)
p.sort()

def split_path_between_salesmen(N: int, M: int, polygon_connections: List[List[int]], distances: List[List[int]], centroid: City):
    tours: List[List[int]] = list()
    
    # aproximate number of cities to be visited by each salesman
    cities_per_salesman = int(N/M)

    already_visited = list()

    # gets the nearest city to centroid
    distances_to_centroid = distances[centroid.id]
    current = distances_to_centroid.index(min(distances_to_centroid))

    n_already_visited_by_one_salesman = 0
    salesman_ix = 0

    for i in range(M):
        # each salesman will always start from centroid
        tours.append([centroid.id])

    # inits by travelling from centroid to nearest city to centroid 
    tours[salesman_ix].append(current)

    for i in range(N - 1):
        cons_to_current = polygon_connections[current]
        # iterates through the connections to current city
        for j in range(N):
            # if it finds a connection that has not been visited and is not the centroid
            if cons_to_current[j] == 1 and j not in already_visited and j != centroid.id:
                current = i
                tours[salesman_ix].append(i)

        # if number of cities visited == X, comes back to centroid, switches travelling salesman, leaves centroid and goes to next city 
        n_already_visited_by_one_salesman += 1
        if n_already_visited_by_one_salesman == cities_per_salesman:
            # if reached supposed last city and there is still a city to be visited
            if i == N - 2:
                tours[salesman_ix].append(current)
                continue
            # each salesman will always go back to centroid after going to cities_per_salesman cities
            tours[salesman_ix].append(centroid.id)
            # new salesman
            n_already_visited_by_one_salesman = 0
            salesman_ix += 1
            tours[salesman_ix].append(current)

    # the last salesman must also go back to centroid
    tours[salesman_ix].append(centroid.id)

    return tours


def draw_solution(tours: List[List[int]], cities: List[City]):
    plt.clf()

    # for edge in polygon:
    #   print(str(edge.origin.id) + "," + str(edge.destination.id))
    #    plt.plot([edge.origin.x, edge.destination.x], [edge.origin.y, edge.destination.y], marker = 'o')

    for t in tours:
        for i in range(len(t) - 1):
            plt.plot([cities[i].x, cities[i+1].x], [cities[i].y, cities[i+1].y], marker = 'o')

    plt.show()