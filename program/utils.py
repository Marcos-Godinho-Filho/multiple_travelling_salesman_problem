from typing import List
from entities.city import City
from math import sqrt

def total_distance_individual(tours: List[List[int]], distances: List[List[int]]):
    total_distance = 0

    for tour in tours:
        for i in range(len(tour) - 1):
            origin = tour[i]
            destination = tour[i+1]
            total_distance += distances[origin][destination]

    return total_distance

def distance_between_cities (first: City, second: City):
    return int(sqrt((second.x - first.x) ** 2 + (second.y - first.y) ** 2))
