import numpy as np

from road import Road
from wheel import Wheel


def max_smoothing(road: Road, maxh: int):
    # maxh = 7
    while max(road) > maxh:
        for i in range(road.size):
            if road[i] > maxh:
                for n in range(1, road.size):
                    right = (i + n) % road.size
                    left = (i - n) % road.size
                    rightr = road[right]
                    leftr = road[left]
                    if rightr < leftr and rightr < maxh:
                        road.add_grain(right)
                        road.remove_grain(i)
                        break
                    elif rightr > leftr and leftr < maxh:
                        road.add_grain(left)
                        road.remove_grain(i)
                        break
                    elif rightr == leftr and rightr < maxh:
                        uniran = np.random.uniform(0, 1)
                        if uniran >= 0.5:
                            road.add_grain(right)
                            road.remove_grain(i)
                            break
                        else:
                            road.add_grain(left)
                            road.remove_grain(i)
                            break


def slope_smoothing(road: Road):
    for i in range(road.size):
        i2 = (i + 1) % road.size
        height1 = road[i]
        height2 = road[i2]
        diff = height1 - height2
        if diff > 1:
            road.add_grain(i2)
            road.remove_grain(i)
        elif diff < -1:
            road.add_grain(i)
            road.remove_grain(i2)


def general_slope_smoothing(road: Road, slope_inverse=3):
    """

    :param road:
    :param slope_inverse:
    :return:
    """
    if slope_inverse < 1:  # do nothing if the slope is not a positive integer
        return
    for i in range(0, road.size, slope_inverse):
        end_segm_slice_point = i + 2 * slope_inverse
        sum_over_next_segment = np.sum(road.piles[i:end_segm_slice_point])
        average_over_next_segment = sum_over_next_segment / (2 * slope_inverse)
        average_floor_int = int(average_over_next_segment)
        start_segm_height = road[i]
        end_segm_index = end_segm_slice_point-1
        end_segm_height = road.piles[end_segm_index]
        road.piles[i:end_segm_slice_point] = average_floor_int

        rest_to_distribute = sum_over_next_segment - average_floor_int * 2 * slope_inverse
        if start_segm_height == end_segm_height:
            if rest_to_distribute > 0:
                road.add_random_irregularities(rest_to_distribute, (i, end_segm_slice_point))
        elif start_segm_height < end_segm_height:
            if rest_to_distribute == 0:
                road.remove_grain(start_segm_height)
                road.add_grain(end_segm_height)
            else:
                k = int(rest_to_distribute / 3)
                road.add_grains(range(end_segm_slice_point - k, end_segm_slice_point), [2] * k)
                rest_to_distribute -= 2 * k
                road.add_grains(range(end_segm_slice_point - k - rest_to_distribute, end_segm_slice_point - k),
                                [1] * rest_to_distribute)
        elif start_segm_height > end_segm_height:
            if rest_to_distribute == 0:
                road.add_grain(start_segm_height)
                road.remove_grain(end_segm_height)
            else:
                k = int(rest_to_distribute / 3)
                road.add_grains(range(i, i + k), [2] * k)
                rest_to_distribute -= 2 * k
                road.add_grains(range(i + k, i + k + rest_to_distribute), [1] * rest_to_distribute)


def smoothing(road: Road, wheel: Wheel, iterations=1):
    """
    @TO DO THE SAME FORMAT AS digging.py, this would be the general function and then we
    can consider sub-smoothing procedures. This one would be one procedure, for example --->
    :param iterations:
    :param road:
    :return:
    """
    # print_road_surface(road, wheel.xf, wheel.diameter)
    general_slope_smoothing(road, slope_inverse=3)
    # max_smoothing(road, (road.height + 5))
    # print_road_surface(road, wheel.xf, wheel.diameter)


# for i in range(iterations):
#      slope_smoothing(road)
# max_smoothing(road, (road.height+2) )
# print_road_surface(road, wheel.xf, wheel.diameter)


######not working yet
def cellular_automata_smoothing(road: Road, iterations: int,
                                D: float, gamma: float,
                                v: float, S_c: int, d: int):
    # FOR US d = 1? width of columns

    N = road.size
    R = road.piles.astype(float)
    h = np.maximum(R - 2, 0)

    # h = road.piles.astype(float)
    # R = np.maximum(h-2,0)

    dR = np.full(N, 0, dtype=np.float)
    dh = np.full(N, 0, dtype=np.float)

    for i in range(N):
        # im = (i-1) % N
        ip = (i + 1) % N
        dh[i] = (h[ip] - h[i]) / d
        dR[i] = (R[ip] - R[i]) / d

    for iter in range(iterations):
        for i in range(N):
            # im = (i-1) % N
            ip = (i + 1) % N

            dh[i] = (h[ip] - h[i]) / d
            dR[i] = (R[ip] - R[i]) / d

            R[i] = R[i] + (-v * R[i] + D * dR[i]) - R[i] * gamma * (dh[i] - abs(S_c))
            h[i] = h[i] + R[i] * gamma * (dh[i] - abs(S_c))
            R[ip] = R[ip] - (-v * R[i] + D * dR[i])

    road.piles = np.round(R).astype(int)
