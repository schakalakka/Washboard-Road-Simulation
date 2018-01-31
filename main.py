from digging import *
from smoothing import *
from utils import *
from bump import *

from initialization import *


def wheel_pass(road: Road, wheel: Wheel, max_iterations: int, bump_method: str,
               dig_method: str, dig_probability_arguments: list,
               smoothing_method: str, smoothing_arguments: list):
    """
     This function performs a loop of wheel passes through a road until 'max_iterations'
     wheel passes have been performed. The successive wheel passes modify the road surface.

    :param road: a Road
    :param wheel: a Wheel
    :param max_iterations: maximum number of wheel passes (iterations)
    :param bump_method: str, method name for the 'determine_bump_height' function
    :param dig_method: str, method name for the 'digging' function
    :param dig_probability_arguments:
    :param smoothing_method:
    :param smoothing_arguments:
    """
    current_passes = 0
    while wheel.number_of_passes < max_iterations:
        if current_passes < wheel.number_of_passes:
            smoothing(road, wheel, smoothing_method, smoothing_arguments)
            current_passes = wheel.number_of_passes
        initial_position = wheel.xf
        bump_position = wheel.move_to_next_bump(road)
        bump_height = determine_bump_height(road, wheel, bump_position, method=bump_method)
        wheel.jump(road, bump_height)

        digging(road, wheel, wheel.xf, method=dig_method, dig_probability_args=dig_probability_arguments)

        wheel.update_position(wheel.diameter)
        wheel.set_elevation(road.piles[wheel.xf])

        final_position = wheel.xf
        if final_position <= initial_position:
            smoothing(road, wheel, smoothing_method, smoothing_arguments)
            wheel.number_of_passes += 1
            if verbose:
                print(f'\nIteration number {wheel.number_of_passes}')
                print(
                    f'The number of grains is {road.get_number_of_grains()}, the initial was {road.initial_number_of_grains}\n')
                print_road_surface(road, wheel.xf, wheel.diameter)


def wheel_pass_debugging(road: Road, wheel: Wheel, max_iterations: int, bump_method: str,
                         dig_method: str, dig_probability_arguments: list,
                         smoothing_method: str, smoothing_arguments: list):
    """
     This function performs a loop of wheel passes through a road until 'max_iterations'
     wheel passes have been performed. The successive wheel passes modify the road surface.

    :param road: a Road
    :param wheel: a Wheel
    :param max_iterations: maximum number of wheel passes (iterations)
    :param bump_method: str, method name for the 'determine_bump_height' function
    :param dig_method: str, method name for the 'digging' function
    :param dig_probability_arguments:
    :param smoothing_method:
    :param smoothing_arguments:
    """
    current_passes = 0
    while wheel.number_of_passes < max_iterations:
        if current_passes < wheel.number_of_passes:
            smoothing(road, wheel, smoothing_method, smoothing_arguments)
            current_passes = wheel.number_of_passes
        initial_position = wheel.xf

        print_road_surface(road, wheel.xf, wheel.diameter)

        bump_position = wheel.move_to_next_bump(road)
        bump_height = determine_bump_height(road, wheel, bump_position, method=bump_method)

        print_road_surface(road, wheel.xf, wheel.diameter)

        wheel.jump(road, bump_height)

        print_road_surface(road, wheel.xf, wheel.diameter)

        digging(road, wheel, wheel.xf, method=dig_method, dig_probability_args=dig_probability_arguments)

        wheel.update_position(wheel.diameter)
        wheel.set_elevation(road.piles[wheel.xf])

        final_position = wheel.xf
        if final_position <= initial_position:
            smoothing(road, wheel, smoothing_method, smoothing_arguments)
            wheel.number_of_passes += 1
            print(f'\nIteration number {wheel.number_of_passes}')
            print(
                f'The number of grains is {road.get_number_of_grains()}, the initial was {road.initial_number_of_grains}\n')
            print_road_surface(road, wheel.xf, wheel.diameter)


def main(kwargs=None):
    #######################################################
    # Initialization of a Road, road, and a Wheel, wheel. #
    #######################################################

    # road = Road(road_size, standard_height, 'specific', list([4, 40]), list([1, 1]))
    # random.seed(2)
    if read_initial_road:
        road = read_road(initial_road_filename)
    elif random_road:
        road = Road(road_size, standard_height, 'random', list([None]), list([nr_of_irregular_points]))
        road_to_csv(road, kwargs)
    else:
        step = 10
        rang = range(step, road_size, step)
        road = Road(road_size, standard_height, 'specific', list([rang]), list([1 for i in rang]))
        road_to_csv(road, kwargs)

    # Initial road equidistant
    if save_initial_road:
        if initial_road_filename == 'initial_road_equidistant.pkl':
            step = 10
            rang = range(step, road_size, step)
            road = Road(road_size, standard_height, 'specific', list([rang]), list([1 for i in rang]))
        save_road(road, initial_road_filename)
        print(f'Initial road saved with name {initial_road_filename}')
        sys.exit()

    wheel = Wheel(wheel_size, 0, road.height, velocity, road.size)

    #############################################################
    #                 SIMULATION BODY                           #
    #############################################################
    average_simulation = False

    if average_simulation == False:
        if verbose:
            # Print the initial road-wheel configuration
            print_road_surface(road, wheel.xf, wheel.diameter)
        # Perform the wheel passes
        if debugging is False:
            wheel_pass(road, wheel, number_of_wheel_passes, 'max',
                       dig_method, dig_probability_args,
                       smoothing_method, smoothing_args)
        else:
            wheel_pass_debugging(road, wheel, number_of_wheel_passes, 'max', dig_method, dig_probability_args)
    else:
        average_simulations(1)
    if verbose:
        print("\nThe simulation has finished...\n")

    ##############################################################
    #         SAVE ROAD IN FILE AND PLOTS                        #
    ##############################################################
    # save_road(road, 'test_road1.pkl')
    if verbose:
        print_road_surface(road, wheel.xf, wheel.diameter)

    # plot_road(road, kwargs)
    road_to_csv(road, kwargs)


if __name__ == '__main__':

    velocities = [3, 5, 6, 11, 20]
    wheel_sizes = [3, 5, 7, 10, 20, 21, 30]
    alphas = [0, 0.1, 0.5, 0.7, 1, 1000]
    p_wind_list = [0, 0.1, 0.2, 0.5, 1]
    # for elem in velocities:
    #     velocity = elem
    #     main({'velocity': velocity})

    # for elem in wheel_sizes:
    #     wheel_size = elem
    #     main({'wheel_size': wheel_size})

    for alpha in alphas:
        dig_probability_args = [h0, alpha]
        main({'alpha': alpha})

    # for p_wind in p_wind_list:
    #     smoothing_args = [h_max, slope_iterations, increment_h_max_wind, lower_bound_increment_h_max_wind, p_wind]
    #     main({'p_wind': p_wind})
    # main()
