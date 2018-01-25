import sys

#######################################################
#            SIMULATION PARAMETERS AND CONSTANTS      #
#######################################################
debugging = False  # True
verbose = False

number_of_wheel_passes = 150  # number of 'vehicles' that pass through the road in the whole simulation
road_size = 1000  # length of the road
standard_height = 20  # standard height or initial height of the road
nr_of_irregular_points = int(road_size/10)  # number of irregularities for the Road.add_random_irregularities function
wheel_size = 6  # (Initial) wheel diameter
velocity = 5  # Proportionality constant to jump (BETA) 2


#########################################################
#                 DIGGING METHOD                        #
#########################################################
dig_method = 'backwards tailed exponential'
constant_probability = 1
h0 = standard_height + 0
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
h_max = standard_height + 3
h_max_wind = standard_height + 4
slope_iterations = 6
increment_h_max_wind = 1  # NOT WORKING, strategy3, eternal loop¿

if smoothing_method == 'strategy 1':
    smoothing_args = list([h_max, slope_iterations])
elif smoothing_method == 'strategy 2':
    smoothing_args = list([h_max, slope_iterations, h_max_wind])
elif smoothing_method == 'strategy 3':
    smoothing_args = list([h_max, slope_iterations, increment_h_max_wind])
else:
    print('The smoothing method/strategy name is not valid')
    sys.exit()

# return (road, wheel, debugging, number_of_wheel_passes, dig_method,
#         dig_probability_args, smoothing_method, smoothing_args)
