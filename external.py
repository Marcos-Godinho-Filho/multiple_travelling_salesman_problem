'''
Lines 12 to 19: 
Copied from: https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect

Lines 22 - 38:
Modification from:
'''
from typing import List
from entities.city import City


# Determines if three points are listed in a counterclockwise order
def ccw(A, B, C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)


# Return true if line segments AB and CD intersect
def intersect(A, B, C, D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


def has_cycle(n_cities: int, cities: List[City], polygon_connections: List[List[int]], start_city: City, end_city: City):
    visited = [False] * n_cities
    stack = [start_city]

    while stack:
        current = stack.pop()

        if visited[start_city.id]:
            return True
        
        visited[start_city.id] = True

        for neighbor in cities:
            if polygon_connections[current.id][neighbor.id] == 1:
                stack.append(neighbor)
    
    return False
