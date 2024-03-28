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
    
    # connects every city to centroid
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
    
    # Starting from the nearest to centroid
    fully_connected_cities = []
    for city in cities_clone:
        # counts connections to this city, in order not to create more than 3 connections
        number_of_connections = count_connections_to_city(city.id, n_cities, polygon_connections)

        if number_of_connections == 3 and city not in fully_connected_cities:
            fully_connected_cities.append(city)

        # 3 connections = 2 between cities and 1 to centroid
        elif number_of_connections < 3:

            # This for loop will iterate through the cities near to centroid. From nearest to farthest
            nearest_cities = cities_clone.copy()
            nearest_cities.sort(key = lambda other_city: distances[other_city.id][city.id])
            # removes city not to create a connection to itself
            nearest_cities.remove(city)
        
            for nearest_city in nearest_cities:
                # This for loop will iterate through the cities near to city. It's important because being the
                # nearest city does not mean the connection will be created, since that may be a intersection.

                # counts connections to nearest city, in order not to create more than 3 connections
                if not nearest_city in fully_connected_cities: 
                    if len(fully_connected_cities) == n_cities - 3:
                        polygon_connections[city.id][nearest_city.id] = 1
                        polygon_connections[nearest_city.id][city.id] = 1
                        number_of_connections += 1
                    else:
                        # Here we have 2 of the 4 points needed to check an intersection:
                        # 1 - The nearest city (C) to centroid
                        # 2 - The nearest city (c) to C
                        # Obs: nearest city must not be fully connnected yet, otherwise cycles would be created
                        remaining_cities = nearest_cities.copy()
                        # remove nearest city in order to, when iterating through the remaining cities, this one not be
                        # considered, since it would be check the insersection: Cc - ccentroid, which is nearest city itself (an angle is formed)
                        remaining_cities.remove(nearest_city)

                        # Check whether there is a intersection between: C - c and any remainin_city - centroid
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
                            # if a cycle is found between far_city and nearest_city, that means they cannot be connected

                            # if going back to the previous city (that not the centroid), and any time arrives at nearest city, 
                            # that means a cycle would be created
                            is_cycle = is_end = False
                            current = city.id
                            already_visited = [current]
                            # while doesn't reach the end of cities or untill doesn't find a cycle
                            while not is_end and not is_cycle:
                                con = polygon_connections[current]
                                for i in range(n_cities):
                                    if con[i] == 1 and i != centroid_index and i not in already_visited:
                                        # goes to the first connection it finds
                                        current = i
                                        already_visited.append(current)
                                        break
                                    # reached the end of cities
                                    elif i == n_cities - 1:
                                        is_end = True
                                        break
                                # the second condition checks if we are not in that last - first city case
                                if current == nearest_city.id and len(already_visited) != n_cities - 1:
                                    # if we're not in the end, but somehow got to the nearest city starting from city,
                                    # that means that, if the connection was made, it would have a cycle
                                    is_cycle = True
                    
                            if not is_cycle:
                                polygon_connections[city.id][nearest_city.id] = 1
                                polygon_connections[nearest_city.id][city.id] = 1
                                number_of_connections += 1
                    
                    if number_of_connections == 3:
                        fully_connected_cities.append(city)
                        break

    print(len(fully_connected_cities))

    return polygon_connections


def split_path_between_salesmen(N: int, M: int, polygon_connections: List[List[int]], distances: List[List[int]], centroid: City):
    tours: List[List[int]] = list()
    
    # aproximate number of cities to be visited by each salesman
    # N - 1 because we disconsider the centroid
    cities_per_salesman = int((N-1)/M)
    # rest will be helpful for handling the last salesman
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

    # N/M might not be exact and some cities might be missing because of the division. Therefore, the last salesman, will travel
    # cities_per_salesman cities AND those remaining. E.g: 16 / 3 = 5 and rest 1. The last salesman will travel 5 + 1 = 6 cities.
    # Because of this, he'll be handled separately
    for salesman in range(M):
        # i = salesman index
        for j in range(cities_per_salesman):
            # j = Nth city the saleman must visit
            con = polygon_connections[current]
            for k in range(N):
                # k = iterate through connected cities to jth city
                if con[k] == 1 and k not in already_visited and k != centroid.id:
                    current = k
                    break
            # The Ith tour will receive the city we are now, and it'll be considered visited
            tours[salesman].append(current)
            already_visited.append(current)
        
        if salesman == M - 1:
            # last salesman travels the number of cities he was supposed to visit + remaining cities
            for i in range(rest):
                con = polygon_connections[current]
                for j in range(N):
                    if con[j] == 1 and j not in already_visited and j != centroid.id:
                        current = j
                        break
                tours[salesman].append(current)
                already_visited.append(current)

        # by the end of the tour, when the salesman finishes travelling through the cities he is supposed to, he must go back to centroid    
        tours[salesman].append(centroid.id)

    return tours


def walk_through_tours(tours: list[list[int]], distances: list[list[int]]):
    total_distance = 0

    for tour in tours:
        for i in range(len(tour) - 1):
            origin = tour[i]
            destination = tour[i+1]
            total_distance += distances[origin][destination]
    
    return total_distance
