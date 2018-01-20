from digging import *
from smoothing import *
from utils import *
from bump import *

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
        bump_position = wheel.move_to_next_bump(road)
        bump_height = determine_bump_height(road, wheel, bump_position, method=bump_method)
        wheel.jump(road, bump_height)

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

def wheel_pass_debugging(road: Road, wheel: Wheel, max_iterations: int, bump_method: str, dig_method: str, dig_probability_arguments: list):
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
            smoothing(road, wheel)
            current_passes = wheel.number_of_passes
        initial_position = wheel.xf

        print_road_surface(road, wheel.xf, wheel.diameter)

        bump_position = wheel.move_to_next_bump(road)
        bump_height = determine_bump_height(road, wheel, bump_position, method=bump_method)

        print_road_surface(road, wheel.xf, wheel.diameter)

        wheel.jump(road, bump_height)

        print_road_surface(road, wheel.xf, wheel.diameter)

        digging(road, wheel, wheel.xf, method=dig_method, dig_probability_args = dig_probability_arguments)

        wheel.update_position(wheel.diameter)
        wheel.set_elevation(road.piles[wheel.xf])

        final_position = wheel.xf
        if final_position <= initial_position:
            smoothing(road, wheel)
            wheel.number_of_passes += 1
            print(f'\nIteration number {wheel.number_of_passes}')
            print(
                f'The number of grains is {road.get_number_of_grains()}, the initial was {road.initial_number_of_grains}\n')
            print_road_surface(road, wheel.xf, wheel.diameter)


def main():

    #######################################################
    #            SIMULATION PARAMETERS AND CONSTANTS      #
    #######################################################
    # @Andreas, you said something like to put this in a separate file?

    debugging = False  # True

    number_of_wheel_passes = 200  # number of 'vehicles' that pass through the road in the whole simulation
    road_size = 100  # length of the road
    standard_height = 10  # standard height or initial height of the road
    nr_of_irregular_points = 20  # number of irregularities for the Road.add_random_irregularities function
    wheel_size = 6  # (Initial) wheel diameter
    velocity = 5  # Proportionality constant to jump (BETA) 2


    #######################################################
    # Initialization of a Road, road, and a Wheel, wheel. #
    #######################################################

    #road = Road(road_size, standard_height, 'specific', list([4, 40]), list([1, 1]))
    #random.seed(2)
    road =Road(road_size, standard_height, 'random', list([None]), list([nr_of_irregular_points]))
    wheel = Wheel(wheel_size, 0, standard_height, velocity, road.size)

    #########################################################
    #                 DIGGING METHOD                        #
    #########################################################
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

    ###########################################################
    #                 SMOOTHING METHOD                        #
    ###########################################################
     ##todo

     #1) deterministic wind (global) smoothing function
       # given a maximum height threshold put all the grains above that
       # to the positions with lowest height

      #1.2) RANDOM wind (global) smoothing function
       # given a maximum height threshold put all the grains above that
       # to the  RANDOM positions

     #2) a generalized slope smoothing function:

     #3) Organize smoothing.py as in digging.py


    #############################################################
    #                 SIMULATION BODY                           #
    #############################################################

    # Print the initial road-wheel configuration
    print_road_surface(road, wheel.xf, wheel.diameter)
    # Perform the wheel passes
    if debugging is False:
        wheel_pass(road, wheel, number_of_wheel_passes, 'max', dig_method, dig_probability_args)
    else:
        wheel_pass_debugging(road, wheel, number_of_wheel_passes, 'max', dig_method, dig_probability_args)
    print("\nThe simulation has finished...\n")

    ##############################################################
    #         SAVE ROAD IN FILE AND PLOTS                        #
    ##############################################################
    #save_road(road, 'test_road1.pkl')
    print_road_surface(road, wheel.xf, wheel.diameter)


    plot_road(road)


if __name__ == '__main__':
    main()
