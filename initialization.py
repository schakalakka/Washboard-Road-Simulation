import sys
from road import Road
from utils import read_road

#######################################################
#            SIMULATION PARAMETERS AND CONSTANTS      #
#######################################################
debugging = False  # True
verbose = False
save_initial_road = False

random_road = False
read_initial_road = False
initial_road_filename = 'initial_road_equidistant.pkl'

number_of_wheel_passes = 1000  # number of 'vehicles' that pass through the road in the whole simulation
road_size = 500  # length of the road 1000
if read_initial_road:
    road = read_road(initial_road_filename)
    standard_height = road.height
    wheel_size = int(road.size / 50)
else:
    wheel_size = 10  # road_size/50
    standard_height = 100  # standard height or initial height of the road

nr_of_irregular_points = int(road_size / 50)  # number of irregularities for the Road.add_random_irregularities function

velocity = 11  # Proportionality constant to jump (BETA) 2

#########################################################
#                 DIGGING METHOD                        #
#########################################################
dig_method = 'backwards tailed exponential'  # 'backwards uniform'#'backwards tailed exponential'
constant_probability = 1
h0 = standard_height
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
smoothing_method = 'strategy 3'
h_max = standard_height + 3
h_max_wind = standard_height + 4  # not used in strategy 3
slope_iterations = 6
increment_h_max_wind = 1  # strength of the wind
lower_bound_increment_h_max_wind = 3  # In fact it is: lower bound of h_max = road.height + l_b_i_h_max_wind
p_wind = 0.2  # Probability of wind effects occurring in each call to the general smoothing function
slope = 1  # arctan(slope)*360/(2*pi) gives the angle of repose that the bumps will tend by applying slope_smoothing

if smoothing_method == 'strategy 1':
    smoothing_args = list([h_max, slope_iterations])
elif smoothing_method == 'strategy 2':
    smoothing_args = list([h_max, slope_iterations, h_max_wind, p_wind])
elif smoothing_method == 'strategy 3':
    smoothing_args = list([h_max, slope_iterations, increment_h_max_wind, lower_bound_increment_h_max_wind, p_wind])
elif smoothing_method == 'strategy 4':
    smoothing_args = list(
        [h_max, slope_iterations, increment_h_max_wind, lower_bound_increment_h_max_wind, p_wind, slope])
else:
    print('The smoothing method/strategy name is not valid')
    sys.exit()

# return (road, wheel, debugging, number_of_wheel_passes, dig_method,
#         dig_probability_args, smoothing_method, smoothing_args)
