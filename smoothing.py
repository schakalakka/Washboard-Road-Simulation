import numpy as np

from road import Road
from wheel import Wheel
import sys
from utils import print_road_surface

# Idea: pass as maxh the current maximum height of the road
def wind_smoothing(road: Road, maxh: int):
    """
    Global max/wind smoothing function.
    Takes all the grains above a threshold maxh and puts them to the lowest heights (globally).
    This methods puts the grains to the first position with the lowest height.
    :param road: Road class instance
    :param maxh: positive integer, threshold value, above this value all grains are removed
    :return:
    """
    while max(road) > maxh:
        for i in range(road.size):
            if road[i] > maxh:
                temp_minimum = min(road)
                for j in range(road.size):
                    if road[j] == temp_minimum:
                        road.remove_grain(i)
                        road.add_grain(j)
                        break


def random_wind_smoothing(road: Road, maxh: int):
    """
    Global max/wind smoothing function similar to wind_smoothing.
    The difference is that the grains are randomly distributed over all lowest positions with the lowest height
    and not to the first position in the road with the lowest height.
    :param road: Road class instance
    :param maxh: positive integer, threshold value, above this value all grains are removed
    :return:
    """
    while max(road) > maxh:
        for i in range(road.size):
            if road[i] > maxh:
                temp_minimum = min(road)
                temp_minimum_indices = np.where(road.piles == temp_minimum)
                chosen_index = np.random.choice(temp_minimum_indices[0])
                road.remove_grain(i)
                road.add_grain(chosen_index)


def max_smoothing(road: Road, maxh: int):
    """
    Local max smoothing method. Takes all the grains above a certain threshold and puts them onto
    neighbouring lower positions.
    :param road: Road class instance
    :param maxh: positive integer, threshold value, above this value all grains are removed
    :return:
    """
    # maxh = 7
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
    """
    Pairwise comparison of neighbouring elements in the road.
    If their height difference is bigger than one they grains from the bigger one are removed
    and put on the lower position.
    :param road: Road class
    :return:
    """
    for i in range(road.size):
        i2 = (i + 1) % road.size
        height1 = road[i]
        height2 = road[i2]
        diff = height1 - height2
        if diff > 1:
            road.add_grain(i2)
            road.remove_grain(i)
        elif diff < -1:
            road.add_grain(i)
            road.remove_grain(i2)


def general_slope_smoothing(road: Road, slope_inverse=3):
    """
    TODO DOES NOT WORK YET
    General slope smoothing function with an aimed slope of 1/slope_inverse for the heapes.
    I.e. if slope_inverse=3 the heaps should a an incline of 1/3.
    :param road: Road class instance
    :param slope_inverse: positive integer, define the slope as 1/slope_inverse
    :return:
    """
    if slope_inverse < 1:  # do nothing if the slope is not a positive integer
        return
    for i in range(0, road.size, slope_inverse):
        end_segm_slice_point = i + 2 * slope_inverse
        sum_over_next_segment = np.sum(road.piles[i:end_segm_slice_point])
        average_over_next_segment = sum_over_next_segment / (2 * slope_inverse)
        average_floor_int = int(average_over_next_segment)
        start_segm_height = road[i]
        end_segm_index = end_segm_slice_point - 1
        end_segm_height = road.piles[end_segm_index]
        road.piles[i:end_segm_slice_point] = average_floor_int

        rest_to_distribute = sum_over_next_segment - average_floor_int * 2 * slope_inverse
        if start_segm_height == end_segm_height:
            if rest_to_distribute > 0:
                road.add_random_irregularities(rest_to_distribute, (i, end_segm_slice_point))
        elif start_segm_height < end_segm_height:
            if rest_to_distribute == 0:
                road.remove_grain(start_segm_height)
                road.add_grain(end_segm_height)
            else:
                k = int(rest_to_distribute / 3)
                road.add_grains(range(end_segm_slice_point - k, end_segm_slice_point), [2] * k)
                rest_to_distribute -= 2 * k
                road.add_grains(range(end_segm_slice_point - k - rest_to_distribute, end_segm_slice_point - k),
                                [1] * rest_to_distribute)
        elif start_segm_height > end_segm_height:
            if rest_to_distribute == 0:
                road.add_grain(start_segm_height)
                road.remove_grain(end_segm_height)
            else:
                k = int(rest_to_distribute / 3)
                road.add_grains(range(i, i + k), [2] * k)
                rest_to_distribute -= 2 * k
                road.add_grains(range(i + k, i + k + rest_to_distribute), [1] * rest_to_distribute)


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
    if len(args) != 3:
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

def smoothing_strategy3(road: Road, wheel: Wheel, args: list):
    if len(args) != 4:
        print('Error: incorrect number of arguments in smoothing_strategy3')
        sys.exit()
    h_max = args[0]
    iterations = args[1]
    increment_h_max_wind = args[2] #At least value equal to 1
    lower_bound_h_max_wind = args[3] #Our defaults: 1 or 2
    max_smoothing(road, h_max)

    for i in range(iterations):
         slope_smoothing(road)

    h_max_road = max(road.piles)
    h_max_wind = max(h_max_road - increment_h_max_wind, road.height+lower_bound_h_max_wind)
    random_wind_smoothing(road, h_max_wind)



def smoothing(road: Road, wheel: Wheel, method: str, smoothing_args: list):
    """
    @TO DO THE SAME FORMAT AS digging.py, this would be the general function and then we
    can consider sub-smoothing procedures. This one would be one procedure, for example --->
    :param iterations:
    :param road:
    :return:
    """
    if method == 'strategy 1':
        return smoothing_strategy1(road, wheel, smoothing_args)
    elif method == 'strategy 2':
        return smoothing_strategy2(road, wheel, smoothing_args)
    elif method == 'strategy 3':
        return smoothing_strategy3(road, wheel, smoothing_args)
    else:
        print("Using default smoothing strategy 1.")
        return smoothing_strategy1(road, wheel, smoothing_args)

    # print("Before doing smoothing")
    # print_road_surface(road, wheel.xf, wheel.diameter)
    # max_smoothing(road, (road.height+5) )
    # print_road_surface(road, wheel.xf, wheel.diameter)

# for i in range(iterations):
#      slope_smoothing(road)
# max_smoothing(road, (road.height+2) )
# random_wind_smoothing(road, (road.height+2) )
# print("after doing smoothing")
# print_road_surface(road, wheel.xf, wheel.diameter)
# print("end smoothing iter")
