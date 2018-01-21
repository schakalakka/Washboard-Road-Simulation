import sys
from road import Road
from wheel import Wheel


#######################################################
#            SIMULATION PARAMETERS AND CONSTANTS      #
#######################################################
def init():
    debugging = False  # True

    number_of_wheel_passes = 200  # number of 'vehicles' that pass through the road in the whole simulation
    road_size = 200  # length of the road
    standard_height = 10  # standard height or initial height of the road
    nr_of_irregular_points = 20  # number of irregularities for the Road.add_random_irregularities function
    wheel_size = 6  # (Initial) wheel diameter
    velocity = 5  # Proportionality constant to jump (BETA) 2

    #######################################################
    # Initialization of a Road, road, and a Wheel, wheel. #
    #######################################################

    # road = Road(road_size, standard_height, 'specific', list([4, 40]), list([1, 1]))
    # random.seed(2)
    road = Road(road_size, standard_height, 'random', list([None]), list([nr_of_irregular_points]))
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
    smoothing_method = 'strategy 1'
    h_max = road.height + 3
    h_max_wind = road.height + 4
    slope_iterations = 5

    if (smoothing_method == 'strategy 1'):
        smoothing_args = list([h_max, slope_iterations])
    elif (smoothing_method == 'strategy 2'):
        smoothing_args = list([h_max, slope_iterations, h_max_wind])
    else:
        print('The smoothing method/strategy name is not valid')
        sys.exit()

    return (road, wheel, debugging, number_of_wheel_passes, dig_method,
            dig_probability_args, smoothing_method, smoothing_args)
