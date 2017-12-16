import numpy as np
from typing import Tuple

import sys
#CLASSES

class Wheel:
    """
    Object that represents a vehicle wheel
    """
    def __init__(self, diameter: int, right_position: int, elevation: int, velocity: int, period: int):
        self.diameter = diameter
        self.xf = right_position % period
        self.x0 = (self.xf - self.diameter + 1) % period #Care, now it could be negative
        self.elevation = elevation
        self.period = period
        self.velocity = velocity
        self.number_of_passes = 0

    def get_diameter(self):
        return self.diameter
    def get_x0(self):
        return self.x0
    def get_xf(self):
        return self.xf

    def set_diameter(self, new_diameter: int):
        if new_diameter <= 0:
            print ('Error: Wheel diameter can not be set to a negative number nor zero.')
            sys.exit()
        self.diameter = new_diameter

    def set_elevation(self, new_elevation: int):
        if new_elevation < 0:
            print('Error: Wheel elevation can not be set to a negative number.')
            sys.exit()
        self.elevation = new_elevation

    def set_velocity(self, new_velocity: int):
        self.velocity = new_velocity

    def set_xf(self, new_xf: int):
        if new_xf >= self.period or new_xf < 0:
            print ('Intent to set xf to a negative number or out of the road. Applying periodic', self.period ,'conditions.')
        self.xf = new_xf % self.period
        self.x0 = (self.xf - self.diameter + 1) % self.period

    def update_position(self, steps: int):
        new_xf = self.xf + steps
        self.set_xf(new_xf)
    def update_velocity(self, steps: int):
        new_velocity = self.velocity + steps
        self.set_velocity(new_velocity)
    def update_elevation(self, steps: int):
        new_elevation = self.elevation + steps
        self.set_elevation(new_elevation)
    def update_diameter(self, steps: int):
        new_diameter = self.diameter + steps
        self.set_diameter(new_diameter)



class Road:
    def __init__(self, size: int, standard_height: int, irregularities = 'random', positions = list([1]), n_grains = list([1])):
        self.piles = np.full(size, standard_height, dtype=np.int)
        self.size = size
        self.height = standard_height
        #self.initial_number_of_grains = size * standard_height

        if irregularities == 'random':
            self.add_random_irregularities(n_grains[0])
        elif irregularities == 'specific':
            self.add_specific_irregularities(positions, n_grains)

        self.initial_number_of_grains = self.get_number_of_grains();

    def get_number_of_grains(self):
        return np.sum(self.piles)

    def add_random_irregularities(self, nr_of_random_irregularities: int):
        irregular_positions = np.random.randint(0, len(self.piles), nr_of_random_irregularities)
        self.piles[irregular_positions] = [self.height + 1] * nr_of_random_irregularities
        #self.initial_number_of_grains += nr_of_random_irregularities

    def add_specific_irregularities(self, positions: list, n_grains: list):
        """
        :param positions:
        :param n_grains:
        :return:
        """
        self.piles[positions] += n_grains
        #self.initial_number_of_grains += np.sum(n_grains)


    def add_grain(self, position: int, n_grains: int):
        self.piles[position] += n_grains

    def remove_grain(self, position: int, n_grains: int):
        self.piles[position] -= n_grains

    def add_grains(self, positions: list, n_grains: list):
        counter = 0
        for position in positions:
            self.add_grain(self, positions[position], n_grains[counter])
            counter += 1

    def remove_grains(self, positions: list, n_grains: list):
        counter = 0
        for position in positions:
            self.remove_grain(self, positions[position], n_grains[counter])
            counter += 1


def smoothing(road: np.ndarray) -> np.ndarray:

    pass



def move_to_next_bump(road: Road, wheel: Wheel) -> int:
    period = road.size
    pos_count = wheel.xf
    #elevation = wheel.elevation
    #f = road.piles[pos_count % period]
    #statement = (pos_count < road.size) & (road.piles[pos_count % period] <= wheel.elevation)
    while (pos_count < 2*period) & (road.piles[pos_count % period] <= wheel.elevation):
        pos_count += 1

    if pos_count > 2*period:
           print("\nNo next bump found. move_to_next_bump() failed.\n")
           sys.exit()

    #if pos_count >= period:
        #wheel.number_of_passes += 1

    bump_position = (pos_count % period) - 1
    wheel.set_xf( bump_position )

    return bump_position

def determine_bump_height(road: Road, wheel: Wheel, position: int,  method='max') -> int:
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
        return max_bump_height(road, wheel, position)




def max_bump_height(road: Road, wheel: Wheel, position: int) -> int:
    """
    At position i determine the bump height of the next w elements/indexes/positions
    with w being the wheel_size.
    The bump height ist determined by taking the maximum from the positions i+1 to i+w (inclusive)
    :param road: np.ndarray, road surface
    :param position: int, current (front) position of the wheel
    :param wheel_size: int, width of the wheel
    :return: int, the bump height
    """
    return np.max(road.piles[ (position + 1) : (position + 1 + wheel.diameter) ]) - wheel.elevation

def jump(road: Road, wheel: Wheel, bump_height: int):
    """
    Returns the front position of the wheel after a jump
    :param from_position:
    :param bump_heigth:
    :param velocity:
    :param road_length:
    :return:
    """
    #wheel.xf = (wheel.xf + wheel.velocity * bump_height) % road.size
    wheel.update_position(wheel.velocity * bump_height)
    wheel.set_elevation(road.piles[wheel.xf])

def digging(road: Road,  wheel: Wheel, position: int, method='backwards'): # -> Tuple[np.ndarray, int]:
    """
    Returs the road after an digging event
    :param road:
    :param position:
    :param wheel_size:
    :param method:
    :return:
    """
    if method == 'backwards':
        return dig_backwards(road, wheel, position)



def dig_backwards(road: Road, wheel: Wheel, position: int): # -> Tuple[np.ndarray, int]:
    """
    Returns the after a backwards digging event, i.e. all the sand is put back behind the wheel
    :param road:
    :param position:
    :param wheel_size:
    :return:
    """
    remove_from = np.mod(np.arange(position - wheel.diameter + 1, position + 1), road.size)
    put_on = np.mod(np.arange(position - 2 * wheel.diameter + 1, position - wheel.diameter + 1), road.size)
    increments = (road.piles[remove_from] > 0).astype(int)
    if len(remove_from) != len(put_on):
        print("\nWe are going to remove or put more or less than put or remove grains\n")
        sys.exit()

    road.piles[remove_from] -= increments
    road.piles[put_on] += increments
    #return position + wheel.diameter




def print_road_surface(road: Road, wheel_pos=None, wheel_size=None):
    """
    Prints the road surface. So far without the wheel.
    :param road: np.ndarray with the height in each index/column/position
    :return:
    """
    max_height = (road.piles).max() + 1
    current_height = max_height
    road_surface = []
    for i in range(max_height + 1):
        for pos, height in enumerate(road.piles):
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



def wheel_pass(road: Road, wheel: Wheel, max_iterations: int, bump_method: str,
               dig_method: str):

    while wheel.number_of_passes < max_iterations:
        #passes = wheel.number_of_passes
        initial_position = wheel.xf
        #print_road_surface(road, wheel.xf, wheel.diameter)
        #elevation = wheel.elevation
        bump_position = move_to_next_bump(road, wheel)
        bump_height = determine_bump_height(road, wheel, bump_position, method = bump_method)
        #print(f'\nbump position = {bump_position}\n')
        #print(f'\nbump height = {bump_height}\n')
        elevation = wheel.elevation
        #print_road_surface(road, wheel.xf, wheel.diameter)
        jump(road, wheel, bump_height)
        #elevation = wheel.elevation

        #print_road_surface(road, wheel.xf, wheel.diameter)
        digging(road, wheel, wheel.xf, method = dig_method)

        #print_road_surface(road, wheel.xf, wheel.diameter)
        wheel.update_position(wheel.diameter)
        wheel.set_elevation(road.piles[wheel.xf])
        #elevation = wheel.elevation
        final_position = wheel.xf
        if final_position <= initial_position:
            wheel.number_of_passes += 1
            print_road_surface(road, wheel.xf, wheel.diameter)
            print(f'number of grains is {road.get_number_of_grains()}')
        #if
        #iteration += 1
        #end iteration

def main():
    iterations = 100
    road_size = 100
    standard_height = 5
    nr_of_irregular_points = 5
    wheel_size = 4
    velocity = 1  # m/s

    road = Road(road_size, standard_height, 'specific', list([4,40]), list([1,1]))
    wheel = Wheel(wheel_size, 0, standard_height, velocity, road.size)


    #road = initialize_road(road_size, standard_height, nr_of_irregular_points)

    #mystring = f'hello my velocity is {[1,2]}'

    #print(5)
    print_road_surface(road, wheel.xf, wheel.diameter)
   # print(8)
    wheel_pass(road, wheel, iterations, 'max', 'backwards')
    #wheel_pass(road, wheel_size, velocity, iterations, bump_method='max', dig_method='backwards')
    #sys.exit()
    print("\n I have finished the main\n")

if __name__ == '__main__':
    main()

