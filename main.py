from functions import *

n_cities = 16
m_salesman = 2
cities, distances = create_random_problem(n_cities)
#print(cities)
#for l in distances:
#    print(l)

centroid = find_centroid_city(n_cities, distances, cities)
draw_cities(cities, centroid)

polygon = create_polygon(n_cities, distances, cities, centroid)
draw_polygon(centroid, n_cities, cities, polygon)

tours = split_path_between_salesmen(n_cities, m_salesman, polygon, distances, centroid)
print(tours)
draw_solution(tours, cities)

distance = walk_through_tours(tours, distances)
print(distance)