'''
Lines 16-29 and 49-50:
Copied and modified from: https://chat.openai.com/share/2b7858a6-1524-4892-aadf-7ae3e650aa60

Line 32:
Copied from: https://stackoverflow.com/questions/110362/how-can-i-find-the-current-os-in-python
'''
from entities.city import City
from typing import List
from draw import *
from utils import *
from metaheuristic import annealing, genetic_algorithm
from colorama import Fore
import time
import heuristic
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

dir = os.listdir(instances_directory)
dir.sort()

for filepath in dir:
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

        cities: List[City] = []
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

        heuristic_solution = heuristic.main(distances, cities, n, m)
        heuristic_distance = calculate_tour_total_distance(heuristic_solution, distances)
        # print(heuristic_solution)
        print(Fore.LIGHTGREEN_EX + f'[Heurística]: Distância total percorrida: {int(heuristic_distance)}')

        # Simulated Annealing
        simulated_annealing_solution = annealing.main(0.95, 1000, 1e-3, heuristic_solution, n, distances, 20)
        annealing_distance = calculate_tour_total_distance(simulated_annealing_solution, distances)
        # print(simulated_annealing_solution)
        print(Fore.LIGHTCYAN_EX + f'[Simulated Annealing]: Melhor distância total achada: {int(annealing_distance)}')
        print(Fore.LIGHTMAGENTA_EX)

        # Genetic algorithm
        genetic_solution = genetic_algorithm.main(100, 0.5, cities, heuristic_solution, 25000, distances)
        genetic_distance = calculate_tour_total_distance(genetic_solution, distances)
        # print(genetic_solution)
        print(f'[Genetic Algorithm]: Melhor distância total achada: {int(genetic_distance)}')

        # input(Fore.LIGHTBLACK_EX + 'Pressione [ENTER] para ir para próxima instância: ')
        print(Fore.RESET)
