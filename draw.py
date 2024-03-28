from typing import List
from entities.city import City
import matplotlib.pyplot as plt


def draw_cities (cities: list, centroid: City):
    plt.clf()

    for i, city in enumerate(cities):
        plt.scatter(city.x, city.y, color='red')
        plt.text(city.x, city.y, f'{i+1}')
    
    plt.scatter(centroid.x, centroid.y, color='blue')

    plt.show()


def draw_polygon (centroid: City, n_cities: int, cities: List[City], polygon: List[List[int]]):
    plt.clf()

    plt.scatter(centroid.x, centroid.y, color='blue')

    for i in range(n_cities):
        plt.text(cities[i].x, cities[i].y, f'{i+1}')
        for j in range(n_cities):
            if polygon[i][j] == 1:
                origin = cities[i]
                destination = cities[j]
                
                color = 'r'
                if i == centroid.id or j == centroid.id:
                    color = 'b'

                plt.plot([origin.x, destination.x], [origin.y, destination.y], color=color, marker='o')

    plt.show()


def draw_solution(tours: List[List[int]], cities: List[City]):
    plt.clf()

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    color = 0

    for tour in tours:  
        for i in range(len(tour) - 1):
            origin = tour[i]
            destination = tour[i+1]
            plt.plot([cities[origin].x, cities[destination].x], [cities[origin].y, cities[destination].y], color=colors[color], marker = 'o')

        color += 1
        if color == 7:
            color = 0

    plt.show()
    