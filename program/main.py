from heuristic import *
from draw import *
from entities.city import City
from external import get_numeric
import os


script_directory = os.path.dirname(os.path.abspath(__file__))
instances_directory = os.path.join(script_directory, '..', 'instances')

for filepath in os.listdir(instances_directory):
    filename = os.path.join(instances_directory, filepath)

    if os.path.isfile(filename):
      print("-" * 100)
      print(f"Lendo arquivo: {filename}")

      primitive = filename.split("/")[-1]
      n_primitive, m_primitive = primitive.split("-")[1], primitive.split("-")[2]
      n = int(n_primitive[1:]) + 1
      m = int(m_primitive[1:])
      print(f"N Cities: {n}")
      print(f"M Salesman: {m}")

      print("-" * 100)

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
      # draw_polygon(centroid, n, cities, polygon)

      distance = walk_through_tours(tours, distances)
      print(f'Distância total percorrida: {distance}')
      
      draw_solution(tours, cities)
