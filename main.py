# from typing import Tuple
import sys

import numpy as np

from road import Road
from wheel import Wheel



def smoothing(road: Road):
    """
    @TO DO
    :param road:
    :return:
    """
    pass


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
        pos_count += 1

    if pos_count > 2 * period:
        print("\nNo next bump found. move_to_next_bump() failed. ",
              "\nThere are no bumps according to the current criteria\n")
        sys.exit()

    # The position that is just before the 'real' bump position is stored in the bump_position variable
    bump_position = (pos_count % period) - 1

    # Update the wheel's position
    wheel.set_xf(bump_position)

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


def digging(road: Road, wheel: Wheel, position: int, method='backwards'):
    """
    Updates the road after a digging event.
    :param road: a Road
    :param wheel: a Wheel
    :param position: reference position from which start the digging event (usually it is the wheel's position)
    :param method: digging method
    :return: a call to a particular digging function depending on the value of the method parameter.
    """
    if method == 'backwards':
        return dig_backwards(road, wheel, position)


def dig_backwards(road: Road, wheel: Wheel, position: int):  # -> Tuple[np.ndarray, int]:
    """
    @TODO
    (MODIFY)Returns the after a backwards digging event, i.e. all the sand is put back behind the wheel
    :param road: a Road
    :param wheel: a Wheel
    :param position: position from which start the digging event
    :return: void
    """
    remove_from = np.mod(np.arange(position - wheel.diameter + 1, position + 1), road.size)
    put_on = np.mod(np.arange(position - 2 * wheel.diameter + 1, position - wheel.diameter + 1), road.size)
    increments = (road.piles[remove_from] > 0).astype(int)

    if len(remove_from) != len(put_on):
        print("\nWe are going to remove or put more or less than put or remove grains\n")
        sys.exit()

    road.piles[remove_from] -= increments
    road.piles[put_on] += increments


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


def wheel_pass(road: Road, wheel: Wheel, max_iterations: int, bump_method: str, dig_method: str):
    """
     This function performs a loop of wheel passes through a road until 'max_iterations'
     wheel passes have been performed. The successive wheel passes modify the road surface.

    :param road: a Road
    :param wheel: a Wheel
    :param max_iterations: maximum number of wheel passes (iterations)
    :param bump_method: str, method name for the 'determine_bump_height' function
    :param dig_method: str, method name for the 'digging' function
    """
    while wheel.number_of_passes < max_iterations:
        initial_position = wheel.xf
        bump_position = move_to_next_bump(road, wheel)
        bump_height = determine_bump_height(road, wheel, bump_position, method=bump_method)
        jump(road, wheel, bump_height)

        digging(road, wheel, wheel.xf, method=dig_method)

        wheel.update_position(wheel.diameter)
        wheel.set_elevation(road.piles[wheel.xf])

        final_position = wheel.xf
        if final_position <= initial_position:
            wheel.number_of_passes += 1
            print(f'\nIteration number {wheel.number_of_passes}')
            print(
                f'The number of grains is {road.get_number_of_grains()}, the initial was {road.initial_number_of_grains}\n')
            print_road_surface(road, wheel.xf, wheel.diameter)


def wheel_pass_debugging(road: Road, wheel: Wheel, max_iterations: int, bump_method: str,
                         dig_method: str):
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
        # elevation = wheel.elevation
        bump_position = move_to_next_bump(road, wheel)
        bump_height = determine_bump_height(road, wheel, bump_position, method=bump_method)
        # print(f'\nbump position = {bump_position}\n')
        # print(f'\nbump height = {bump_height}\n')
        # elevation = wheel.elevation

        print_road_surface(road, wheel.xf, wheel.diameter)

        jump(road, wheel, bump_height)
        # elevation = wheel.elevation

        print_road_surface(road, wheel.xf, wheel.diameter)
        digging(road, wheel, wheel.xf, method=dig_method)

        print_road_surface(road, wheel.xf, wheel.diameter)
        wheel.update_position(wheel.diameter)
        wheel.set_elevation(road.piles[wheel.xf])
        # elevation = wheel.elevation

        final_position = wheel.xf
        if final_position <= initial_position:
            wheel.number_of_passes += 1
            print(f'\nIteration number {wheel.number_of_passes}')
            print(
                f'The number of grains is {road.get_number_of_grains()}, the initial was {road.initial_number_of_grains}\n')
            # print_road_surface(road, wheel.xf, wheel.diameter)


def main():
    debugging = True  # True

    number_of_wheel_passes = 1000  # number of 'vehicles' that pass through the road in the whole simulation
    road_size = 150  # length of the road
    standard_height = 5  # standard height or initial height of the road
    nr_of_irregular_points = 20  # number of irregularities for the Road.add_random_irregularities function
    wheel_size = 6  # (Initial) wheel diameter
    velocity = 2  # Proportionality constant to jump (BETA)

    # Initialization of a Road, road, and a Wheel, wheel.
    # road = Road(road_size, standard_height, 'specific', list([4, 40]), list([1, 1]))
    road = Road(road_size, standard_height, 'random', list([None]), list([nr_of_irregular_points]))

    wheel = Wheel(wheel_size, 0, standard_height, velocity, road.size)

    # Print the initial road-wheel configuration
    print_road_surface(road, wheel.xf, wheel.diameter)

    # Perform the wheel passes
    if debugging is False:
        wheel_pass(road, wheel, number_of_wheel_passes, 'max', 'backwards')
    else:
        wheel_pass_debugging(road, wheel, number_of_wheel_passes, 'max', 'backwards')

    print("\nThe simulation has finished...\n")


if __name__ == '__main__':
    main()
