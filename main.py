import random
import math
import matplotlib.pyplot as plt
from city import City


def distance_between_cities (first: City, second: City):
    return int(math.sqrt((second.x - first.x) ** 2 + (second.y - first.y) ** 2))


def count_connections_to_city (city_id: int, n_cities: int, polygon_connections: list[list[int]]):
    # iterate through connections to city
    connections_to_city = polygon_connections[city_id]
    print(connections_to_city)
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
    
    # it'll be used in the next step for connecting not connected edges (it starts with all cities)
    cities_not_fully_connected_yet = cities_clone.copy()
    
    cities_already_popped: list[City] = []

    # for each far city from centroid
    while len(cities_clone) > 1:
        far_city = cities_clone.pop(0)
        cities_already_popped.append(far_city)
        
        # if the farthest city already has 2 connections, the connection
        # cannot be created, since that city is already full of connections
        number_of_connections_to_farthest_city = count_connections_to_city(far_city.id, n_cities, polygon_connections)
        print(f'Far city: {far_city} - Connections: {number_of_connections_to_farthest_city}')
        
        # if the far_city doesn't have 2 connections yet, it means that connections to it still can be created
        if number_of_connections_to_farthest_city < 2:    
            # we'll then get the cities close to far_city
            cities_close_to_far_city = cities.copy()
            cities_close_to_far_city.sort(key = lambda city: distance_between_cities(far_city, city))
            
            # is True when it finds a city to which the connection with far_city can be created
            is_valid = False
            # c will be used to iterate through cities_close_to_far_city. We'll check if th cth close city to far_city has 4 connections,
            # if it does, that city cannot be connected to far_city. If it doesn't have 2 connections yet, that will be the city
            # to be connected to far_city. It must starts with 1, since cities_close_to_far_city[0] is far_city itself, which
            # means that far_city would have a connection to itself.
            c = 1
            # while we don't find a city to connected or if we reach the end of the cities
            while not is_valid and c < n_cities:
                # get cth close city to far_city
                nearest_city = cities_close_to_far_city[c]
                # the idea is to ignore the centroid. The second comparation prevents the creation of cycles
                if nearest_city == centroid or nearest_city in cities_already_popped:
                    c += 1
                    continue

                # now we'll count the connections to the nearest_city and see if far_city can connect to it
                number_of_connections_to_nearest_city = count_connections_to_city(nearest_city.id, n_cities, polygon_connections)
                print(f'{c}th nearest city: {nearest_city} - connections: {number_of_connections_to_nearest_city}')
                
                # if the cth nearest_city is not connected to 2 cities
                if number_of_connections_to_nearest_city < 2:
                    # create connection from far_city to nearest_city
                    polygon_connections[far_city.id][nearest_city.id] = 1
                    polygon_connections[nearest_city.id][far_city.id] = 1
                    
                    # if nearest_city already made 1 connection, now it makes 2. Now 
                    # nearest_city is fully connected
                    if number_of_connections_to_nearest_city == 1:
                        cities_not_fully_connected_yet.remove(nearest_city)
                    # found a city to connect
                    is_valid = True
                # otherwise, if the cth nearest_city have 2 connections, go to the next one
                c += 1
    
    draw_polygon(centroid, n_cities, cities, polygon_connections)
    # # connect cities that still have only 1 connection (edges)
    while len(cities_not_fully_connected_yet) > 1:
        # get the farthest city from the not fully connected ones
        not_fully_connected_far_city = cities_not_fully_connected_yet.pop(0)
        print(f'Far city: {not_fully_connected_far_city}')
        
        # now find the nearest city from that one
        # TODO: Consider using cities_not_fully_connected instead of cities
        cities_close_to_far_city = cities.copy()
        cities_close_to_far_city = sorted(cities_close_to_far_city, key = lambda city: distance_between_cities(not_fully_connected_far_city, city))
        # same logic from the step above: get the cth city near to the not_fully_connected_far_city, check if it is not the centroid,
        # count its connection to see if it's making 2 connections. If it is, go to the cth next city, otherwise, check cycles
        is_valid = False
        c = 1
        while not is_valid:
            nearest_city = cities_close_to_far_city[c]
            if nearest_city == centroid:
                c += 1
                continue

            number_of_connections_to_nearest_city = count_connections_to_city(nearest_city.id, n_cities, polygon_connections)
            
            if number_of_connections_to_nearest_city < 2:
                print(f'Nearest city: {nearest_city}')      
                # if connection being created does not lead to a cycle
                is_cycle = False
                current = not_fully_connected_far_city.id

                i = 0
                cons_to_current = polygon_connections[current]
                already_visited = []
                while i < len(cons_to_current):
                    # this means that there is a connection between far_city and nearest_city, which will
                    # then result in a cycle
                    if i == nearest_city.id:
                        is_cycle = True
                        break
                    
                    if cons_to_current[i] == 1 and not i in already_visited:
                        # we must keep track of the cities already visited in order not to fall into a loop,
                        # by going to city Y then going back to X and so on
                        already_visited.append(current)
                        current = i
                        cons_to_current = polygon_connections[current]
                        i = 0
                    else:
                        i += 1
                
                # if no cycle was found between far_city and nearest_city, that means they can 
                # be connected without creating a cycle
                if not is_cycle:
                    polygon_connections[not_fully_connected_far_city.id][nearest_city.id] = 1
                    is_valid = True
            c += 1
    
    return polygon_connections


p = create_polygon(n_cities, distances, cities, centroid)
p.sort()


draw_polygon(centroid, n_cities, cities, p)

# TODO:
    # [x] Draw cities
    # [x] Find centroid city (city that has the lowest sum of distances to every other city)
    # [x] Draw centroid
    # [] Create polygon:
    #   [x] Find farest city
    #   [x] Find nearest city to the previous one
    #   [X] Create a connection between both
    #   [] Create two connections per city (first and second nearest cities) to see what happens
    #   [] Do cicle creation verification (if a path is going to create a cicle before all the cities except the centroid are connected, don't)
    # [X] Draw polygon
    # [] Each salesman will travel through one path