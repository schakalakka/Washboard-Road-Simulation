import numpy as np

from road import Road


def max_smoothing(road: Road):
    pass


def slope_smoothing(road: Road):
    for i in range(road.size):
        i2 = (i+1) % road.size
        height1 = road[i]
        height2 = road[i2]
        diff = height1 - height2
        if diff > 1:
            road.add_grain(i2)
            road.remove_grain(i)
        elif diff < -1:
            road.add_grain(i)
            road.remove_grain(i2)
