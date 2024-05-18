'''
Lines 16-29 and 49-50:
Copied and modified from: https://chat.openai.com/share/2b7858a6-1524-4892-aadf-7ae3e650aa60

Line 32:
Copied from: https://stackoverflow.com/questions/110362/how-can-i-find-the-current-os-in-python
'''
from entities.city import City
from draw import *
from heuristic import *
from metaheuristic import annealing, genetic_algorithm
from colorama import Fore, Style
import os
import platform
import re


# Read numberic values from instances files
def get_numeric(list):
    primitive = [value.strip() for value in list if re.match(r'^\d+$', value.strip())]
    numerical = [int(value) for value in primitive]
    return numerical


script_directory = os.path.dirname(os.path.abspath(__file__))
instances_directory = os.path.join(script_directory, '..', 'instances')

for filepath in os.listdir(instances_directory):
    filename = os.path.join(instances_directory, filepath)

    if os.path.isfile(filename):
        print("-" * 100)
        print(f"Lendo arquivo: {filename}")

        operational_system = platform.platform().lower()
        # get last "/" section: file name, i.e "mTSP-n12-m1"
        if 'windows' in operational_system:
            primitive = filename.split("\\")[-1]
        else:
            primitive = filename.split("/")[-1]

        n_primitive, m_primitive = primitive.split("-")[1], primitive.split("-")[2] # i.e, n12 and m1
        n = int(n_primitive[1:]) + 1 # n12 has 13 cities. 12 is the last city's index
        m = int(m_primitive[1:])
        print(f"N Cities: {n}")
        print(f"M Salesman: {m}")

        cities: list[City] = []
        distances = [[0 for _ in range(n)] for __ in range(n)]

        with open(filename, 'r') as file:
            for line in file:
                numerical = get_numeric(line.split(" "))
                id, x, y = numerical
                city = City(id, x, y)
                cities.append(city)
        file.close()

        for i in range(n):
            for j in range(i+1, n):
                distances[i][j] = distances[j][i] = distance_between_cities(cities[j], cities[i])

        centroid = find_centroid_city(distances, cities)

        polygon = create_polygon(n, distances, cities, centroid)

        tours = split_path_between_salesmen(n, m, polygon, distances, centroid)
        # print(tours)
        # draw_polygon(centroid, n, cities, polygon)

        heuristic_distance = walk_through_tours(tours, distances)
        print(Fore.LIGHTGREEN_EX + f'[Heurística]: Distância total percorrida: {heuristic_distance}')

        # Simullated Annealing
        simullated_annealing_solution = annealing.annealing(0.95, 10000, 500, tours, n, distances)
        annealing_distance = walk_through_tours(tours, distances)
        # print(simullated_annealing_solution)
        print(Fore.LIGHTCYAN_EX + f'[Simullated Annealing]: Melhor distância total achada: {annealing_distance}')

        # Genetic algorithm
        genetic_solution = genetic_algorithm.main(500, 0.1, 3057, range(n), tours, distances)
        genetic_distance = walk_through_tours(tours, distances)
        # print(simullated_annealing_solution)
        print(Fore.LIGHTMAGENTA_EX + f'[Genetic Algorithm]: Melhor distância total achada: {genetic_distance}')

        # draw_solution(tours, cities)
        input(Fore.LIGHTBLACK_EX + 'Pressione [ENTER] para ir para próxima instância: ')
        print(Fore.RESET)
