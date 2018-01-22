from road import Road
import pickle
import matplotlib.pyplot as plt

from initialization import *

def average_simulations(avg_iterations = 1):
    # from initialization import init
    from main import wheel_pass
    import numpy as np

    # road, wheel, debugging, number_of_wheel_passes, dig_method, \
    # dig_probability_args, smoothing_method, smoothing_args = init()

    initial_profile = np.copy(road.piles)
    avg_profile = np.full(road.size, 0, dtype=np.float)

    for iter in range(avg_iterations):
        wheel_pass(road, wheel, number_of_wheel_passes, 'max',
                   dig_method, dig_probability_args,
                   smoothing_method, smoothing_args)
        final_road_profile = np.copy(road.piles)
        avg_profile += final_road_profile
        road.piles = initial_profile

    avg_profile = avg_profile * (1.0/avg_iterations)
    road.piles = np.copy(avg_profile)

    plot_road(road)


def plot_road(road: Road, **kwargs):
    """
    Plots the road surface via matplotlib for a better smoother display.
    :param road:
    :return:
    """
    plt.clf()
    plt.plot(road.piles)
    plt.xlabel('Distance (block size units)')
    plt.ylabel('Surface height (block size units)')
    plt.title('Road surface profile')
    parameters = []
    if kwargs:
        foo = ', '.join(f'{key}: {value}' for key, value in kwargs.items())
    plt.title(foo)
    plt.grid(True)

    # plt.axes().set_aspect('equal', 'datalim')
    x_min = 0
    x_max = road.size
    y_min = 0 - 5
    y_max = max(road.piles) + 10
    plt.axis([x_min, x_max, y_min, y_max])
    plt.axes().set_aspect('equal', 'box')

    # plt.show()
    plt.savefig(f'plots/{foo}.png')


def print_road_surface(road: Road, wheel_pos=None, wheel_size=None):
    """
    Prints the road surface. It also prints the lower part of the wheel if  wheel_pos != None
    and wheel_size != None (both conditions at the same time)
    :param road: a Road
    :param wheel_pos: integer or None
    :param wheel_size: integer or None
    :return: prints the road with or without the wheel as standard output.
    """
    max_height = max(road.piles) + 1
    current_height = max_height
    road_surface = []
    for i in range(max_height + 1):
        for pos, height in enumerate(road.piles):
            if height >= current_height:
                road_surface.append('.')
            else:
                if (wheel_pos is not None) & (wheel_size is not None):
                    if wheel_pos - wheel_size < pos <= wheel_pos and height == current_height - 1:
                        road_surface.append('w')
                    else:
                        road_surface.append(' ')
                else:
                    road_surface.append(' ')
        current_height -= 1
        road_surface.append('\n')
    print(''.join(road_surface))


def save_road(road: Road, output_filename: str):
    """
    Writes the current road surface to a pickle file.
    :param road:
    :param output_filename:
    :return:
    """
    with open(output_filename, 'wb') as output:
        pickle.dump(road, output, pickle.HIGHEST_PROTOCOL)


def read_road(input_filename: str):
    """
    Reads a pickled(written) road surface and initializes a Road class instance
    :param input_filename:
    :return:
    """
    with open(input_filename, 'rb') as input:
        road = pickle.load(input)
    return road
