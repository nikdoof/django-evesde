from math import sqrt


def euclidean_distance(origin, destination):
    """Calculates the Euclidean distance of two sets of x/y/z tuples"""
    return sqrt(sum((a - b)**2 for a, b in zip(origin, destination)))
