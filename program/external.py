'''
Lines 12 to 19: 
Copied from: https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect

Lines 21-24:
Copied and modified from: https://chat.openai.com/share/2b7858a6-1524-4892-aadf-7ae3e650aa60
'''
from typing import List
import re


# Determines if three points are listed in a counterclockwise order
def ccw(A, B, C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)


# Return true if line segments AB and CD intersect
def intersect(A, B, C, D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


# Read numberic values from instances files
def get_numeric(list):
    primitive = [value.strip() for value in list if re.match(r'^\d+$', value.strip())]
    numerical = [int(value) for value in primitive]
    return numerical