import itertools
from multiprocessing import Pool

from main import main
from utils import plot_road

from initialization import *

wheel_sizes = [3, 10]
velocities = [3, 11]

alphas = [0.1, 0.5, 1]

smoothing_methods = ['strategy 1', 'strategy 2', 'strategy 3']
slope_iterations_list = [1, 6, 10]
# h_max_list = [2, 3, 5]

all_lists = [wheel_sizes, velocities, alphas, smoothing_methods, slope_iterations_list]
print(len(list(itertools.product(*all_lists))))


def func(tup):
    # if 0 <= i < 40:
    i = tup[0]
    element = tup[1]
    print(i)
    wheel_size = element[0]
    velocity = element[1]
    alpha = element[2]
    smoothing_method = element[3]
    slope_iterations = element[4]
    parameter_dict = {'it': i, 'wheel_size': wheel_size, 'velocity': velocity, 'alpha': alpha,
                      'smoothing_method': smoothing_method, 'slope_iterations': slope_iterations}
    main(parameter_dict)


with Pool(5) as p:
    p.map(func, [(i, x) for i, x in enumerate(itertools.product(*all_lists))])
