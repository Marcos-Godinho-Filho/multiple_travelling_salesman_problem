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


# code created with help of chat-gpt and based on this article: https://mauricio.resende.info/tttplots/
def calculate_probabilities(n):
    return [(i - 0.5) / n for i in range(1, n + 1)]


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

        # number of iterations for ttt plot
        k = 5
        probabilities = calculate_probabilities(n)

        # Simulated Annealing
        annealing_times = []
        for _ in range(k):
            simulated_annealing_solution, simulated_annealing_time = annealing.main(0.95, 1000, 1e-3, heuristic_solution, n, distances, 20)
            annealing_times.append(simulated_annealing_time)
        annealing_distance = calculate_tour_total_distance(simulated_annealing_solution, distances)
        # print(simulated_annealing_solution)
        print(Fore.LIGHTCYAN_EX + f'[Simulated Annealing]: Melhor distância total achada: {int(annealing_distance)}')
        print(Fore.LIGHTMAGENTA_EX)

        draw_ttt_plot(annealing_times, probabilities, os.path.join('pictures', f'annealing-n{n}-m{m}'))

        # Genetic algorithm
        genetic_times = []
        for _ in range(k):
            genetic_solution, genetic_time = genetic_algorithm.main(100, 0.5, cities, heuristic_solution, 20000, distances)
            genetic_times.append(genetic_time)
        genetic_distance = calculate_tour_total_distance(genetic_solution, distances)
        # print(genetic_solution)
        print(f'[Genetic Algorithm]: Melhor distância total achada: {int(genetic_distance)}')

        draw_ttt_plot(genetic_times, probabilities, os.path.join('pictures', f'genetic-n{n}-m{m}'))

        # input(Fore.LIGHTBLACK_EX + 'Pressione [ENTER] para ir para próxima instância: ')
        print(Fore.RESET)
