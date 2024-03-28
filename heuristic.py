from typing import List
from entities.city import City
from external import *
from math import sqrt
import random


def distance_between_cities (first: City, second: City):
    return sqrt((second.x - first.x) ** 2 + (second.y - first.y) ** 2)


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


def find_centroid_city (distances: list, cities: list):
    centroid_city = min(cities, key = lambda city: sum(distances[city.id]))

    return cities[centroid_city.id]


def create_polygon (n_cities: int, distances: List[List[int]], cities: List[City], centroid: City) -> List[List[int]]:

    # represents the connection between cities
    polygon_connections = [[0 for _ in range(0, n_cities)] for _ in range(0, n_cities)]
    
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
    
    # [] Starting from the nearest to centroid (city C):
    #   [x] Get n nearest cities to C (c)
    fully_connected_cities = []
    for ix, city in enumerate(cities_clone):
        # This for loop will iterate through the cities near to centroid. From nearest to farthest
        nearest_cities = cities_clone.copy()
        nearest_cities.sort(key = lambda other_city: distances[other_city.id][city.id])
        nearest_cities.remove(city)

        number_of_connections = count_connections_to_city(city.id, n_cities, polygon_connections)

        # 3 connections = 2 between cities and 1 to centroid
        if number_of_connections < 3:
            for nearest_city in nearest_cities:
                if count_connections_to_city(nearest_city.id, n_cities, polygon_connections) < 3 and not nearest_city in fully_connected_cities: 
                    if ix == n_cities - 1:
                        polygon_connections[city.id][nearest_city.id] = 1
                        polygon_connections[nearest_city.id][city.id] = 1
                        number_of_connections += 1
                    else:
                         # This for loop will iterate through the cities near to city. It's important because being the
                        # nearest city does not mean the connection will be created, since that may be a intersection.
                        # Here we have 2 of the 4 points needed to check an intersection:
                        # 1 - The nearest city (C) to centroid
                        # 2 - The nearest city (c) to C
                        # Obs: nearest city must not be fully connnected yet, otherwise cycles would be created
                        remaining_cities = nearest_cities.copy()
                        remaining_cities.remove(nearest_city)
                        # Check whether there is a intersection between: C - c and any city - centroid
                        for remaining_city in remaining_cities:
                            # This for loop will iterate through the remaining cities (that not the centroid, city C and city c)
                            # Here we have the remaing 2 points needed to check an intersection:
                            # 3 - Any other city
                            # 4 - The centroid
                            has_intersection = intersect(city, nearest_city, remaining_city, centroid)
                            # if there is any intersection, stop and check the next nearest city
                            if has_intersection:
                                break
                        else:
                        # if no cycle was found between far_city and nearest_city, that means they can 
                        # be connected without creating a cycle
                        
                        # se eu ando para tras da cidade que eu estou, sempre indo da cidade ja conectada fora o centroid, e chego na cidade mais proxima em algum momento, entao um ciclo sera formado
                            is_cycle = False
                            is_end = False
                            current = city.id
                            already_visited = [current]
                            while not is_end and not is_cycle:
                                con = polygon_connections[current]
                                for i in range(n_cities):
                                    if con[i] == 1 and i != centroid_index and i not in already_visited:
                                        current = i
                                        already_visited.append(current)
                                        break
                                    elif i == n_cities - 1:
                                        is_end = True
                                        break
                                if current == nearest_city.id and len(already_visited) != n_cities - 1:
                                    is_cycle = True
                    
                            if not is_cycle:
                                polygon_connections[city.id][nearest_city.id] = 1
                                polygon_connections[nearest_city.id][city.id] = 1
                                number_of_connections += 1
                    
                    if number_of_connections == 3: # between cities
                        fully_connected_cities.append(city)
                        break

    return polygon_connections


def split_path_between_salesmen(N: int, M: int, polygon_connections: List[List[int]], distances: List[List[int]], centroid: City):
    tours: List[List[int]] = list()
    
    # aproximate number of cities to be visited by each salesman
    # N - 1 because we disconsider the centroid
    cities_per_salesman = int((N-1)/M)
    rest = (N - 1) % M

    already_visited = list()

    # gets the nearest city to centroid
    distances_to_centroid = distances[centroid.id]
    current = distances_to_centroid.index(min(distances_to_centroid))

    for i in range(M):
        # each salesman will always start from centroid
        tours.append([centroid.id])

    # inits by travelling from centroid to nearest city to centroid 
    already_visited.append(current)

    # M - 1 because the last salesman usually travels more than the others
    for i in range(M - 1):
        for j in range(cities_per_salesman):
            con = polygon_connections[current]
            for k in range(N):
                if con[k] == 1 and k not in already_visited and k != centroid.id:
                    current = k
                    break
            tours[i].append(current)
            already_visited.append(current)
            
        tours[i].append(centroid.id)
    
    # last salesman travels also remaining cities
    for i in range(cities_per_salesman + rest):
        con = polygon_connections[current]
        for j in range(N):
            if con[j] == 1 and j not in already_visited and j != centroid.id:
                current = j
                break
        tours[M - 1].append(current)
        already_visited.append(current)
        
    tours[M - 1].append(centroid.id)

    return tours

def walk_through_tours(tours: list[list[int]], distances: list[list[int]]):
    total_distance = 0

    for tour in tours:
        for i in range(len(tour) - 1):
            origin = tour[i]
            destination = tour[i+1]
            total_distance += distances[origin][destination]
    
    return total_distance

