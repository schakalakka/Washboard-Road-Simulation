from road import Road
from wheel import Wheel
import numpy as np

def determine_bump_height(road: Road, wheel: Wheel, position: int, method='max') -> int:
    """
    General bump height function, returns the bump height of a position on a road for a given
    wheel_size and method
    :param road: a Road
    :param wheel: a Wheel
    :param position: int
    :param method: str, 'max'
    :return: a bump_height function call
    """
    available_methods = list(['max', 'max'])
    default_method = 'max'
    method = method

    if method not in available_methods:
        print("The bump_height method '", method, "' does not exist. Using default method '", default_method, "'")
        method = 'max'

    if method == 'max':
        return max_bump_height(road, wheel, position)


def max_bump_height(road: Road, wheel: Wheel, position: int) -> int:
    """
    At position i determine the bump height of the next w elements/indexes/positions
    with w being the wheel diameter.
    The bump height is determined by taking the maximum from the positions i+1 to i+w (inclusive) minus
    the current elevation of the wheel.
    :param road: a Road
    :param wheel: a Wheel
    :param position: int, current (front) position of the wheel
                         (it should be the first position before the bump position)
    :return: the bump height
    """
    return np.max(road.piles[(position + 1): (position + 1 + wheel.diameter)]) - wheel.elevation

