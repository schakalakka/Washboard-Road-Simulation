import itertools
from multiprocessing import Pool

from main import main
from utils import plot_road

from initialization import *

wheel_sizes = [3, 5, 7, 10, 20, 21, 30]
velocities = [3, 5, 6, 11, 20]

alphas = [0.1, 0.5, 0.7, 1]
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


# with Pool(5) as p:
#     p.map(func, [(i, x) for i, x in enumerate(itertools.product(*all_lists))])


print('velocity')
from initialization import *

for velocity in velocities:
    main({'velocity': velocity})

print('wheel_size')
from initialization import *

for wheel_size in wheel_sizes:
    main({'wheel_size': wheel_size})

print('alpha')
from initialization import *

for alpha in alphas:
    main({'alpha': alpha})

print('p_wind')
from initialization import *

for p_wind in p_wind_list:
    main({'p_wind': p_wind})
