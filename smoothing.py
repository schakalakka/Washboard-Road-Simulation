import numpy as np

from road import Road
from wheel import Wheel
from utils import print_road_surface
import random
import sys

#Idea: pass as maxh the current maximum height of the road
def wind_smoothing(road: Road, maxh: int):
    while max(road) > maxh:
        for i in range(road.size):
            if road[i] > maxh:
                temp_minimum=min(road)
                for j in range(road.size):
                    if road[j] == temp_minimum:
                        road.remove_grain(i)
                        road.add_grain(j)
                        break

def random_wind_smoothing(road: Road, maxh: int):
    while max(road) > maxh:
        for i in range(road.size):
            if road[i] > maxh:
                temp_minimum=min(road)
                temp_minimum_indices = np.where(road.piles == temp_minimum)
                chosen_index = np.random.choice(temp_minimum_indices[0])
                road.remove_grain(i)
                road.add_grain(chosen_index)


def max_smoothing(road: Road, maxh: int):
    #maxh = 7
    while max(road) > maxh:
        for i in range(road.size):
            if road[i] > maxh:
                for n in range(1, road.size):
                    right = (i + n) % road.size
                    left = (i - n) % road.size
                    rightr = road[right]
                    leftr = road[left]
                    if rightr < leftr and rightr < maxh:
                        road.add_grain(right)
                        road.remove_grain(i)
                        break
                    elif rightr > leftr and leftr < maxh:
                        road.add_grain(left)
                        road.remove_grain(i)
                        break
                    elif rightr == leftr and rightr < maxh:
                        uniran = np.random.uniform(0, 1)
                        if uniran >= 0.5:
                            road.add_grain(right)
                            road.remove_grain(i)
                            break
                        else:
                            road.add_grain(left)
                            road.remove_grain(i)
                            break


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

def smoothing_strategy1(road: Road, wheel: Wheel, args: list):
    if len(args) != 2:
        print('Error: incorrect number of arguments in smoothing_strategy1')
        sys.exit()
    h_max = args[0]
    iterations = args[1]

    max_smoothing(road, h_max)
    # print_road_surface(road, wheel.xf, wheel.diameter)

    for i in range(iterations):
         slope_smoothing(road)
    # max_smoothing(road, (road.height+2) )

def smoothing_strategy2(road: Road, wheel: Wheel, args: list):
    if len(args) != 2:
        print('Error: incorrect number of arguments in smoothing_strategy2')
        sys.exit()
    h_max = args[0]
    iterations = args[1]
    h_max_wind = args[2]

    max_smoothing(road, h_max)
    # print_road_surface(road, wheel.xf, wheel.diameter)

    for i in range(iterations):
         slope_smoothing(road)

    random_wind_smoothing(road, h_max_wind)



def smoothing(road: Road, wheel: Wheel,  method: str,  smoothing_args: list ):
    """
    @TO DO THE SAME FORMAT AS digging.py, this would be the general function and then we
    can consider sub-smoothing procedures. This one would be one procedure, for example --->
    :param iterations:
    :param road:
    :return:
    """
    if method == 'strategy 1':
        return smoothing_strategy1(road, wheel, smoothing_args)
    if method == 'strategy 2':
        return smoothing_strategy2(road, wheel, smoothing_args)
    else:
        print("Using default smoothing strategy 1.")
        return smoothing_strategy1(road, wheel, smoothing_args)

    #print("Before doing smoothing")
    #print_road_surface(road, wheel.xf, wheel.diameter)
    #max_smoothing(road, (road.height+5) )
    #print_road_surface(road, wheel.xf, wheel.diameter)

   # for i in range(iterations):
   #      slope_smoothing(road)
    #max_smoothing(road, (road.height+2) )
    #random_wind_smoothing(road, (road.height+2) )
    #print("after doing smoothing")
    #print_road_surface(road, wheel.xf, wheel.diameter)
    #print("end smoothing iter")











