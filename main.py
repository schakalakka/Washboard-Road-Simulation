# from typing import Tuple

from road import Road
from wheel import Wheel
import numpy as np
import sys

from digging import *
from smoothing import *
import utils
import bump


def wheel_pass(road: bump.Road, wheel: bump.Wheel, max_iterations: int, bump_method: str, dig_method: str, dig_probability_arguments: list):
    """
     This function performs a loop of wheel passes through a road until 'max_iterations'
     wheel passes have been performed. The successive wheel passes modify the road surface.

    :param road: a Road
    :param wheel: a Wheel
    :param max_iterations: maximum number of wheel passes (iterations)
    :param bump_method: str, method name for the 'determine_bump_height' function
    :param dig_method: str, method name for the 'digging' function
    """
    current_passes = 0
    while wheel.number_of_passes < max_iterations:
        if current_passes < wheel.number_of_passes:
            utils.smoothing(road, wheel, 5)
            current_passes = wheel.number_of_passes
        initial_position = wheel.xf
        bump_position = wheel.move_to_next_bump(road)
        bump_height = bump.determine_bump_height(road, wheel, bump_position, method=bump_method)
        wheel.jump(road, bump_height)

        utils.digging(road, wheel, wheel.xf, method=dig_method, dig_probability_args = dig_probability_arguments)

        wheel.update_position(wheel.diameter)
        wheel.set_elevation(road.piles[wheel.xf])

        final_position = wheel.xf
        if final_position <= initial_position:
            utils.smoothing(road, wheel, 5)
            wheel.number_of_passes += 1
            print(f'\nIteration number {wheel.number_of_passes}')
            print(
                f'The number of grains is {road.get_number_of_grains()}, the initial was {road.initial_number_of_grains}\n')
            utils.print_road_surface(road, wheel.xf, wheel.diameter)

def wheel_pass_debugging(road: bump.Road, wheel: bump.Wheel, max_iterations: int, bump_method: str, dig_method: str, dig_probability_arguments: list):
    """
     This function performs a loop of wheel passes through a road until 'max_iterations'
     wheel passes have been performed. The successive wheel passes modify the road surface.

    :param road: a Road
    :param wheel: a Wheel
    :param max_iterations: maximum number of wheel passes (iterations)
    :param bump_method: str, method name for the 'determine_bump_height' function
    :param dig_method: str, method name for the 'digging' function
    """
    current_passes = 0
    while wheel.number_of_passes < max_iterations:
        if current_passes < wheel.number_of_passes:
            utils.smoothing(road, wheel, 5)
            current_passes = wheel.number_of_passes
        initial_position = wheel.xf

        utils.print_road_surface(road, wheel.xf, wheel.diameter)

        bump_position = wheel.move_to_next_bump(road)
        bump_height = bump.determine_bump_height(road, wheel, bump_position, method=bump_method)

        utils.print_road_surface(road, wheel.xf, wheel.diameter)

        wheel.jump(road, bump_height)

        utils.print_road_surface(road, wheel.xf, wheel.diameter)

        utils.digging(road, wheel, wheel.xf, method=dig_method, dig_probability_args = dig_probability_arguments)

        wheel.update_position(wheel.diameter)
        wheel.set_elevation(road.piles[wheel.xf])

        final_position = wheel.xf
        if final_position <= initial_position:
            utils.smoothing(road, wheel, 5)
            wheel.number_of_passes += 1
            print(f'\nIteration number {wheel.number_of_passes}')
            print(
                f'The number of grains is {road.get_number_of_grains()}, the initial was {road.initial_number_of_grains}\n')
            utils.print_road_surface(road, wheel.xf, wheel.diameter)


def main():

    debugging = True  # True

    number_of_wheel_passes = 200  # number of 'vehicles' that pass through the road in the whole simulation
    road_size = 100  # length of the road
    standard_height = 10  # standard height or initial height of the road
    nr_of_irregular_points = 20  # number of irregularities for the Road.add_random_irregularities function
    wheel_size = 6  # (Initial) wheel diameter
    velocity = 5  # Proportionality constant to jump (BETA) 2

    # Initialization of a Road, road, and a Wheel, wheel.
    #road = Road(road_size, standard_height, 'specific', list([4, 40]), list([1, 1]))
    #random.seed(2)
    road = bump.Road(road_size, standard_height, 'random', list([None]), list([nr_of_irregular_points]))
    wheel = bump.Wheel(wheel_size, 0, standard_height, velocity, road.size)

    # Dig method
    dig_method = 'backwards tailed exponential'
    constant_probability = 1
    h0 = road.height
    alpha = 1

    if (dig_method == 'backwards tailed exponential') | (dig_method == 'backwards non-tailed exponential'):
        dig_probability_args = list([h0, alpha])
    elif dig_method == 'backwards uniform':
        dig_probability_args = list([constant_probability])
    elif dig_method == 'backwards quadratic':
        dig_probability_args = list([h0])
    else:
        print('The digging method name is not valid')
        utils.sys.exit()


    # Print the initial road-wheel configuration
    utils.print_road_surface(road, wheel.xf, wheel.diameter)
    # Perform the wheel passes
    if debugging is False:
        utils.wheel_pass(road, wheel, number_of_wheel_passes, 'max', dig_method, dig_probability_args)
    else:
        utils.wheel_pass_debugging(road, wheel, number_of_wheel_passes, 'max', dig_method, dig_probability_args)


    #save_road(road, 'test_road1.pkl')

    utils.print_road_surface(road, wheel.xf, wheel.diameter)

    print("\nThe simulation has finished...\n")
    #road_read = read_road('test_road1.pkl')

   #print(road_read.piles)
    utils.plot_road(road)


if __name__ == '__main__':
    main()
