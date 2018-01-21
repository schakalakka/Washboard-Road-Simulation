from road import Road
import pickle
import matplotlib.pyplot as plt


def plot_road(road: Road):
    """
    Plots the road surface via matplotlib for a better smoother display.
    :param road:
    :return:
    """
    plt.plot(road.piles)
    plt.xlabel('Distance (block size units)')
    plt.ylabel('Surface height (block size units)')
    plt.title('Road surface profile')
    plt.grid(True)

    # plt.axes().set_aspect('equal', 'datalim')
    xmin = 0
    xmax = road.size
    ymin = 0 - 5
    ymax = max(road.piles) + 10
    plt.axis([xmin, xmax, ymin, ymax])
    plt.axes().set_aspect('equal', 'box')

    plt.show()


def print_road_surface(road: Road, wheel_pos=None, wheel_size=None):
    """
    Prints the road surface. It also prints the lower part of the wheel if  wheel_pos != None
    and wheel_size != None (both conditions at the same time)
    :param road: a Road
    :param wheel_pos: integer or None
    :param wheel_size: integer or None
    :return: prints the road with or without the wheel as standard output.
    """
    max_height = road.piles.max() + 1
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
