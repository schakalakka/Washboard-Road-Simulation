import itertools

from main import main
from utils import plot_road

from initialization import *

road_sizes = [100, 200, 300]
number_of_wheel_passes_list = [100, 200]
standard_heights = [10, 20]
nr_of_irregular_points_list = [5, 10, 20]
wheel_sizes = [4, 6, 8]
velocities = [2, 5, 10]

all_lists = [road_sizes, number_of_wheel_passes_list]  # , standard_heights, nr_of_irregular_points_list, wheel_sizes,
# velocities]

for i, element in enumerate(itertools.product(*all_lists)):
    print(i)
    road_size = element[0]
    number_of_wheel_passes = element[1]
    parameter_dict = {'road_size': road_size, 'number_of_wheel_passes': number_of_wheel_passes}
    main(parameter_dict)
