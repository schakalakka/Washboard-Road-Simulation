import itertools

from main import main
from utils import plot_road

from initialization import *

# road_sizes = [100, 200, 300]
# number_of_wheel_passes_list = [100, 200]
# standard_heights = [10, 20]
# nr_of_irregular_points_list = [5, 10, 20]
wheel_sizes = [4, 6, 8]
velocities = [2, 5, 10]
h0_list = [1, 2, 3, 4]
alphas = [0.1, 0.5, 1]

all_lists = [wheel_sizes, velocities, h0_list, alphas]

for i, element in enumerate(itertools.product(*all_lists)):
    print(i)
    wheel_size = element[0]
    velocity = element[1]
    h0 = element[2] + standard_height
    alpha = element[3]
    parameter_dict = {'wheel_size': wheel_size, 'velocity': velocity, 'h0': h0, 'alpha': alpha}
    main(parameter_dict)
