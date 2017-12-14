import numpy as np
from typing import Tuple

import sys
#CLASSES

class Wheel:
    """
    Object that represents a vehicle wheel
    """
    def __init__(self, diameter: int, right_position: int, elevation: int, period: int):
        self.diameter = diameter
        self.x0 = diameter - right_position #Care, now it could be negative
        self.xf = right_position
        self.elevation = elevation
        self.period = period

    def get_diameter(self):
        return self.diameter
    def get_x0(self):
        return self.x0
    def get_xf(self):
        return self.xf

    def set_diameter(self, new_diameter: int):
        if new_diameter <= 0:
            print ('Error: Wheel diameter can not be set to a negative number.')
            sys.exit()
        self.diameter = new_diameter
    def set_x0(self, new_x0: int):
        if new_x0 < 0:
            print ('Intent to set x0 to a negative number or out of the road. Applying periodic', self.period ,'conditions.')
            self.x0 = new_x0 % self.period
        else:
            self.x0 = new_x0
    def set_xf(self, new_xf: int):
        if new_xf >= self.period:
            print ('Intent to set xf to a negative number or out of the road. Applying periodic', self.period ,'conditions.')
            self.xf = new_xf % self.period
        else:
            self.xf = new_xf


def initialize_road(size: int, standard_height: int, nr_of_random_irregularities: int) -> np.ndarray:
    """
    Initializes a numpy array of a given length with a standard height and several small irregular bumps
    :param size: size/length of road, i.e. positions
    :param standard_height: level above zero
    :param nr_of_random_irregularities: number of bumps (position is chosen randomly)
    :return: road array
    """
    road = np.full(size, standard_height, dtype=np.int)
    irregular_positions = np.random.randint(0, len(road), nr_of_random_irregularities)
    road[irregular_positions] = [standard_height + 1] * nr_of_random_irregularities
    return road


def smoothing(road: np.ndarray) -> np.ndarray:

    pass


def determine_bump_height(road: np.ndarray, position: int, wheel_size: int, method='max') -> int:
    """
    General bump height function, returns the bump height of a position on a road for a given
    wheel_size and method
    :param road: np.ndarray, array with height at each position of the road
    :param position: int, current position on road
    :param wheel_size: int
    :param method: str, 'max'
    :return: int, bump height
    """
    available_methods = list(['max', 'max'])
    default_method = 'max'
    method = method

    if method not in available_methods:
        print("The bump_height method '",  method  ,"' does not exist. Using default method '", default_method, "'")
        method = 'max'


    if method == 'max':
        return max_bump_height(road, position, wheel_size)




def max_bump_height(road: np.ndarray, position: int, wheel_size: int) -> int:
    """
    At position i determine the bump height of the next w elements/indexes/positions
    with w being the wheel_size.
    The bump height ist determined by taking the maximum from the positions i+1 to i+w (inclusive)
    :param road: np.ndarray, road surface
    :param position: int, current (front) position of the wheel
    :param wheel_size: int, width of the wheel
    :return: int, the bump height
    """
    return np.max(road[ (position + 1) : (position + 1 + wheel_size) ])


def jump(from_position: int, bump_heigth: int, velocity: int, road_length: int) -> int:
    """
    Returns the front position of the wheel after a jump
    :param from_position:
    :param bump_heigth:
    :param velocity:
    :param road_length:
    :return:
    """
    return (from_position + velocity * bump_heigth) % road_length


def digging(road: np.ndarray, position: int, wheel_size: int, method='backwards') -> Tuple[np.ndarray, int]:
    """
    Returs the road after an digging event
    :param road:
    :param position:
    :param wheel_size:
    :param method:
    :return:
    """
    if method == 'backwards':
        return dig_backwards(road, position, wheel_size)


def dig_backwards(road: np.ndarray, position: int, wheel_size: int) -> Tuple[np.ndarray, int]:
    """
    Returns the after a backwards digging event, i.e. all the sand is put back behind the wheel
    :param road:
    :param position:
    :param wheel_size:
    :return:
    """
    remove_from = np.mod(np.arange(position - wheel_size + 1, position + 1), len(road))
    put_on = np.mod(np.arange(position - 2 * wheel_size + 1, position - wheel_size + 1), len(road))
    road[remove_from] -= (road[remove_from] > 0).astype(int)
    road[put_on] += (road[remove_from] > 0).astype(int)
    return road, position + wheel_size


def print_road_surface(road: np.ndarray, wheel_pos=None, wheel_size=None):
    """
    Prints the road surface. So far without the wheel.
    :param road: np.ndarray with the height in each index/column/position
    :return:
    """
    max_height = road.max() + 1
    current_height = max_height
    road_surface = []
    for i in range(max_height + 1):
        for pos, height in enumerate(road):
            if height >= current_height:
                road_surface.append('.')
            else:
                if wheel_pos is not None:
                    if wheel_pos - wheel_size < pos <= wheel_pos and height == current_height - 1:
                        road_surface.append('w')
                    else:
                        road_surface.append(' ')
                else:
                    road_surface.append(' ')
        current_height -= 1
        road_surface.append('\n')
    print(''.join(road_surface))


def wheel_pass(road: np.ndarray, wheel_size: int, velocity: int, max_iterations: int, bump_method: str,
               dig_method: str):
    current_height = road[0]
    pos = 1
    iteration = 0
    while iteration < max_iterations:
        if road[pos] <= current_height:
            current_height = road[pos]
            pos += 1
            if pos == len(road):
                pos = 0
                iteration += 1
        else:
            bump_height = determine_bump_height(road, pos, wheel_size, method=bump_method)
            new_pos = jump(from_position=pos, bump_heigth=bump_height, velocity=velocity, road_length=len(road))
            road, new_pos = digging(road, new_pos, wheel_size, method=dig_method)
            if new_pos < pos:
                iteration += 1
            pos = new_pos
        print_road_surface(road, pos, wheel_size)


def main():
    iterations = 100
    road_size = 183
    standard_height = 5
    nr_of_irregular_points = 5
    wheel_size = 4
    velocity = 5  # m/s
    road = initialize_road(road_size, standard_height, nr_of_irregular_points)
    print_road_surface(road)
    wheel_pass(road, wheel_size, velocity, iterations, bump_method='max', dig_method='backwards')
    pass


if __name__ == '__main__':
    main()
