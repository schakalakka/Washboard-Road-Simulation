import itertools
from multiprocessing import Pool

import matplotlib.pyplot as plt
import numpy as np
from main import main
from utils import plot_road

from initialization import *

wheel_sizes = [3, 5, 7, 10, 20, 21, 30]
velocities = [3, 5, 6, 11, 20]

alphas = [0, 0.1, 0.5, 0.7, 1]
p_wind_list = [0, 0.1, 0.2, 0.5, 1]

all_lists = [wheel_sizes, velocities, alphas]
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


alpha = 0.1
main({'attempt': 1})
main({'attempt': 2})
main({'attempt': 3})


# with Pool(5) as p:
#     p.map(func, [(i, x) for i, x in enumerate(itertools.product(*all_lists))])

###### create csv
# print('velocity')
# from initialization import *
#
# for velocity in velocities:
#     main({'velocity': velocity})
#
# print('wheel_size')
# from initialization import *
#
# for wheel_size in wheel_sizes:
#     main({'wheel_size': wheel_size})
#
# print('alpha')
# from initialization import *
#
# for alpha in alphas:
#     main({'alpha': alpha})
#
# print('p_wind')
# from initialization import *
#
# for p_wind in p_wind_list:
#     main({'p_wind': p_wind})


#### creates plots

# print('velocity')
# from initialization import *
#
# for velocity in velocities:
#     csv_to_plot(f'csv/velocity-{velocity}.csv', velocity)
#
# print('wheel_size')
# from initialization import *
#
# for wheel_size in wheel_sizes:
#     csv_to_plot(f'csv/wheel_size-{wheel_size}.csv', wheel_size)
#
# print('alpha')
# from initialization import *
#
# for alpha in alphas:
#     csv_to_plot(f'csv/alpha-{alpha}'.replace('.', '')+'.csv', alpha)
#
# print('p_wind')
# from initialization import *
#
# for p_wind in p_wind_list:
#     csv_to_plot(f'csv/p_wind-{p_wind}'.replace('.', '')+'.csv', p_wind)

def csv_to_plot(param_list, parameter_name, overlay=True):
    # param_list has the form [('csv/alpha_01.csv', 0.1)]
    foo = [np.genfromtxt(csv_filename, delimiter=',', dtype=int, skip_header=1, usecols=1) for csv_filename, _ in
           param_list]
    # param_name, _ = csv_filename.split('/')[1].split('.')[0].split('-')
    plt.clf()
    # plt.title(f'{param_name}: {param_value}')
    if overlay:
        for param in foo:
            plt.plot(param)
            filename = f'plots/{parameter_name}-overlay.png'
    else:
        f, axx = plt.subplots(len(param_list), sharex=True, sharey=True)
        for i, param in enumerate(foo):
            axx[i].plot(foo)
        f.subplots_adjust(hspace=0)
        plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
        filename = f'plots/{parameter_name}-subplots.png'

    # plt.axis([0, len(foo), 0, max(foo)+5])
    plt.savefig(filename, dpi=900, format='png')
