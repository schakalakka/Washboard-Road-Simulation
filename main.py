# from typing import Tuple
import sys

import numpy as np
import pickle
import random
from road import Road
from wheel import Wheel
from smoothing import *
from digging import *
import matplotlib.pyplot as plt

def smoothing(road: Road, wheel: Wheel, iterations=1):
    """
    @TO DO
    :param iterations:
    :param road:
    :return:
    """
    #print_road_surface(road, wheel.xf, wheel.diameter)

    max_smoothing(road, (road.height+5) )
    #print_road_surface(road, wheel.xf, wheel.diameter)

    for i in range(iterations):
         slope_smoothing(road)
    #max_smoothing(road, (road.height+2) )

    #print_road_surface(road, wheel.xf, wheel.diameter)


def move_to_next_bump(road: Road, wheel: Wheel) -> int:
    """
    Given a Road road and a Wheel wheel, this function moves the wheel to the position
    that is just before the next road-bump that the wheel will find.
    :param road: a Road
    :param wheel: a Wheel
    :return: the position (the number of the pile) that is just before the next bump that the wheel will find.
    """
    period = road.size
    pos_count = wheel.xf

    while (pos_count < 2 * period) & (road.piles[pos_count % period] <= wheel.elevation):
        wheel.set_elevation(road.piles[pos_count % period])
        pos_count += 1

    if pos_count > 2 * period:
        print("\nNo next bump found. move_to_next_bump() failed. ",
              "\nThere are no bumps according to the current criteria\n")
        sys.exit()

    # The position that is just before the 'real' bump position is stored in the bump_position variable
    bump_position = (pos_count % period) - 1

    # Update the wheel's position
    wheel.set_xf(bump_position)
    #wheel.set_elevation(road.piles[wheel.xf])

    return bump_position


def determine_bump_height(road: Road, wheel: Wheel, position: int, method='max') -> int:
    """
    General bump height function, returns the bump height of a position on a road for a given
    wheel_size and method
    :param road: a Road
    :param wheel: a Wheel
    :param position: int
    :param method: str, 'max'
    :return: a bump_height function call
    """
    available_methods = list(['max', 'max'])
    default_method = 'max'
    method = method

    if method not in available_methods:
        print("The bump_height method '", method, "' does not exist. Using default method '", default_method, "'")
        method = 'max'

    if method == 'max':
        return max_bump_height(road, wheel, position)


def max_bump_height(road: Road, wheel: Wheel, position: int) -> int:
    """
    At position i determine the bump height of the next w elements/indexes/positions
    with w being the wheel diameter.
    The bump height is determined by taking the maximum from the positions i+1 to i+w (inclusive) minus
    the current elevation of the wheel.
    :param road: a Road
    :param wheel: a Wheel
    :param position: int, current (front) position of the wheel
                         (it should be the first position before the bump position)
    :return: the bump height
    """
    return np.max(road.piles[(position + 1): (position + 1 + wheel.diameter)]) - wheel.elevation


def jump(road: Road, wheel: Wheel, bump_height: int):
    """
    Updates the wheel's position and elevation before it jumps.
    :param road:
    :param wheel:
    :param bump_height: the height of the bump from which the wheel jumps
    :return: void
    """
    wheel.update_position(wheel.velocity * bump_height + wheel.diameter)
    wheel.set_elevation(road.piles[wheel.xf])



def print_road_surface(road: Road, wheel_pos=None, wheel_size=None):
    """
    Prints the road surface. It also prints the lower part of the wheel if  wheel_pos != None
    and wheel_size != None (both conditions at the same time)
    :param road: a Road
    :param wheel_pos:
    :param wheel_size:
    :return: prints the road with or without the wheel as standard output.
    """
    max_height = road.piles.max() + 1
    current_height = max_height
    road_surface = []
    for i in range(max_height + 1):
        for pos, height in enumerate(road.piles):
            if height >= current_height:
                road_surface.append('.')
            else:
                if (wheel_pos is not None) & (wheel_size is not None):
                    if wheel_pos - wheel_size < pos <= wheel_pos and height == current_height - 1:
                        road_surface.append('w')
                    else:
                        road_surface.append(' ')
                else:
                    road_surface.append(' ')
        current_height -= 1
        road_surface.append('\n')
    print(''.join(road_surface))


def wheel_pass(road: Road, wheel: Wheel, max_iterations: int, bump_method: str, dig_method: str, dig_probability_arguments: list):
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
            smoothing(road, wheel, 5)
            current_passes = wheel.number_of_passes
        initial_position = wheel.xf
        bump_position = move_to_next_bump(road, wheel)
        bump_height = determine_bump_height(road, wheel, bump_position, method=bump_method)
        jump(road, wheel, bump_height)

        digging(road, wheel, wheel.xf, method=dig_method, dig_probability_args = dig_probability_arguments)

        wheel.update_position(wheel.diameter)
        wheel.set_elevation(road.piles[wheel.xf])

        final_position = wheel.xf
        if final_position <= initial_position:
            smoothing(road, wheel, 5)
            wheel.number_of_passes += 1
            print(f'\nIteration number {wheel.number_of_passes}')
            print(
                f'The number of grains is {road.get_number_of_grains()}, the initial was {road.initial_number_of_grains}\n')
            print_road_surface(road, wheel.xf, wheel.diameter)

def wheel_pass_debugging2(road: Road, wheel: Wheel, max_iterations: int, bump_method: str, dig_method: str, dig_probability_arguments: list):
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
            smoothing(road, wheel, 5)
            current_passes = wheel.number_of_passes
        initial_position = wheel.xf
        print_road_surface(road, wheel.xf, wheel.diameter)

        bump_position = move_to_next_bump(road, wheel)
        bump_height = determine_bump_height(road, wheel, bump_position, method=bump_method)

        print_road_surface(road, wheel.xf, wheel.diameter)

        jump(road, wheel, bump_height)

        print_road_surface(road, wheel.xf, wheel.diameter)


        digging(road, wheel, wheel.xf, method=dig_method, dig_probability_args = dig_probability_arguments)

        wheel.update_position(wheel.diameter)
        wheel.set_elevation(road.piles[wheel.xf])

        print_road_surface(road, wheel.xf, wheel.diameter)


        final_position = wheel.xf
        if final_position <= initial_position:
            smoothing(road, wheel, 5)
            wheel.number_of_passes += 1
            print(f'\nIteration number {wheel.number_of_passes}')
            print(
                f'The number of grains is {road.get_number_of_grains()}, the initial was {road.initial_number_of_grains}\n')
            print_road_surface(road, wheel.xf, wheel.diameter)


def wheel_pass_debugging(road: Road, wheel: Wheel, max_iterations: int, bump_method: str,
                         dig_method: str, dig_probability_arguments: list):
    """
    Put a red circle (for the debugger) in each print statement that is not hidden with a '#'
    :param road:
    :param wheel:
    :param max_iterations:
    :param bump_method:
    :param dig_method:
    """
    while wheel.number_of_passes < max_iterations:
        # passes = wheel.number_of_passes
        initial_position = wheel.xf
        print_road_surface(road, wheel.xf, wheel.diameter)
        elevation = wheel.elevation
        bump_position = move_to_next_bump(road, wheel)
        bump_height = determine_bump_height(road, wheel, bump_position, method=bump_method)
        # print(f'\nbump position = {bump_position}\n')
        # print(f'\nbump height = {bump_height}\n')
        elevation = wheel.elevation

        print_road_surface(road, wheel.xf, wheel.diameter)

        jump(road, wheel, bump_height)
        # elevation = wheel.elevation

        print_road_surface(road, wheel.xf, wheel.diameter)
        digging(road, wheel, wheel.xf, method=dig_method, dig_probability_args = dig_probability_arguments)

        print_road_surface(road, wheel.xf, wheel.diameter)
        wheel.update_position(wheel.diameter)
        wheel.set_elevation(road.piles[wheel.xf])
        elevation = wheel.elevation

        final_position = wheel.xf
        if final_position <= initial_position:
            wheel.number_of_passes += 1
            print(f'\nIteration number {wheel.number_of_passes}')
            print(
                f'The number of grains is {road.get_number_of_grains()}, the initial was {road.initial_number_of_grains}\n')
            # print_road_surface(road, wheel.xf, wheel.diameter)

def save_road(road: Road, output_filename: str):
    with open(output_filename, 'wb') as output:
        pickle.dump(road, output, pickle.HIGHEST_PROTOCOL)

def read_road(input_filename: str):
    with open(input_filename, 'rb') as input:
        road = pickle.load(input)
    return(road)

def plot_road(road: Road):
    plt.plot(road.piles)
    plt.xlabel('Distance (block size units)')
    plt.ylabel('Surface height (block size units)')
    plt.title('Road surface profile')
    plt.grid(True)

    #plt.axes().set_aspect('equal', 'datalim')
    xmin = 0
    xmax = road.size
    ymin = 0-5
    ymax = max(road.piles)+10
    plt.axis([xmin, xmax, ymin, ymax])
    plt.axes().set_aspect('equal', 'box')

    plt.show()



def main():
    debugging = False  # True

    number_of_wheel_passes = 200  # number of 'vehicles' that pass through the road in the whole simulation
    road_size = 500  # length of the road
    standard_height = 10  # standard height or initial height of the road
    nr_of_irregular_points = 20  # number of irregularities for the Road.add_random_irregularities function
    wheel_size = 6  # (Initial) wheel diameter
    velocity = 5  # Proportionality constant to jump (BETA) 2

    # Initialization of a Road, road, and a Wheel, wheel.
    #road = Road(road_size, standard_height, 'specific', list([4, 40]), list([1, 1]))
    #random.seed(2)
    road = Road(road_size, standard_height, 'random', list([None]), list([nr_of_irregular_points]))
    wheel = Wheel(wheel_size, 0, standard_height, velocity, road.size)

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
        sys.exit()


    # Print the initial road-wheel configuration
    print_road_surface(road, wheel.xf, wheel.diameter)
    # Perform the wheel passes
    if debugging is False:
        wheel_pass(road, wheel, number_of_wheel_passes, 'max', dig_method, dig_probability_args)
    else:
        wheel_pass_debugging2(road, wheel, number_of_wheel_passes, 'max', dig_method, dig_probability_args)


    #save_road(road, 'test_road1.pkl')

    print_road_surface(road, wheel.xf, wheel.diameter)

    print("\nThe simulation has finished...\n")
    #road_read = read_road('test_road1.pkl')

   #print(road_read.piles)
    plot_road(road)


if __name__ == '__main__':
    main()
