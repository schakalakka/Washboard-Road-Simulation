import itertools

from main import main
from utils import plot_road

from initialization import *

# road_sizes = [100, 200, 300]
# number_of_wheel_passes_list = [100, 200]
# standard_heights = [10, 20]
# nr_of_irregular_points_list = [5, 10, 20]
wheel_sizes = [40]
velocities = [2, 5, 10]
h0_list = [1, 2, 3, 4]
alphas = [0.1, 0.5, 1]
smoothing_methods = ['strategy 1', 'strategy 2']  # , 'strategy 3']
slope_iterations_list = [1, 2, 6, 10]
h_max_list = [2, 3, 5]

all_lists = [wheel_sizes, velocities, h0_list, alphas, smoothing_methods, slope_iterations_list, h_max_list]
print(len(list(itertools.product(*all_lists))))
for i, element in enumerate(itertools.product(*all_lists)):
    if 600 <= i < 864:
        print(i)
        wheel_size = element[0]
        velocity = element[1]
        h0 = element[2] + standard_height
        alpha = element[3]
        smoothing_method = element[4]
        slope_iterations = element[5]
        h_max = element[6] + standard_height
        parameter_dict = {'it': i, 'wheel_size': wheel_size, 'velocity': velocity, 'h0': h0, 'alpha': alpha,
                          'smoothing_method': smoothing_method, 'slope_iterations': slope_iterations, 'h_max': h_max}
        main(parameter_dict)
